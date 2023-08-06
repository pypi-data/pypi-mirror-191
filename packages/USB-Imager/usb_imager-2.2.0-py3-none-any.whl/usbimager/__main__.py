#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__main__."""

# import os
import sys

from usbimager.ui_application import Application
from usbimager.modules.udisks2 import UDisks2
from usbimager.modules.msgbox import MsgBox


def check_deps() -> None:
    """Check system dependencies."""
    if sys.version_info.major < 3 or sys.version_info.minor < 9:
        MsgBox().error("Python version must be at least 3.9!")
        sys.exit(1)

    # Check for platform 'linux'
    if not sys.platform.startswith('linux'):
        MsgBox().error("Programm only supports Unix!")
        sys.exit(1)

    # Check for installed UDisks2/D-Bus
    if not UDisks2.has_udisks2():
        MsgBox().error("UDisks2 was not found!")
        sys.exit(1)


def main() -> int:
    """Start application."""
    check_deps()

    # os.environ['QT_STYLE_OVERRIDE'] = "kvantum"
    # os.environ['QT_QPA_PLATFORMTHEME'] = "gnome"
    app = Application(sys.argv)
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
