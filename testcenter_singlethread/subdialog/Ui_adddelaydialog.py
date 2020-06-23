# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\adddelaydialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddDelayDialog(object):
    def setupUi(self, AddDelayDialog):
        AddDelayDialog.setObjectName("AddDelayDialog")
        AddDelayDialog.resize(400, 159)
        AddDelayDialog.setSizeGripEnabled(True)
        self.label = QtWidgets.QLabel(AddDelayDialog)
        self.label.setGeometry(QtCore.QRect(20, 50, 131, 16))
        self.label.setObjectName("label")
        self.lineEdit_delayTime = QtWidgets.QLineEdit(AddDelayDialog)
        self.lineEdit_delayTime.setGeometry(QtCore.QRect(20, 70, 321, 20))
        self.lineEdit_delayTime.setObjectName("lineEdit_delayTime")
        self.pushButton_cancel = QtWidgets.QPushButton(AddDelayDialog)
        self.pushButton_cancel.setGeometry(QtCore.QRect(50, 110, 75, 23))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_addDelayTime = QtWidgets.QPushButton(AddDelayDialog)
        self.pushButton_addDelayTime.setGeometry(QtCore.QRect(200, 110, 75, 23))
        self.pushButton_addDelayTime.setObjectName("pushButton_addDelayTime")

        self.retranslateUi(AddDelayDialog)
        QtCore.QMetaObject.connectSlotsByName(AddDelayDialog)

    def retranslateUi(self, AddDelayDialog):
        _translate = QtCore.QCoreApplication.translate
        AddDelayDialog.setWindowTitle(_translate("AddDelayDialog", "Dialog"))
        self.label.setText(_translate("AddDelayDialog", "请输入延时时间（s）："))
        self.pushButton_cancel.setText(_translate("AddDelayDialog", "取消"))
        self.pushButton_addDelayTime.setText(_translate("AddDelayDialog", "确定"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddDelayDialog = QtWidgets.QDialog()
    ui = Ui_AddDelayDialog()
    ui.setupUi(AddDelayDialog)
    AddDelayDialog.show()
    sys.exit(app.exec_())

