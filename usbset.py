# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'usbset.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_usbsetting(object):
    def setupUi(self, usbsetting):
        usbsetting.setObjectName("usbsetting")
        usbsetting.resize(1024, 600)
        self.centralwidget = QtWidgets.QWidget(usbsetting)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("/home/decas/ui/DecasUI_New/pics/Standby.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 180, 200, 50))
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.done3 = QtWidgets.QPushButton(self.centralwidget)
        self.done3.setGeometry(QtCore.QRect(780, 430, 200, 100))
        self.done3.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pics/2234.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.done3.setIcon(icon)
        self.done3.setIconSize(QtCore.QSize(200, 200))
        self.done3.setFlat(True)
        self.done3.setObjectName("done3")
        self.back = QtWidgets.QPushButton(self.centralwidget)
        self.back.setGeometry(QtCore.QRect(40, 430, 200, 100))
        self.back.setAutoFillBackground(False)
        self.back.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("pics/1 (400 × 400 px).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.back.setIcon(icon1)
        self.back.setIconSize(QtCore.QSize(200, 200))
        self.back.setFlat(True)
        self.back.setObjectName("back")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(440, 50, 200, 50))
        self.label_5.setObjectName("label_5")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(360, 180, 300, 50))
        self.textEdit.setObjectName("textEdit")
        self.COM = QtWidgets.QPushButton(self.centralwidget)
        self.COM.setGeometry(QtCore.QRect(360, 180, 300, 50))
        self.COM.setText("")
        self.COM.setFlat(True)
        self.COM.setObjectName("COM")
        usbsetting.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(usbsetting)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        usbsetting.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(usbsetting)
        self.statusbar.setObjectName("statusbar")
        usbsetting.setStatusBar(self.statusbar)

        self.retranslateUi(usbsetting)
        QtCore.QMetaObject.connectSlotsByName(usbsetting)

    def retranslateUi(self, usbsetting):
        _translate = QtCore.QCoreApplication.translate
        usbsetting.setWindowTitle(_translate("usbsetting", "MainWindow"))
        self.label_2.setText(_translate("usbsetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">COM Port</span></p></body></html>"))
        self.label_5.setText(_translate("usbsetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">USB Setting</span></p></body></html>"))
