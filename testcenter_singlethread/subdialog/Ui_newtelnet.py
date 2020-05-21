# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\Testcenter\testcenter_singlethread\subdialog\newtelnet.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewTelnet(object):
    def setupUi(self, NewTelnet):
        NewTelnet.setObjectName("NewTelnet")
        NewTelnet.resize(319, 100)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewTelnet)
        self.buttonBox.setGeometry(QtCore.QRect(-40, 50, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.telnethost = QtWidgets.QLineEdit(NewTelnet)
        self.telnethost.setGeometry(QtCore.QRect(60, 20, 131, 20))
        self.telnethost.setObjectName("telnethost")
        self.label = QtWidgets.QLabel(NewTelnet)
        self.label.setGeometry(QtCore.QRect(10, 20, 54, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(NewTelnet)
        self.label_2.setGeometry(QtCore.QRect(200, 20, 54, 20))
        self.label_2.setObjectName("label_2")
        self.telnetport = QtWidgets.QLineEdit(NewTelnet)
        self.telnetport.setGeometry(QtCore.QRect(230, 20, 71, 20))
        self.telnetport.setObjectName("telnetport")

        self.retranslateUi(NewTelnet)
        self.buttonBox.accepted.connect(NewTelnet.accept)
        self.buttonBox.rejected.connect(NewTelnet.reject)
        QtCore.QMetaObject.connectSlotsByName(NewTelnet)

    def retranslateUi(self, NewTelnet):
        _translate = QtCore.QCoreApplication.translate
        NewTelnet.setWindowTitle(_translate("NewTelnet", "新建Telnet连接"))
        self.label.setText(_translate("NewTelnet", "Telnet:"))
        self.label_2.setText(_translate("NewTelnet", "Port:"))

