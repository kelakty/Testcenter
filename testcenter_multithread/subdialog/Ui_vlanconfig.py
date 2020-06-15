# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\subdialog\vlanconfig.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VlanConfig(object):
    def setupUi(self, VlanConfig):
        VlanConfig.setObjectName("VlanConfig")
        VlanConfig.resize(315, 235)
        VlanConfig.setSizeGripEnabled(True)
        self.com_num = QtWidgets.QLineEdit(VlanConfig)
        self.com_num.setGeometry(QtCore.QRect(130, 40, 113, 20))
        self.com_num.setObjectName("com_num")
        self.first_vlan = QtWidgets.QLineEdit(VlanConfig)
        self.first_vlan.setGeometry(QtCore.QRect(130, 160, 113, 20))
        self.first_vlan.setObjectName("first_vlan")
        self.com_type = QtWidgets.QLineEdit(VlanConfig)
        self.com_type.setGeometry(QtCore.QRect(130, 80, 113, 20))
        self.com_type.setObjectName("com_type")
        self.slot_num = QtWidgets.QLineEdit(VlanConfig)
        self.slot_num.setGeometry(QtCore.QRect(130, 120, 113, 20))
        self.slot_num.setObjectName("slot_num")
        self.layoutWidget = QtWidgets.QWidget(VlanConfig)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 30, 86, 161))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.cancel = QtWidgets.QPushButton(VlanConfig)
        self.cancel.setGeometry(QtCore.QRect(40, 200, 75, 23))
        self.cancel.setObjectName("cancel")
        self.auto_gen = QtWidgets.QPushButton(VlanConfig)
        self.auto_gen.setGeometry(QtCore.QRect(160, 200, 75, 23))
        self.auto_gen.setObjectName("auto_gen")
        self.com_num.raise_()
        self.com_type.raise_()
        self.slot_num.raise_()
        self.layoutWidget.raise_()
        self.cancel.raise_()
        self.auto_gen.raise_()
        self.first_vlan.raise_()

        self.retranslateUi(VlanConfig)
        QtCore.QMetaObject.connectSlotsByName(VlanConfig)
        VlanConfig.setTabOrder(self.com_num, self.com_type)
        VlanConfig.setTabOrder(self.com_type, self.slot_num)
        VlanConfig.setTabOrder(self.slot_num, self.first_vlan)
        VlanConfig.setTabOrder(self.first_vlan, self.auto_gen)
        VlanConfig.setTabOrder(self.auto_gen, self.cancel)

    def retranslateUi(self, VlanConfig):
        _translate = QtCore.QCoreApplication.translate
        VlanConfig.setWindowTitle(_translate("VlanConfig", "vlan配置"))
        self.com_num.setText(_translate("VlanConfig", "48"))
        self.first_vlan.setText(_translate("VlanConfig", "2"))
        self.com_type.setText(_translate("VlanConfig", "gi"))
        self.slot_num.setText(_translate("VlanConfig", "0"))
        self.label.setText(_translate("VlanConfig", "端口数："))
        self.label_2.setText(_translate("VlanConfig", "端口类型："))
        self.label_3.setText(_translate("VlanConfig", "槽位号："))
        self.label_4.setText(_translate("VlanConfig", "vlan起始编号："))
        self.cancel.setText(_translate("VlanConfig", "取消"))
        self.auto_gen.setText(_translate("VlanConfig", "自动生成"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VlanConfig = QtWidgets.QDialog()
    ui = Ui_VlanConfig()
    ui.setupUi(VlanConfig)
    VlanConfig.show()
    sys.exit(app.exec_())

