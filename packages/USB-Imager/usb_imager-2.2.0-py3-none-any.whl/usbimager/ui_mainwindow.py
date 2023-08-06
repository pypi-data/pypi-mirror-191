# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowQhnDnu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 500)
        MainWindow.setMinimumSize(QSize(450, 0))
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAboutQt = QAction(MainWindow)
        self.actionAboutQt.setObjectName(u"actionAboutQt")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_select_all = QCheckBox(self.centralwidget)
        self.checkBox_select_all.setObjectName(u"checkBox_select_all")
        self.checkBox_select_all.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_select_all)

        self.checkBox_verify_all = QCheckBox(self.centralwidget)
        self.checkBox_verify_all.setObjectName(u"checkBox_verify_all")

        self.horizontalLayout_2.addWidget(self.checkBox_verify_all)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.toolButton_menu = QToolButton(self.centralwidget)
        self.toolButton_menu.setObjectName(u"toolButton_menu")
        icon = QIcon()
        iconThemeName = u"help-about-symbolic"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u"../../../../../../.designer/backup", QSize(), QIcon.Normal, QIcon.Off)
        
        self.toolButton_menu.setIcon(icon)
        self.toolButton_menu.setPopupMode(QToolButton.InstantPopup)
        self.toolButton_menu.setToolButtonStyle(Qt.ToolButtonFollowStyle)

        self.horizontalLayout_2.addWidget(self.toolButton_menu)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 484, 16))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout_targets = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_targets.setSpacing(12)
        self.verticalLayout_targets.setObjectName(u"verticalLayout_targets")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_open = QPushButton(self.centralwidget)
        self.pushButton_open.setObjectName(u"pushButton_open")
        icon1 = QIcon()
        iconThemeName = u"document-open"
        if QIcon.hasThemeIcon(iconThemeName):
            icon1 = QIcon.fromTheme(iconThemeName)
        else:
            icon1.addFile(u"../../../../../../.designer/backup", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_open.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.pushButton_open)

        self.label_imagename = QLabel(self.centralwidget)
        self.label_imagename.setObjectName(u"label_imagename")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_imagename.sizePolicy().hasHeightForWidth())
        self.label_imagename.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label_imagename)

        self.label_imagesize = QLabel(self.centralwidget)
        self.label_imagesize.setObjectName(u"label_imagesize")
        self.label_imagesize.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label_imagesize)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.progressbar_all = QProgressBar(self.centralwidget)
        self.progressbar_all.setObjectName(u"progressbar_all")
        self.progressbar_all.setValue(0)

        self.horizontalLayout_5.addWidget(self.progressbar_all)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_stop_all = QPushButton(self.centralwidget)
        self.pushButton_stop_all.setObjectName(u"pushButton_stop_all")
        icon2 = QIcon()
        iconThemeName = u"media-playback-stop"
        if QIcon.hasThemeIcon(iconThemeName):
            icon2 = QIcon.fromTheme(iconThemeName)
        else:
            icon2.addFile(u"../../../../../../.designer/backup", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_stop_all.setIcon(icon2)

        self.horizontalLayout.addWidget(self.pushButton_stop_all)

        self.pushButton_start_all = QPushButton(self.centralwidget)
        self.pushButton_start_all.setObjectName(u"pushButton_start_all")
        icon3 = QIcon()
        iconThemeName = u"media-playback-start"
        if QIcon.hasThemeIcon(iconThemeName):
            icon3 = QIcon.fromTheme(iconThemeName)
        else:
            icon3.addFile(u"../../../../../../.designer/backup", QSize(), QIcon.Normal, QIcon.Off)
        
        self.pushButton_start_all.setIcon(icon3)

        self.horizontalLayout.addWidget(self.pushButton_start_all)


        self.horizontalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 30))
        self.menubar.setLayoutDirection(Qt.RightToLeft)
        self.menuInfo = QMenu(self.menubar)
        self.menuInfo.setObjectName(u"menuInfo")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuInfo.menuAction())
        self.menuInfo.addAction(self.actionAbout)
        self.menuInfo.addAction(self.actionAboutQt)

        self.retranslateUi(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionAboutQt.setText(QCoreApplication.translate("MainWindow", u"About Qt", None))
#if QT_CONFIG(tooltip)
        self.checkBox_select_all.setToolTip(QCoreApplication.translate("MainWindow", u"Select all USB sticks for writing", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_select_all.setText(QCoreApplication.translate("MainWindow", u"Select all", None))
#if QT_CONFIG(tooltip)
        self.checkBox_verify_all.setToolTip(QCoreApplication.translate("MainWindow", u"Select all USB sticks for validation", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_verify_all.setText(QCoreApplication.translate("MainWindow", u"Verify all", None))
#if QT_CONFIG(tooltip)
        self.toolButton_menu.setToolTip(QCoreApplication.translate("MainWindow", u"About", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_open.setToolTip(QCoreApplication.translate("MainWindow", u"Open image", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_open.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.label_imagename.setToolTip(QCoreApplication.translate("MainWindow", u"Image name", None))
#endif // QT_CONFIG(tooltip)
        self.label_imagename.setText(QCoreApplication.translate("MainWindow", u"No image", None))
#if QT_CONFIG(tooltip)
        self.label_imagesize.setToolTip(QCoreApplication.translate("MainWindow", u"Image size", None))
#endif // QT_CONFIG(tooltip)
        self.label_imagesize.setText(QCoreApplication.translate("MainWindow", u"0 GB", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Total:", None))
#if QT_CONFIG(tooltip)
        self.progressbar_all.setToolTip(QCoreApplication.translate("MainWindow", u"Total progress", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_stop_all.setToolTip(QCoreApplication.translate("MainWindow", u"Stop all", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_start_all.setToolTip(QCoreApplication.translate("MainWindow", u"Start all", None))
#endif // QT_CONFIG(tooltip)
        self.menuInfo.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
    # retranslateUi

