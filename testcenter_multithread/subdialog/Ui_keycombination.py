# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\Testcenter\testcenter_singlethread\subdialog\keycombination.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_keycombination(object):
    def setupUi(self, keycombination):
        keycombination.setObjectName("keycombination")
        keycombination.resize(292, 94)
        self.ctrlC = QtWidgets.QPushButton(keycombination)
        self.ctrlC.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.ctrlC.setObjectName("ctrlC")
        self.ctrlZ = QtWidgets.QPushButton(keycombination)
        self.ctrlZ.setGeometry(QtCore.QRect(100, 50, 75, 23))
        self.ctrlZ.setObjectName("ctrlZ")
        self.ctrlT = QtWidgets.QPushButton(keycombination)
        self.ctrlT.setGeometry(QtCore.QRect(20, 50, 75, 23))
        self.ctrlT.setObjectName("ctrlT")
        self.ctrlU = QtWidgets.QPushButton(keycombination)
        self.ctrlU.setGeometry(QtCore.QRect(180, 20, 75, 23))
        self.ctrlU.setObjectName("ctrlU")
        self.ctrlB = QtWidgets.QPushButton(keycombination)
        self.ctrlB.setGeometry(QtCore.QRect(100, 20, 75, 23))
        self.ctrlB.setObjectName("ctrlB")
        self.ctrlA = QtWidgets.QPushButton(keycombination)
        self.ctrlA.setGeometry(QtCore.QRect(180, 50, 75, 23))
        self.ctrlA.setObjectName("ctrlA")

        self.retranslateUi(keycombination)
        QtCore.QMetaObject.connectSlotsByName(keycombination)

    def retranslateUi(self, keycombination):
        _translate = QtCore.QCoreApplication.translate
        keycombination.setWindowTitle(_translate("keycombination", "Dialog"))
        self.ctrlC.setText(_translate("keycombination", "Ctrl+C"))
        self.ctrlZ.setText(_translate("keycombination", "Ctrl+Z"))
        self.ctrlT.setText(_translate("keycombination", "Ctrl+T"))
        self.ctrlU.setText(_translate("keycombination", "Ctrl+U"))
        self.ctrlB.setText(_translate("keycombination", "Ctrl+B"))
        self.ctrlA.setText(_translate("keycombination", "Ctrl+A"))

