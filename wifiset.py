# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wifiset.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wifisetting(object):
    def setupUi(self, wifisetting):
        wifisetting.setObjectName("wifisetting")
        wifisetting.resize(1024, 600)
        self.centralwidget = QtWidgets.QWidget(wifisetting)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("/home/decas/ui/DecasUI_New/pics/Standby.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.done = QtWidgets.QPushButton(self.centralwidget)
        self.done.setGeometry(QtCore.QRect(780, 430, 200, 100))
        self.done.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pics/2234.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.done.setIcon(icon)
        self.done.setIconSize(QtCore.QSize(200, 200))
        self.done.setFlat(True)
        self.done.setObjectName("done")
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
        self.textEdit = QtWidgets.QTextBrowser(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(360, 180, 300, 50))
        self.textEdit.setObjectName("textEdit")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(420, 50, 200, 50))
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 180, 200, 50))
        self.label_2.setScaledContents(True)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 270, 200, 50))
        self.label_3.setScaledContents(True)
        self.label_3.setWordWrap(False)
        self.label_3.setObjectName("label_3")
        self.textEdit1 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textEdit1.setGeometry(QtCore.QRect(360, 270, 300, 50))
        self.textEdit1.setObjectName("textEdit1")
        self.connection = QtWidgets.QPushButton(self.centralwidget)
        self.connection.setGeometry(QtCore.QRect(360, 180, 300, 50))
        self.connection.setText("")
        self.connection.setShortcut("")
        self.connection.setFlat(True)
        self.connection.setObjectName("connection")
        self.password = QtWidgets.QPushButton(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(360, 270, 300, 50))
        self.password.setText("")
        self.password.setFlat(True)
        self.password.setObjectName("password")
        wifisetting.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(wifisetting)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        wifisetting.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(wifisetting)
        self.statusbar.setObjectName("statusbar")
        wifisetting.setStatusBar(self.statusbar)

        self.retranslateUi(wifisetting)
        QtCore.QMetaObject.connectSlotsByName(wifisetting)

    def retranslateUi(self, wifisetting):
        _translate = QtCore.QCoreApplication.translate
        wifisetting.setWindowTitle(_translate("wifisetting", "MainWindow"))
        self.label_5.setText(_translate("wifisetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Wifi Setting</span></p></body></html>"))
        self.label_2.setText(_translate("wifisetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Connection</span></p></body></html>"))
        self.label_3.setText(_translate("wifisetting", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Password</span></p></body></html>"))
