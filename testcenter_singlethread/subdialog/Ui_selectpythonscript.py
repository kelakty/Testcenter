# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5 - 副本\subdialog\selectpythonscript.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form_selectpythonscript(object):
    def setupUi(self, form_selectpythonscript):
        form_selectpythonscript.setObjectName("form_selectpythonscript")
        form_selectpythonscript.resize(400, 110)
        self.label = QtWidgets.QLabel(form_selectpythonscript)
        self.label.setGeometry(QtCore.QRect(20, 30, 151, 16))
        self.label.setObjectName("label")
        self.lineEdit_selectpythonscript = QtWidgets.QLineEdit(form_selectpythonscript)
        self.lineEdit_selectpythonscript.setGeometry(QtCore.QRect(20, 50, 271, 21))
        self.lineEdit_selectpythonscript.setObjectName("lineEdit_selectpythonscript")
        self.pushButton_selectpythonscript = QtWidgets.QPushButton(form_selectpythonscript)
        self.pushButton_selectpythonscript.setGeometry(QtCore.QRect(300, 50, 81, 23))
        self.pushButton_selectpythonscript.setObjectName("pushButton_selectpythonscript")
        self.pushButton_runscript = QtWidgets.QPushButton(form_selectpythonscript)
        self.pushButton_runscript.setGeometry(QtCore.QRect(140, 80, 75, 23))
        self.pushButton_runscript.setObjectName("pushButton_runscript")

        self.retranslateUi(form_selectpythonscript)
        QtCore.QMetaObject.connectSlotsByName(form_selectpythonscript)

    def retranslateUi(self, form_selectpythonscript):
        _translate = QtCore.QCoreApplication.translate
        form_selectpythonscript.setWindowTitle(_translate("form_selectpythonscript", "选择python脚本文件"))
        self.label.setText(_translate("form_selectpythonscript", "请选择要运行的脚本文件："))
        self.pushButton_selectpythonscript.setText(_translate("form_selectpythonscript", "选择脚本文件"))
        self.pushButton_runscript.setText(_translate("form_selectpythonscript", "运行脚本"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form_selectpythonscript = QtWidgets.QWidget()
    ui = Ui_form_selectpythonscript()
    ui.setupUi(form_selectpythonscript)
    form_selectpythonscript.show()
    sys.exit(app.exec_())

