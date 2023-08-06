# -*- coding: utf-8 -*-
"""ui_application."""

import os
import re
from pathlib import Path
import importlib.resources

from gi.repository import GLib
from PySide2.QtGui import QIcon
from PySide2.QtCore import QMetaObject, Slot
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QLabel
)

from usbimager import (
    __version__, APP_NAME, APP_ORGANISATION, APP_ID, APP_TITLE, APP_ABOUT
)
from usbimager.ui_mainwindow import Ui_MainWindow
from usbimager.ui_targetwidget import Ui_targetwidget
from usbimager.shared_objects import SharedObjects as shared
from usbimager.threads import WritingThread
from usbimager.modules.filesize import FileSize


STATUSBAR_TIMEOUT = 5000


class Application(QApplication):
    """Application."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_application()
        self.mainwindow = MainWindow()
        self.mainwindow.show()

    def setup_application(self) -> None:
        """Application setup."""
        self.setApplicationName(APP_NAME)
        self.setApplicationVersion(__version__)
        self.setOrganizationName(APP_ORGANISATION)
        self.setOrganizationDomain(APP_ID)

        icon = get_app_icon()
        self.setWindowIcon(icon)

        # TODO
        # Configure style
        # self.setStyle('kvantum')
        # Choose theme: KvLibadwaitaMaiaDark in kvantum configurator

        # app_style = get_qss_text('style.qss')
        # self.setStyleSheet(app_style)


class MainWindow(QMainWindow):
    """MainWidget."""

    def __init__(self):
        super().__init__()

        self.init_mainwindow()

        shared.udisks2.signal_connect_obj_added(self.callback_object_added)
        shared.udisks2.signal_connect_obj_removed(self.callback_object_removed)

        self.init_targetwidgets()

    def init_mainwindow(self) -> None:
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle(APP_TITLE)
        self.ui.toolButton_menu.setMenu(self.ui.menuInfo)
        self.ui.menubar.hide()

        self.label_version = QLabel('V ' + __version__)
        self.ui.statusbar.addPermanentWidget(self.label_version)

        QMetaObject.connectSlotsByName(self)

    def init_targetwidgets(self) -> None:
        block_device_pathes = \
            shared.udisks2.get_object_pathes('block_devices')

        for object_path in block_device_pathes:
            if self.is_usb_key(object_path):
                self.add_targetwidget(object_path)

    def add_targetwidget(self, object_path: str) -> str:
        widget = TargetWidget(object_path, self)
        widget.ui.progressbar.valueChanged.connect(
            self.update_progressbar_all)
        # widget.ui.pushButton_stop

        self.ui.verticalLayout_targets.addWidget(widget)
        shared.targetwidgets.append(widget)

        return widget.device_info

    def callback_object_added(self, sender, dbus_object) -> None:
        object_path = dbus_object.get_object_path()

        if self.is_usb_key(object_path):
            device_info = self.add_targetwidget(object_path)
            self.ui.statusbar.showMessage(
                f"USB-Device added:  {device_info}", STATUSBAR_TIMEOUT)

    def callback_object_removed(self, sender, dbus_object) -> None:
        object_path = dbus_object.get_object_path()

        for widget in shared.targetwidgets:
            if widget.object_path == object_path:
                device_info = widget.device_info
                widget.close()
                shared.targetwidgets.remove(widget)
                self.ui.statusbar.showMessage(
                    f"USB-Device removed:  {device_info}", STATUSBAR_TIMEOUT)

    @Slot(bool)
    def on_checkBox_select_all_toggled(self, checked: bool) -> None:
        if shared.targetwidgets:
            for widget in shared.targetwidgets:
                widget.ui.checkBox_switch.setChecked(checked)

    @Slot(bool)
    def on_checkBox_verify_all_toggled(self, checked: bool) -> None:
        if shared.targetwidgets:
            for widget in shared.targetwidgets:
                widget.ui.checkBox_verify.setChecked(checked)

    @Slot()
    def on_pushButton_open_clicked(self):
        homedir = Path.home() / 'Downloads'
        filters = ('Image Files (*.iso *.img *.raw *.bin *.dd)',)

        filename = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open Image",
            dir=str(homedir),
            filter=';;'.join(filters)
            )[0]

        if filename:
            filename = Path(filename)
            if filename.match('*.iso') and not self.is_bootable_iso(filename):
                return
            shared.imagepath = filename
            self.ui.label_imagename.setText(shared.imagepath.name)

            size = os.path.getsize(shared.imagepath)
            imagesize = FileSize(size).convert(max_decimals=1)
            self.ui.label_imagesize.setText(str(imagesize))

    @Slot()
    def on_pushButton_start_all_clicked(self) -> None:
        if not shared.targetwidgets:
            return

        for widget in shared.targetwidgets:
            if widget.ui.checkBox_switch.isChecked():
                break
        else:
            message = "Please select a device for writing."
            self.ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)
            return

        if not shared.imagepath:
            message = "Please select an image to use!"
            self.ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)
            return

        # Check for mounted filesystems on all devices and try to unmount them
        for widget in shared.targetwidgets:
            widget.are_filesystem_mounted()

        # Security question before start writing
        text = \
            "All selected devices will be completely overwritten "\
            "and data on it will be lost.\n\n" \
            "Do you want to continue the process?"
        result = QMessageBox.warning(self, "Warning", text,
                                     QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            return

        # Start writing
        for widget in shared.targetwidgets:
            if not widget.ui.checkBox_switch.isChecked():
                continue
            widget.on_pushButton_start_clicked(
                security_message=False)

    @Slot()
    def on_pushButton_stop_all_clicked(self) -> None:
        if shared.targetwidgets:
            for widget in shared.targetwidgets:
                widget.on_pushButton_stop_clicked()

    @Slot()
    def on_actionAboutQt_triggered(self) -> None:
        QMessageBox.aboutQt(self)

    @Slot()
    def on_actionAbout_triggered(self) -> None:
        QMessageBox.about(self, "About USB-Imager", APP_ABOUT)

    def is_bootable_iso(self, filepath: Path) -> bool:
        is_bootable = False

        try:
            with filepath.open(mode='rb') as file:
                file.seek(510)
                mbr_signature = file.read(2).hex()
        except OSError as error:
            self.ui.statusbar.showMessage(error.args)
        else:
            if mbr_signature == '55aa':
                is_bootable = True
            else:
                message = "Selected ISO file is not bootable!"
                self.ui.statusbar.showMessage(message, STATUSBAR_TIMEOUT)

        return is_bootable

    def is_usb_key(self, object_path: str) -> bool:
        """
        Check if given object path is a USB-Stick.

        NOTE: This method only works if a device is plugged in!!!

        Parameters
        ----------
        object_path : str
            An object path string like \
                '/org/freedesktop/UDisks2/block_devices/sda'.

        Returns
        -------
        bool
            True/False if USB-Key is detected or not.

        """
        is_usbdev = True

        whole_block_device_pathes = \
            shared.udisks2.get_object_pathes_whole_block_device()
        interface = shared.udisks2.get_interface(object_path, 'Block')
        if not interface:
            return False

        if object_path not in whole_block_device_pathes:
            is_usbdev = False
        elif re.search(r"[0-9]$", object_path):
            is_usbdev = False
        else:
            drive_path, device_path, size = \
                interface.get_properties('drive', 'device', 'size')

            if not drive_path or drive_path == '/':
                is_usbdev = False
            elif not device_path or device_path == '/':
                is_usbdev = False
            elif not size or size == 0:
                is_usbdev = False
            else:
                interface = shared.udisks2.get_interface(drive_path, 'Drive')
                if not interface:
                    return False

                connection_bus, removable = \
                    interface.get_properties('connection-bus', 'removable')

                if removable is False or connection_bus != "usb":
                    is_usbdev = False

        return is_usbdev

    def update_progressbar_all(self) -> None:
        threads = 0
        progressbar_values = 0

        for widget in shared.targetwidgets:
            if widget.copythread and widget.copythread.isRunning():
                threads += 1
                progressbar_values += widget.ui.progressbar.value()
            elif widget.ui.progressbar.value() == 100:
                threads += 1
                progressbar_values += 100

        if threads:
            value = progressbar_values / threads
            self.ui.progressbar_all.setFormat('Process... %p%')
            self.ui.progressbar_all.setValue(value)
        else:
            self.ui.progressbar_all.setFormat('All canceled... %p%')

        if self.ui.progressbar_all.value() == 100:
            self.ui.progressbar_all.setFormat('All done... %p%')


class TargetWidget(QWidget):
    """Widget stores all data about target device."""

    def __init__(self,
                 object_path: str,
                 mainwindow: QMainWindow):
        super().__init__()

        self.object_path = object_path
        self.mainwindow = mainwindow

        self.ui = Ui_targetwidget()
        self.ui.setupUi(self)

        # Device properties
        self.path = None
        self.vendor = "[No Vendor]"
        self.model = "[No Model]"
        self.size = 0
        self.init_properties()
        self.humanreadable_size = \
            str(FileSize(self.size).convert(max_decimals=1))

        self.copythread = None

        self.init_ui()

    def init_properties(self) -> None:
        """Set properties path, vendor, model, size."""
        drive_path = \
            shared.udisks2.get_property(self.object_path, 'Block', 'drive')
        device_path = \
            shared.udisks2.get_property(self.object_path, 'Block', 'device')

        self.path = Path(device_path)

        interface = \
            shared.udisks2.get_interface(drive_path, 'Drive')
        self.size, vendor, model = \
            interface.get_properties('size', 'vendor', 'model')

        if vendor:
            self.vendor = vendor
        if model:
            self.model = model

    @property
    def device_info(self) -> str:
        return f"{self.vendor} - {self.model} ({self.path.name})"

    def init_ui(self) -> None:
        """Set USB-Stick informations to label_stickname."""

        self.ui.label_stickname.setText(self.device_info)
        self.ui.label_sticksize.setText(self.humanreadable_size)

        # Add buffer sizes to comboBox_buffers
        # NOTE: os.sendfile doesn't work in my test with parameter count < 4096
        sizes = [4096, 8192, 16384, 32768,
                 1024 ** 2, 2048 ** 2, 4096 ** 2]
        for blksize in sizes:
            filesize = str(FileSize(blksize).convert())
            self.ui.comboBox_buffers.addItem(filesize, blksize)
        self.ui.comboBox_buffers.setCurrentIndex(4)

        self.switch_visible_stats(False)
        QMetaObject.connectSlotsByName(self)

    @Slot()
    def on_pushButton_start_clicked(self,
                                    security_message: bool = True) -> None:

        if not self.ui.checkBox_switch.isChecked():
            # If checkBox_switch is not checked, pushButton_start is disabled
            # The return statement is nevertheless set for safety.
            return

        if not shared.imagepath:
            message = "Please select an image to use!"
            self.mainwindow.ui.statusbar.showMessage(
                message, STATUSBAR_TIMEOUT)
            return

        # Check if the target device is large enough for the image file.
        srcfile_size = os.path.getsize(shared.imagepath)
        if srcfile_size > self.size:
            message = \
                "Error:  " \
                "The size of the device is too small to write the image."
            self.mainwindow.ui.statusbar.showMessage(
                message, STATUSBAR_TIMEOUT)
            return

        # Check for mounted filesystems on all devices and try to unmount them
        if self.are_filesystem_mounted():
            return

        # Security question before start writing
        if security_message:
            text = \
                "The device will be completely overwritten " \
                "and data on it will be lost.\n\n" \
                "Do you want to continue the process?"
            result = QMessageBox.warning(self, "Warning", text,
                                         QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.No:
                return

        # Start writing
        blksize = self.ui.comboBox_buffers.currentData()
        validation = self.ui.checkBox_verify.isChecked()

        self.copythread = WritingThread(shared.imagepath,
                                        self.object_path,
                                        blksize,
                                        validation)

        self.copythread.started.connect(
            lambda: self.switch_enabled_widgets(False))
        self.copythread.finished.connect(self.finished_writing)

        self.start_writing()

    @Slot()
    def on_pushButton_stop_clicked(self) -> None:
        if self.copythread:
            self.copythread.stop_writing()

    def start_writing(self) -> None:
        if self.copythread:
            self.copythread.sig_progress_value.connect(
                self.ui.progressbar.setValue)
            self.copythread.sig_progress_format.connect(
                self.ui.progressbar.setFormat)
            self.copythread.sig_timer_results.connect(
                self.set_stats)
            self.copythread.sig_status.connect(
                self.mainwindow.ui.statusbar.showMessage)

            self.mainwindow.ui.statusbar.clearMessage()
            self.copythread.start()

    def finished_writing(self) -> None:
        self.copythread.wait()
        self.switch_enabled_widgets(True)
        self.mainwindow.update_progressbar_all()

    def are_filesystem_mounted(self) -> bool:
        mounted = False

        mounted_filesystem_interfaces = \
            shared.udisks2.get_mounted_filesystems(self.object_path)

        if mounted_filesystem_interfaces:
            text = \
                f"There are filesystem(s) mounted on {self.device_info}.\n\n" \
                "Would you like to unmount them?"
            result = QMessageBox.warning(self, "Warning", text,
                                         QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.No:
                mounted = True
                return mounted

            for iface_fs in mounted_filesystem_interfaces:
                # Unmount device
                arg_options = shared.udisks2.preset_args['unmount']
                try:
                    iface_fs.call_unmount_sync(arg_options)
                except GLib.Error as error:
                    self.mainwindow.ui.statusbar.showMessage(error.message)
                    mounted = True
                    break
                else:
                    shared.udisks2.settle()

        # TODO
                # Lock device if unlocked
                # object_path = iface_fs.get_object_path()
                # unlocked_encrypted = \
                #     shared.udisks2.get_unlocked_encrypted(object_path)
                # if unlocked_encrypted:
                #     arg_options = shared.udisks2.preset_args['lock']
                #     try:
                #         unlocked_encrypted.call_lock_sync(arg_options)
                #     except GLib.Error as error:
                #         self.mainwindow.ui.statusbar.showMessage(error.message)
                #         return

                #     shared.udisks2.settle()

        return mounted

    def switch_enabled_widgets(self, switch: bool) -> None:
        # TargetWidget widgets
        self.ui.pushButton_start.setEnabled(switch)
        self.ui.checkBox_switch.setEnabled(switch)
        self.ui.checkBox_verify.setEnabled(switch)
        self.ui.comboBox_buffers.setEnabled(switch)

        # MainWindow widgets

        # checkBox_switch and ui_pushButton_start_all remains disabled
        # as long as a copythread is running
        if switch is False:
            self.mainwindow.ui.pushButton_start_all.setEnabled(switch)
            self.mainwindow.ui.checkBox_select_all.setEnabled(switch)
            self.mainwindow.ui.checkBox_verify_all.setEnabled(switch)
        elif switch is True:
            for widget in shared.targetwidgets:
                if not widget.ui.checkBox_switch.isEnabled():
                    break
            else:
                self.mainwindow.ui.pushButton_start_all.setEnabled(switch)
                self.mainwindow.ui.checkBox_select_all.setEnabled(switch)
                self.mainwindow.ui.checkBox_verify_all.setEnabled(switch)

    def switch_visible_stats(self, switch: bool) -> None:
        self.ui.label_speed.setVisible(switch)
        self.ui.label_time_cpu.setVisible(switch)
        self.ui.label_time.setVisible(switch)

    @Slot(float, float, int)
    def set_stats(self,
                  time: float,
                  time_cpu: float,
                  bytes_per_sec: int) -> None:

        if not time and not time_cpu and not bytes_per_sec:
            self.switch_visible_stats(False)
            return

        if bytes_per_sec:
            speed = FileSize(bytes_per_sec).convert('MiB', max_decimals=2)
            self.ui.label_speed.setText(f'{speed}/s')
            self.ui.label_speed.setVisible(True)
        if time:
            time = round(time, 2)
            self.ui.label_time.setText(f"{time} s")
            self.ui.label_time.setVisible(True)
        if time_cpu:
            time_cpu = round(time_cpu, 2)
            self.ui.label_time_cpu.setText(f"{time_cpu} s")
            self.ui.label_time_cpu.setVisible(True)


def get_app_icon() -> QIcon:
    path = importlib.resources.files('usbimager.resources')
    icon = QIcon(str(path) + '/' + 'usb-imager.ico')
    return icon


def get_qss_text(qss_filename: str) -> str:
    path = importlib.resources.files('usbimager.resources')
    qss_text = path.joinpath(qss_filename).read_text()
    return qss_text
