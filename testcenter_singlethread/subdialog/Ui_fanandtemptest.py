# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\fanandtemptest.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fanandtemp_test(object):
    def setupUi(self, fanandtemp_test):
        fanandtemp_test.setObjectName("fanandtemp_test")
        fanandtemp_test.resize(408, 152)
        self.lineEdit_logfile = QtWidgets.QLineEdit(fanandtemp_test)
        self.lineEdit_logfile.setGeometry(QtCore.QRect(20, 30, 241, 21))
        self.lineEdit_logfile.setObjectName("lineEdit_logfile")
        self.pushButton_selectlog = QtWidgets.QPushButton(fanandtemp_test)
        self.pushButton_selectlog.setGeometry(QtCore.QRect(280, 30, 75, 23))
        self.pushButton_selectlog.setObjectName("pushButton_selectlog")
        self.label = QtWidgets.QLabel(fanandtemp_test)
        self.label.setGeometry(QtCore.QRect(20, 10, 111, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(fanandtemp_test)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 191, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_savedir = QtWidgets.QLineEdit(fanandtemp_test)
        self.lineEdit_savedir.setGeometry(QtCore.QRect(20, 80, 241, 20))
        self.lineEdit_savedir.setObjectName("lineEdit_savedir")
        self.pushButton_selectsavedir = QtWidgets.QPushButton(fanandtemp_test)
        self.pushButton_selectsavedir.setGeometry(QtCore.QRect(280, 80, 75, 23))
        self.pushButton_selectsavedir.setObjectName("pushButton_selectsavedir")
        self.pushButton_startgenerate = QtWidgets.QPushButton(fanandtemp_test)
        self.pushButton_startgenerate.setGeometry(QtCore.QRect(130, 110, 91, 23))
        self.pushButton_startgenerate.setObjectName("pushButton_startgenerate")

        self.retranslateUi(fanandtemp_test)
        QtCore.QMetaObject.connectSlotsByName(fanandtemp_test)

    def retranslateUi(self, fanandtemp_test):
        _translate = QtCore.QCoreApplication.translate
        fanandtemp_test.setWindowTitle(_translate("fanandtemp_test", "风扇转速与温度提取"))
        self.pushButton_selectlog.setText(_translate("fanandtemp_test", "选择"))
        self.label.setText(_translate("fanandtemp_test", "请选择拷机log文件："))
        self.label_2.setText(_translate("fanandtemp_test", "请选择生成表格位置："))
        self.pushButton_selectsavedir.setText(_translate("fanandtemp_test", "选择"))
        self.pushButton_startgenerate.setText(_translate("fanandtemp_test", "开始合成Excel"))

