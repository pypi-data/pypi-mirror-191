# -*- coding: utf-8 -*-
"""Threading."""

import os
import hashlib
from pathlib import Path
from typing import Union

from gi.repository import GLib, Gio
from PySide2.QtCore import Signal, Slot, QThread

from usbimager.shared_objects import SharedObjects as shared
from usbimager.modules.timer import Timer


class WritingThread(QThread):
    """Writing worker class.

    Unlike QRunnable the QThread class does inherit from QObject so you can
    define the signals on the thread object itself.
    """

    sig_progress_value = Signal(int)
    sig_progress_format = Signal(str)
    sig_timer_results = Signal(float, float, int)
    sig_status = Signal(str)

    timer = Timer()

    def __init__(self,
                 image_file: Path,
                 object_path: str,
                 bufsize: int = 1024 ** 2,
                 validation: bool = False):
        super().__init__()

        self.image_file = image_file
        self.image_size = os.path.getsize(self.image_file)
        self.object_path = object_path
        self.bufsize_user = bufsize
        self.validation = validation

        self.cancel = False
        self.progressbar_current_value = 0

    def stop_writing(self) -> None:
        """Stop writing to device."""
        self.cancel = True

    @Slot()
    def run(self):
        """Run thread."""
        written = 0
        progress_steps = 100

        in_fd, out_fd = self.get_fd_all()
        if not in_fd or not out_fd:
            return

        try:
            self.sig_progress_format.emit('Writing... %p%')
            self.sig_timer_results.emit(0, 0, 0)
            self.timer.start()

            while written < self.image_size:
                if self.cancel is True:
                    break
                # NOTE:
                # os.sendfile doesn't work in my tests with parameter less than
                # count=4096
                written += os.sendfile(out_fd, in_fd,
                                       offset=None, count=self.bufsize_user)

                if self.validation:
                    progress_steps = 50
                self.update_progressbar(written,
                                        self.image_size,
                                        self.progressbar_current_value,
                                        progress_start=0,
                                        progress_steps=progress_steps)

            self.timer.stop()
            bytes_per_sec = int(written / self.timer.result)
            self.sig_timer_results.emit(self.timer.result,
                                        self.timer.result_cpu,
                                        bytes_per_sec)

        except OSError:
            # FIXME
            # Here is not always thrown an exception.
            # (e.g. when removing a USB stick while writing).
            format_msg = 'Error while writing, writing canceled... %p%'
            self.sig_progress_format.emit(format_msg)
        else:
            if self.cancel is True:
                format_msg = 'Writing canceled... %p%'
            else:
                format_msg = 'Writing finished... %p%'
            self.sig_progress_format.emit(format_msg)
        finally:
            self.close_fd_all(in_fd, out_fd)

        self.close_fd_all(in_fd, out_fd)

        if self.validation:
            format_msg = 'Validating... %p%'
            self.sig_progress_format.emit(format_msg)

            is_valid = self.start_validation()

            if self.cancel is True:
                format_msg = 'Validation canceled... %p%'
                self.sig_progress_format.emit(format_msg)
            elif is_valid is True:
                format_msg = 'Validation successful... %p%'
                self.sig_progress_format.emit(format_msg)
            elif is_valid is False:
                format_msg = 'Validation failed... %p%'
                self.sig_progress_format.emit(format_msg)

    def get_fd_all(self) -> tuple:
        in_fd = self.get_fd_image(self.image_file)
        out_fd = self.get_fd_device(mode='w')

        if not out_fd:
            os.close(in_fd)
            in_fd = None

        return in_fd, out_fd

    def get_fd_image(self, file: Path) -> Union[int, None]:
        filedescriptor = None

        try:
            filedescriptor = os.open(file, os.O_RDONLY)
        except OSError as error:
            self.sig_status.emit(error.args)

        return filedescriptor

    def get_fd_device(self, mode: str) -> Union[int, None]:
        filedescriptor = None

        if mode == 'r':
            arg_options = shared.udisks2.preset_args['open_device_backup']
        elif mode == 'w':
            arg_options = shared.udisks2.preset_args['open_device_restore']
        else:
            self.sig_status.emit('Couldn´t get a file descriptor for device.')
            return filedescriptor

        interface_block = \
            shared.udisks2.get_interface(self.object_path, 'Block')

        if not interface_block:
            return None

        # interface.call_open_device is recommended since UDisks v273
        if shared.udisks2.version >= 273:
            try:
                result = interface_block.call_open_device_sync(
                    mode, arg_options, Gio.UnixFDList(), None)
            except GLib.Error as error:
                self.sig_status.emit(error.message)
            else:
                if result:
                    out_fd, out_fd_list = result
                    filedescriptor = out_fd_list.get(out_fd.unpack())
                shared.udisks2.settle()

        return filedescriptor

    def close_fd_all(self, *args) -> bool:
        all_fd_closed = False

        try:
            for file_fd in args:
                os.close(file_fd)
        except OSError as error:
            self.sig_status.emit(error.args)
        else:
            all_fd_closed = True

        return all_fd_closed

    def start_validation(self) -> bool:
        valid = False

        hash_file = self.hash_file()
        hash_device = self.hash_device()

        if hash_file and hash_device:
            if hash_file == hash_device:
                valid = True

            # print('hash_file =', hash_file)
            # print('hash_device =', hash_device)

        return valid

    def hash_file(self) -> str:
        hexdigest = ''

        hashobj = hashlib.sha256()
        bufsize = 1024 ** 2
        read_total = 0

        with self.image_file.open('rb') as file:
            buffer = file.read(bufsize)
            hashobj.update(buffer)
            read_total += len(buffer)
            while len(buffer) > 0:
                if self.cancel is True:
                    break
                buffer = file.read(bufsize)
                hashobj.update(buffer)
                read_total += len(buffer)
                self.update_progressbar(read_total,
                                        self.image_size,
                                        self.progressbar_current_value,
                                        progress_start=50,
                                        progress_steps=25)

        hexdigest = hashobj.hexdigest()

        return hexdigest

    def hash_device(self) -> str:
        hexdigest = ''

        hashobj = hashlib.sha256()
        bufsize = 1024 ** 2
        bufsize_rest = self.image_size % bufsize
        read = 0

        fd_in = self.get_fd_device('r')
        if fd_in:
            if bufsize_rest:
                buffer = os.read(fd_in, bufsize_rest)
                hashobj.update(buffer)
                read += len(buffer)
            while read < self.image_size:
                if self.cancel is True:
                    break
                buffer = os.read(fd_in, bufsize)
                hashobj.update(buffer)
                read += len(buffer)
                self.update_progressbar(
                    read,
                    self.image_size,
                    self.progressbar_current_value,
                    progress_start=75,
                    progress_steps=25)
            self.close_fd_all(fd_in)

        hexdigest = hashobj.hexdigest()

        return hexdigest

    def update_progressbar(self,
                           progress: int,
                           progress_total: int,
                           progressbar_current_value: int,
                           progress_start: int = 0,
                           progress_steps: int = 100) -> int:
        """
        Update the progressbar.

        Parameters
        ----------
        progress : int
            The processed size of the progress object.
        progress_total : int
            The total size of the progress object.
        progressbar_current_value : int
            The current value of progressbar.

            This function needs to know the current value of the progress bar
            to update it only when it changes. The calculated floating point
            values are truncated to their nominal value for
            QProgressBar.setValue (int). Therefore they often result in the
            same value.

            If the current value cannot be read from QProgressBar.value(), it
            can also be stored in a variable of the calling function of
            update_progressbar().
        progress_start : int, optional
            The starting value of the progress bar. The default is 0.
        progress_steps : int, optional
            The end value of the progress bar. The default is 100.

        Returns
        -------
        int
            The current value of progressbar.

        """
        progressbar_value = int(
            progress * progress_steps / progress_total + progress_start)
        if progressbar_value > progressbar_current_value:
            self.sig_progress_value.emit(progressbar_value)
            progressbar_current_value = progressbar_value
