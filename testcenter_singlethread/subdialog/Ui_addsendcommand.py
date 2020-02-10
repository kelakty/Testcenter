# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\addsendcommand.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 144)
        Dialog.setSizeGripEnabled(True)
        self.pushButton_addTestCommand = QtWidgets.QPushButton(Dialog)
        self.pushButton_addTestCommand.setGeometry(QtCore.QRect(200, 90, 101, 23))
        self.pushButton_addTestCommand.setObjectName("pushButton_addTestCommand")
        self.lineEditSendCommand = QtWidgets.QLineEdit(Dialog)
        self.lineEditSendCommand.setGeometry(QtCore.QRect(70, 40, 321, 21))
        self.lineEditSendCommand.setObjectName("lineEditSendCommand")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.label.setObjectName("label")
        self.pushButton_editSendCommand_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_editSendCommand_cancel.setGeometry(QtCore.QRect(90, 90, 75, 23))
        self.pushButton_editSendCommand_cancel.setObjectName("pushButton_editSendCommand_cancel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.lineEditSendCommand, self.pushButton_addTestCommand)
        Dialog.setTabOrder(self.pushButton_addTestCommand, self.pushButton_editSendCommand_cancel)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_addTestCommand.setText(_translate("Dialog", "添加到测试序列"))
        self.label.setText(_translate("Dialog", "发送命令："))
        self.pushButton_editSendCommand_cancel.setText(_translate("Dialog", "取消"))

