# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\addquickcommand.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddQuickCommand(object):
    def setupUi(self, AddQuickCommand):
        AddQuickCommand.setObjectName("AddQuickCommand")
        AddQuickCommand.resize(310, 148)
        AddQuickCommand.setSizeGripEnabled(True)
        self.pushButton_confirm = QtWidgets.QPushButton(AddQuickCommand)
        self.pushButton_confirm.setGeometry(QtCore.QRect(100, 110, 75, 23))
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.lineEdit_quickcommand = QtWidgets.QLineEdit(AddQuickCommand)
        self.lineEdit_quickcommand.setGeometry(QtCore.QRect(20, 80, 261, 21))
        self.lineEdit_quickcommand.setObjectName("lineEdit_quickcommand")
        self.label = QtWidgets.QLabel(AddQuickCommand)
        self.label.setGeometry(QtCore.QRect(20, 60, 171, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddQuickCommand)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 61, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_commandname = QtWidgets.QLineEdit(AddQuickCommand)
        self.lineEdit_commandname.setGeometry(QtCore.QRect(20, 30, 261, 20))
        self.lineEdit_commandname.setObjectName("lineEdit_commandname")

        self.retranslateUi(AddQuickCommand)
        QtCore.QMetaObject.connectSlotsByName(AddQuickCommand)
        AddQuickCommand.setTabOrder(self.lineEdit_commandname, self.lineEdit_quickcommand)
        AddQuickCommand.setTabOrder(self.lineEdit_quickcommand, self.pushButton_confirm)

    def retranslateUi(self, AddQuickCommand):
        _translate = QtCore.QCoreApplication.translate
        AddQuickCommand.setWindowTitle(_translate("AddQuickCommand", "Dialog"))
        self.pushButton_confirm.setText(_translate("AddQuickCommand", "确定"))
        self.label.setText(_translate("AddQuickCommand", "请在下方输入快速发送字符串："))
        self.label_2.setText(_translate("AddQuickCommand", "标签命名："))

