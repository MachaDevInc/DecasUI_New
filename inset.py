# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inset.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow7(object):
    def setupUi(self, MainWindow7):
        MainWindow7.setObjectName("MainWindow7")
        MainWindow7.resize(1024, 600)
        MainWindow7.setIconSize(QtCore.QSize(100, 100))
        self.centralwidget = QtWidgets.QWidget(MainWindow7)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("/home/decas/ui/DecasUI_New/pics/Standby.png"))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(100, 320, 200, 50))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(410, 320, 200, 50))
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(780, 320, 200, 50))
        self.label_7.setScaledContents(False)
        self.label_7.setObjectName("label_7")
        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(40, 430, 100, 100))
        self.back.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pics/1 (400 × 400 px).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon)
        self.back.setIconSize(QtCore.QSize(90, 90))
        self.back.setCheckable(False)
        self.back.setAutoDefault(False)
        self.back.setDefault(False)
        self.back.setFlat(True)
        self.back.setObjectName("back")
        self.wifi = QtWidgets.QPushButton(self.centralwidget)
        self.wifi.setGeometry(QtCore.QRect(150, 190, 100, 100))
        self.wifi.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pics/1 (90 × 90 px) (5).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.wifi.setIcon(icon1)
        self.wifi.setIconSize(QtCore.QSize(100, 100))
        self.wifi.setFlat(True)
        self.wifi.setObjectName("wifi")
        self.rs = QtWidgets.QPushButton(self.centralwidget)
        self.rs.setGeometry(QtCore.QRect(470, 190, 100, 100))
        self.rs.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pics/1 (90 × 90 px) (4).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rs.setIcon(icon2)
        self.rs.setIconSize(QtCore.QSize(100, 100))
        self.rs.setFlat(True)
        self.rs.setObjectName("rs")
        self.usb = QtWidgets.QPushButton(self.centralwidget)
        self.usb.setGeometry(QtCore.QRect(770, 190, 100, 100))
        self.usb.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("pics/1 (90 × 90 px) (6).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.usb.setIcon(icon3)
        self.usb.setIconSize(QtCore.QSize(100, 100))
        self.usb.setFlat(True)
        self.usb.setObjectName("usb")
        self.about = QtWidgets.QPushButton(self.centralwidget)
        self.about.setGeometry(QtCore.QRect(849, 440, 100, 100))
        self.about.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("pics/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.about.setIcon(icon4)
        self.about.setIconSize(QtCore.QSize(200, 200))
        self.about.setFlat(True)
        self.about.setObjectName("about")
        self.label.raise_()
        self.label_4.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.wifi.raise_()
        self.rs.raise_()
        self.usb.raise_()
        self.back.raise_()
        self.about.raise_()
        MainWindow7.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow7)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        MainWindow7.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow7)
        self.statusbar.setObjectName("statusbar")
        MainWindow7.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow7)
        QtCore.QMetaObject.connectSlotsByName(MainWindow7)

    def retranslateUi(self, MainWindow7):
        _translate = QtCore.QCoreApplication.translate
        MainWindow7.setWindowTitle(_translate("MainWindow7", "MainWindow"))
        self.label_4.setText(_translate("MainWindow7", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Wifi Setting</span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow7", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">RS485/232</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow7", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">USB</span></p></body></html>"))
