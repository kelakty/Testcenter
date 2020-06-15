# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\registerbaselinecheck.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RegisterBaseLineCheck(object):
    def setupUi(self, RegisterBaseLineCheck):
        RegisterBaseLineCheck.setObjectName("RegisterBaseLineCheck")
        RegisterBaseLineCheck.resize(494, 122)
        self.pushButton_browse_RBL_dir = QtWidgets.QPushButton(RegisterBaseLineCheck)
        self.pushButton_browse_RBL_dir.setGeometry(QtCore.QRect(370, 40, 75, 23))
        self.pushButton_browse_RBL_dir.setObjectName("pushButton_browse_RBL_dir")
        self.lineEdit_register_base_line_dir = QtWidgets.QLineEdit(RegisterBaseLineCheck)
        self.lineEdit_register_base_line_dir.setGeometry(QtCore.QRect(20, 40, 341, 21))
        self.lineEdit_register_base_line_dir.setObjectName("lineEdit_register_base_line_dir")
        self.label = QtWidgets.QLabel(RegisterBaseLineCheck)
        self.label.setGeometry(QtCore.QRect(20, 20, 171, 16))
        self.label.setObjectName("label")
        self.startRegisterBaseLine_Test = QtWidgets.QPushButton(RegisterBaseLineCheck)
        self.startRegisterBaseLine_Test.setGeometry(QtCore.QRect(60, 80, 75, 23))
        self.startRegisterBaseLine_Test.setObjectName("startRegisterBaseLine_Test")
        self.generateRegisterBaseLineReport = QtWidgets.QPushButton(RegisterBaseLineCheck)
        self.generateRegisterBaseLineReport.setGeometry(QtCore.QRect(180, 80, 75, 23))
        self.generateRegisterBaseLineReport.setObjectName("generateRegisterBaseLineReport")
        self.pushButton = QtWidgets.QPushButton(RegisterBaseLineCheck)
        self.pushButton.setGeometry(QtCore.QRect(300, 80, 111, 23))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(RegisterBaseLineCheck)
        QtCore.QMetaObject.connectSlotsByName(RegisterBaseLineCheck)

    def retranslateUi(self, RegisterBaseLineCheck):
        _translate = QtCore.QCoreApplication.translate
        RegisterBaseLineCheck.setWindowTitle(_translate("RegisterBaseLineCheck", "Form"))
        self.pushButton_browse_RBL_dir.setText(_translate("RegisterBaseLineCheck", "browse"))
        self.label.setText(_translate("RegisterBaseLineCheck", "请选择寄存器基线文件路径："))
        self.startRegisterBaseLine_Test.setText(_translate("RegisterBaseLineCheck", "开始测试"))
        self.generateRegisterBaseLineReport.setText(_translate("RegisterBaseLineCheck", "生成报告"))
        self.pushButton.setText(_translate("RegisterBaseLineCheck", "使用报告直接比对"))

