# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\Testcenter\testcenter_singlethread\subdialog\loganalyzer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_loganalyzer(object):
    def setupUi(self, loganalyzer):
        loganalyzer.setObjectName("loganalyzer")
        loganalyzer.resize(400, 567)
        self.lineEdit_logpath = QtWidgets.QLineEdit(loganalyzer)
        self.lineEdit_logpath.setGeometry(QtCore.QRect(100, 20, 231, 20))
        self.lineEdit_logpath.setObjectName("lineEdit_logpath")
        self.label = QtWidgets.QLabel(loganalyzer)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 20))
        self.label.setObjectName("label")
        self.selectpath = QtWidgets.QPushButton(loganalyzer)
        self.selectpath.setGeometry(QtCore.QRect(330, 20, 51, 20))
        self.selectpath.setObjectName("selectpath")
        self.lineEdit_searchchar = QtWidgets.QLineEdit(loganalyzer)
        self.lineEdit_searchchar.setGeometry(QtCore.QRect(10, 89, 371, 21))
        self.lineEdit_searchchar.setObjectName("lineEdit_searchchar")
        self.label_3 = QtWidgets.QLabel(loganalyzer)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 341, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(loganalyzer)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 171, 20))
        self.label_4.setObjectName("label_4")
        self.lineEdit_saveline = QtWidgets.QLineEdit(loganalyzer)
        self.lineEdit_saveline.setGeometry(QtCore.QRect(190, 130, 191, 20))
        self.lineEdit_saveline.setObjectName("lineEdit_saveline")
        self.label_5 = QtWidgets.QLabel(loganalyzer)
        self.label_5.setGeometry(QtCore.QRect(10, 160, 91, 20))
        self.label_5.setObjectName("label_5")
        self.selectsavepath = QtWidgets.QPushButton(loganalyzer)
        self.selectsavepath.setGeometry(QtCore.QRect(340, 160, 51, 20))
        self.selectsavepath.setObjectName("selectsavepath")
        self.lineEdit_savepath = QtWidgets.QLineEdit(loganalyzer)
        self.lineEdit_savepath.setGeometry(QtCore.QRect(100, 160, 231, 20))
        self.lineEdit_savepath.setObjectName("lineEdit_savepath")
        self.groupBox = QtWidgets.QGroupBox(loganalyzer)
        self.groupBox.setGeometry(QtCore.QRect(0, 50, 401, 181))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.pushButton_gen = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_gen.setGeometry(QtCore.QRect(300, 150, 75, 23))
        self.pushButton_gen.setObjectName("pushButton_gen")
        self.groupBox_2 = QtWidgets.QGroupBox(loganalyzer)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 240, 401, 311))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget.setGeometry(QtCore.QRect(10, 20, 381, 81))
        self.listWidget.setFrameShape(QtWidgets.QFrame.HLine)
        self.listWidget.setLayoutMode(QtWidgets.QListView.Batched)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        item.setFont(font)
        self.listWidget.addItem(item)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 100, 381, 101))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 5, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(True)
        self.addColumn = QtWidgets.QPushButton(self.groupBox_2)
        self.addColumn.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.addColumn.setObjectName("addColumn")
        self.deleteColumn = QtWidgets.QPushButton(self.groupBox_2)
        self.deleteColumn.setGeometry(QtCore.QRect(120, 210, 75, 23))
        self.deleteColumn.setObjectName("deleteColumn")
        self.selectsavepath_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.selectsavepath_2.setGeometry(QtCore.QRect(340, 250, 51, 20))
        self.selectsavepath_2.setObjectName("selectsavepath_2")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(10, 250, 101, 20))
        self.label_6.setObjectName("label_6")
        self.lineEdit_savepath_2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_savepath_2.setGeometry(QtCore.QRect(120, 250, 211, 20))
        self.lineEdit_savepath_2.setObjectName("lineEdit_savepath_2")
        self.pushButton_gen_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_gen_2.setGeometry(QtCore.QRect(300, 280, 75, 23))
        self.pushButton_gen_2.setObjectName("pushButton_gen_2")
        self.groupBox.raise_()
        self.groupBox_2.raise_()
        self.lineEdit_logpath.raise_()
        self.label.raise_()
        self.selectpath.raise_()
        self.lineEdit_searchchar.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.lineEdit_saveline.raise_()
        self.label_5.raise_()
        self.selectsavepath.raise_()
        self.lineEdit_savepath.raise_()

        self.retranslateUi(loganalyzer)
        self.listWidget.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(loganalyzer)

    def retranslateUi(self, loganalyzer):
        _translate = QtCore.QCoreApplication.translate
        loganalyzer.setWindowTitle(_translate("loganalyzer", "log分析器"))
        self.lineEdit_logpath.setText(_translate("loganalyzer", "D:\\test2\\123.log"))
        self.label.setText(_translate("loganalyzer", "log文件路径*："))
        self.selectpath.setText(_translate("loganalyzer", "选择"))
        self.lineEdit_searchchar.setText(_translate("loganalyzer", "EYE\\(L,R,U,D\\)"))
        self.label_3.setText(_translate("loganalyzer", "要查找的文字(括号为特殊字符之前需要加反斜杆)*："))
        self.label_4.setText(_translate("loganalyzer", "提取查找到文字的后面第几行："))
        self.lineEdit_saveline.setText(_translate("loganalyzer", "0,1,2,3,4"))
        self.label_5.setText(_translate("loganalyzer", "保存log到路径："))
        self.selectsavepath.setText(_translate("loganalyzer", "选择"))
        self.lineEdit_savepath.setText(_translate("loganalyzer", "D:\\test2\\"))
        self.groupBox.setTitle(_translate("loganalyzer", "提取并保存为文本："))
        self.pushButton_gen.setText(_translate("loganalyzer", "开始生成"))
        self.groupBox_2.setTitle(_translate("loganalyzer", "提取并保存为excel："))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("loganalyzer", "列名"))
        item = self.listWidget.item(1)
        item.setText(_translate("loganalyzer", "要匹配的字段"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("loganalyzer", "匹配值"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("loganalyzer", "列名；要匹配的字段"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("loganalyzer", "列名；要匹配的字段"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("loganalyzer", "列名；要匹配的字段"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("loganalyzer", "列名；要匹配的字段"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("loganalyzer", "列名；要匹配的字段"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("loganalyzer", "列名；要匹配的字段"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("loganalyzer", "SLOTID；physical slotid:(\\d\\d)"))
        item = self.tableWidget.item(0, 1)
        item.setText(_translate("loganalyzer", "地址；Address = (\"0x\"+\\w\\w)"))
        item = self.tableWidget.item(0, 2)
        item.setText(_translate("loganalyzer", "L；\"1*  1*\"+\".*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,\"+\" 0     \"+(\\w*)"))
        item = self.tableWidget.item(0, 3)
        item.setText(_translate("loganalyzer", "R；\"1*  1*\"+\".*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,\"+\" 0     \"+\\w*,(\\w*)"))
        item = self.tableWidget.item(0, 4)
        item.setText(_translate("loganalyzer", "U；\"1*  1*\"+\".*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,\"+\" 0     \"(\\w*,\\w*,(\\w*),\\w*"))
        item = self.tableWidget.item(0, 5)
        item.setText(_translate("loganalyzer", "D；\"1*  1*\"+\".*,.*,.*,.*,.*,.*,.*,.*,.*,.*,.*,\"+\" 0     \"+\\w*,\\w*,\\w*,(\\w*)"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.addColumn.setText(_translate("loganalyzer", "添加列"))
        self.deleteColumn.setText(_translate("loganalyzer", "删除列"))
        self.selectsavepath_2.setText(_translate("loganalyzer", "选择"))
        self.label_6.setText(_translate("loganalyzer", "保存excel到路径："))
        self.lineEdit_savepath_2.setText(_translate("loganalyzer", "D:\\test2\\"))
        self.pushButton_gen_2.setText(_translate("loganalyzer", "开始生成"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    loganalyzer = QtWidgets.QWidget()
    ui = Ui_loganalyzer()
    ui.setupUi(loganalyzer)
    loganalyzer.show()
    sys.exit(app.exec_())

