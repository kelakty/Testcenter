# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\characterrecognition.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogCharacterRecognition(object):
    def setupUi(self, DialogCharacterRecognition):
        DialogCharacterRecognition.setObjectName("DialogCharacterRecognition")
        DialogCharacterRecognition.resize(415, 162)
        DialogCharacterRecognition.setSizeGripEnabled(True)
        self.pushButton_addTest = QtWidgets.QPushButton(DialogCharacterRecognition)
        self.pushButton_addTest.setGeometry(QtCore.QRect(210, 130, 101, 23))
        self.pushButton_addTest.setObjectName("pushButton_addTest")
        self.label = QtWidgets.QLabel(DialogCharacterRecognition)
        self.label.setGeometry(QtCore.QRect(10, 20, 201, 16))
        self.label.setObjectName("label")
        self.pushButton_cancel = QtWidgets.QPushButton(DialogCharacterRecognition)
        self.pushButton_cancel.setGeometry(QtCore.QRect(100, 130, 75, 23))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.layoutWidget = QtWidgets.QWidget(DialogCharacterRecognition)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 40, 391, 48))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.radioButton = QtWidgets.QRadioButton(DialogCharacterRecognition)
        self.radioButton.setGeometry(QtCore.QRect(100, 100, 89, 16))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(DialogCharacterRecognition)
        self.radioButton_2.setGeometry(QtCore.QRect(220, 100, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(DialogCharacterRecognition)
        QtCore.QMetaObject.connectSlotsByName(DialogCharacterRecognition)
        DialogCharacterRecognition.setTabOrder(self.lineEdit, self.lineEdit_2)
        DialogCharacterRecognition.setTabOrder(self.lineEdit_2, self.pushButton_addTest)
        DialogCharacterRecognition.setTabOrder(self.pushButton_addTest, self.pushButton_cancel)

    def retranslateUi(self, DialogCharacterRecognition):
        _translate = QtCore.QCoreApplication.translate
        DialogCharacterRecognition.setWindowTitle(_translate("DialogCharacterRecognition", "Dialog"))
        self.pushButton_addTest.setText(_translate("DialogCharacterRecognition", "添加到测试序列"))
        self.label.setText(_translate("DialogCharacterRecognition", "请在下方输入需要识别的字符："))
        self.pushButton_cancel.setText(_translate("DialogCharacterRecognition", "取消"))
        self.label_2.setText(_translate("DialogCharacterRecognition", "包括："))
        self.label_3.setText(_translate("DialogCharacterRecognition", "不包括："))
        self.radioButton.setText(_translate("DialogCharacterRecognition", "包括则PASS"))
        self.radioButton_2.setText(_translate("DialogCharacterRecognition", "包括则FAIL"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogCharacterRecognition = QtWidgets.QDialog()
    ui = Ui_DialogCharacterRecognition()
    ui.setupUi(DialogCharacterRecognition)
    DialogCharacterRecognition.show()
    sys.exit(app.exec_())

