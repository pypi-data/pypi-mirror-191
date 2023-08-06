# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'targetwidgetjHklBG.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_targetwidget(object):
    def setupUi(self, targetwidget):
        if not targetwidget.objectName():
            targetwidget.setObjectName(u"targetwidget")
        targetwidget.resize(500, 126)
        self.verticalLayout_2 = QVBoxLayout(targetwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame_targetwidget = QFrame(targetwidget)
        self.frame_targetwidget.setObjectName(u"frame_targetwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_targetwidget.sizePolicy().hasHeightForWidth())
        self.frame_targetwidget.setSizePolicy(sizePolicy)
        self.frame_targetwidget.setFrameShape(QFrame.StyledPanel)
        self.frame_targetwidget.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_targetwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_settings = QHBoxLayout()
        self.horizontalLayout_settings.setObjectName(u"horizontalLayout_settings")
        self.checkBox_switch = QCheckBox(self.frame_targetwidget)
        self.checkBox_switch.setObjectName(u"checkBox_switch")
        self.checkBox_switch.setChecked(True)

        self.horizontalLayout_settings.addWidget(self.checkBox_switch)

        self.label_stickname = QLabel(self.frame_targetwidget)
        self.label_stickname.setObjectName(u"label_stickname")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_stickname.sizePolicy().hasHeightForWidth())
        self.label_stickname.setSizePolicy(sizePolicy1)
        self.label_stickname.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_settings.addWidget(self.label_stickname)


        self.verticalLayout.addLayout(self.horizontalLayout_settings)

        self.horizontalLayout_progress = QHBoxLayout()
        self.horizontalLayout_progress.setObjectName(u"horizontalLayout_progress")
        self.progressbar = QProgressBar(self.frame_targetwidget)
        self.progressbar.setObjectName(u"progressbar")
        self.progressbar.setValue(0)

        self.horizontalLayout_progress.addWidget(self.progressbar)


        self.verticalLayout.addLayout(self.horizontalLayout_progress)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_verify = QCheckBox(self.frame_targetwidget)
        self.checkBox_verify.setObjectName(u"checkBox_verify")

        self.horizontalLayout_2.addWidget(self.checkBox_verify)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.horizontalLayout_stats = QHBoxLayout()
        self.horizontalLayout_stats.setSpacing(12)
        self.horizontalLayout_stats.setObjectName(u"horizontalLayout_stats")
        self.label_speed = QLabel(self.frame_targetwidget)
        self.label_speed.setObjectName(u"label_speed")

        self.horizontalLayout_stats.addWidget(self.label_speed)

        self.label_time_cpu = QLabel(self.frame_targetwidget)
        self.label_time_cpu.setObjectName(u"label_time_cpu")

        self.horizontalLayout_stats.addWidget(self.label_time_cpu)

        self.label_time = QLabel(self.frame_targetwidget)
        self.label_time.setObjectName(u"label_time")

        self.horizontalLayout_stats.addWidget(self.label_time)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_stats)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_sticksize = QLabel(self.frame_targetwidget)
        self.label_sticksize.setObjectName(u"label_sticksize")
        self.label_sticksize.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_sticksize)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButton_stop = QPushButton(self.frame_targetwidget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        icon = QIcon()
        iconThemeName = u"media-playback-stop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u"../../../../../../.designer/backup", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_stop.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.pushButton_stop)

        self.pushButton_start = QPushButton(self.frame_targetwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        icon1 = QIcon()
        iconThemeName = u"media-playback-start"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u"../../../../../../.designer/backup", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_start.setIcon(icon1)

        self.horizontalLayout_4.addWidget(self.pushButton_start)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.comboBox_buffers = QComboBox(self.frame_targetwidget)
        self.comboBox_buffers.setObjectName(u"comboBox_buffers")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.comboBox_buffers.sizePolicy().hasHeightForWidth())
        self.comboBox_buffers.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.comboBox_buffers)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addWidget(self.frame_targetwidget)


        self.retranslateUi(targetwidget)
    # setupUi

    def retranslateUi(self, targetwidget):
        targetwidget.setWindowTitle(QCoreApplication.translate("targetwidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.checkBox_switch.setToolTip(QCoreApplication.translate("targetwidget", u"Enable/disable writing", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_switch.setText("")
        self.label_stickname.setText(QCoreApplication.translate("targetwidget", u"USB-Stick Info", None))
#if QT_CONFIG(tooltip)
        self.checkBox_verify.setToolTip(QCoreApplication.translate("targetwidget", u"Verify after writing (Hash).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_verify.setText(QCoreApplication.translate("targetwidget", u"Verify", None))
#if QT_CONFIG(tooltip)
        self.label_speed.setToolTip(QCoreApplication.translate("targetwidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Overall speed after writing.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_speed.setText(QCoreApplication.translate("targetwidget", u"0.00 Mib/s", None))
#if QT_CONFIG(tooltip)
        self.label_time_cpu.setToolTip(QCoreApplication.translate("targetwidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">CPU time</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(without verification)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_time_cpu.setText(QCoreApplication.translate("targetwidget", u"0.00 s", None))
#if QT_CONFIG(tooltip)
        self.label_time.setToolTip(QCoreApplication.translate("targetwidget", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Progress time</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(without verification)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_time.setText(QCoreApplication.translate("targetwidget", u"0.00 s", None))
#if QT_CONFIG(tooltip)
        self.label_sticksize.setToolTip(QCoreApplication.translate("targetwidget", u"USB stick size", None))
#endif // QT_CONFIG(tooltip)
        self.label_sticksize.setText(QCoreApplication.translate("targetwidget", u"0 GB", None))
#if QT_CONFIG(tooltip)
        self.pushButton_stop.setToolTip(QCoreApplication.translate("targetwidget", u"Stop", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_start.setToolTip(QCoreApplication.translate("targetwidget", u"Start", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.comboBox_buffers.setToolTip(QCoreApplication.translate("targetwidget", u"Write buffer", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

