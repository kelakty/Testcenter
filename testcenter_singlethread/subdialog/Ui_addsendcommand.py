# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5 - 副本\subdialog\addsendcommand.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_addsendcommandandwaitingtecho(object):
    def setupUi(self, addsendcommandandwaitingtecho):
        addsendcommandandwaitingtecho.setObjectName("addsendcommandandwaitingtecho")
        addsendcommandandwaitingtecho.resize(412, 235)
        self.pushButton_addTestCommand = QtWidgets.QPushButton(addsendcommandandwaitingtecho)
        self.pushButton_addTestCommand.setGeometry(QtCore.QRect(250, 200, 101, 23))
        self.pushButton_addTestCommand.setObjectName("pushButton_addTestCommand")
        self.checkBox_clearbufferlog = QtWidgets.QCheckBox(addsendcommandandwaitingtecho)
        self.checkBox_clearbufferlog.setGeometry(QtCore.QRect(240, 160, 151, 16))
        self.checkBox_clearbufferlog.setChecked(True)
        self.checkBox_clearbufferlog.setObjectName("checkBox_clearbufferlog")
        self.label_5 = QtWidgets.QLabel(addsendcommandandwaitingtecho)
        self.label_5.setGeometry(QtCore.QRect(10, 140, 54, 12))
        self.label_5.setObjectName("label_5")
        self.plainTextEdit_comment = QtWidgets.QPlainTextEdit(addsendcommandandwaitingtecho)
        self.plainTextEdit_comment.setGeometry(QtCore.QRect(40, 140, 181, 91))
        self.plainTextEdit_comment.setObjectName("plainTextEdit_comment")
        self.widget = QtWidgets.QWidget(addsendcommandandwaitingtecho)
        self.widget.setGeometry(QtCore.QRect(10, 10, 61, 121))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.widget1 = QtWidgets.QWidget(addsendcommandandwaitingtecho)
        self.widget1.setGeometry(QtCore.QRect(70, 10, 331, 121))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEditSendCommand = QtWidgets.QLineEdit(self.widget1)
        self.lineEditSendCommand.setObjectName("lineEditSendCommand")
        self.verticalLayout_2.addWidget(self.lineEditSendCommand)
        self.lineEdit_delaytime = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit_delaytime.setObjectName("lineEdit_delaytime")
        self.verticalLayout_2.addWidget(self.lineEdit_delaytime)
        self.lineEdit_checkechostring = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit_checkechostring.setWhatsThis("")
        self.lineEdit_checkechostring.setObjectName("lineEdit_checkechostring")
        self.verticalLayout_2.addWidget(self.lineEdit_checkechostring)
        self.lineEdit_Instructions = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit_Instructions.setObjectName("lineEdit_Instructions")
        self.verticalLayout_2.addWidget(self.lineEdit_Instructions)

        self.retranslateUi(addsendcommandandwaitingtecho)
        QtCore.QMetaObject.connectSlotsByName(addsendcommandandwaitingtecho)

    def retranslateUi(self, addsendcommandandwaitingtecho):
        _translate = QtCore.QCoreApplication.translate
        addsendcommandandwaitingtecho.setWindowTitle(_translate("addsendcommandandwaitingtecho", "发送命令并等待回显"))
        self.pushButton_addTestCommand.setText(_translate("addsendcommandandwaitingtecho", "添加到测试序列"))
        self.checkBox_clearbufferlog.setToolTip(_translate("addsendcommandandwaitingtecho", "为该项测试单独缓存的log，用于匹配回显。测试结束无需再匹配本次log时建议清空"))
        self.checkBox_clearbufferlog.setText(_translate("addsendcommandandwaitingtecho", "结束测试后清空缓存log"))
        self.label_5.setText(_translate("addsendcommandandwaitingtecho", "备注："))
        self.label.setText(_translate("addsendcommandandwaitingtecho", "发送命令："))
        self.label_2.setText(_translate("addsendcommandandwaitingtecho", "超时时间："))
        self.label_3.setToolTip(_translate("addsendcommandandwaitingtecho", "支持正则"))
        self.label_3.setText(_translate("addsendcommandandwaitingtecho", "期待回显："))
        self.label_4.setText(_translate("addsendcommandandwaitingtecho", "命令说明："))
        self.lineEditSendCommand.setToolTip(_translate("addsendcommandandwaitingtecho", "发送给对端的命令，如果需要发送回车换行，请加上\\r\\n等回车换行字符"))
        self.lineEdit_delaytime.setToolTip(_translate("addsendcommandandwaitingtecho", "发送命令后等待对端回显的时间"))
        self.lineEdit_checkechostring.setToolTip(_translate("addsendcommandandwaitingtecho", "在此输入发送命令后期望对端返回的特定字符。支持正则表达式匹配字符"))

