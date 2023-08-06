# -*- coding: utf-8 -*-
"""SharedObjects."""

import os
from usbimager.modules.udisks2 import UDisks2


class SharedObjects:
    imagepath = None
    targetwidgets = []

    udisks2 = UDisks2()
