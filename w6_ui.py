# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\DecasUI\DecasUI_V2\w6.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow6(object):
    def setupUi(self, MainWindow6):
        MainWindow6.setObjectName("MainWindow6")
        MainWindow6.resize(1024, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow6)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 1024, 571))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("d:\\DecasUI\\DecasUI_V2\\/home/decas/ui/DecasUI_New/pics/Standby.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setOpenExternalLinks(False)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 350, 600, 60))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 410, 600, 60))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 470, 600, 60))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(310, 0, 400, 400))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("d:\\DecasUI\\DecasUI_V2\\/home/decas/ui/DecasUI_New/pics/Decas_Logo.png"))
        self.label_5.setObjectName("label_5")
        MainWindow6.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow6)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        MainWindow6.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow6)
        self.statusbar.setObjectName("statusbar")
        MainWindow6.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow6)

    def retranslateUi(self, MainWindow6):
        _translate = QtCore.QCoreApplication.translate
        MainWindow6.setWindowTitle(_translate("MainWindow6", "MainWindow"))
        self.label.setText(_translate("MainWindow6", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Receipt Sent Successfully</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow6", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">Thanks for choosing.</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow6", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt; font-weight:600;\">RESPSLIPS</span></p></body></html>"))
