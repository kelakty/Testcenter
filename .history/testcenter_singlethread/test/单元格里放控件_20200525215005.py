# -*- coding: utf-8 -*-

'''
    【简介】
	PyQT5中 单元格里面放控件

'''

import sys
from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QTableWidgetItem, QAbstractItemView,
                             QComboBox, QPushButton)


class Table(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QTableWidget 例子")
        self.resize(430, 300)
        conLayout = QHBoxLayout()  # 创建水平布局文件
        tableWidget = QTableWidget()  # 创建一个列表
        tableWidget.setRowCount(4)  # 设置行数
        tableWidget.setColumnCount(3)  # 设置列数
        conLayout.addWidget(tableWidget)  # 添加列表到布局

        tableWidget.setHorizontalHeaderLabels(['姓名', '性别', '体重(kg)'])  # 设置水平表头

        newItem = QTableWidgetItem("张三")  # 添加张三 到（0，0）
        tableWidget.setItem(0, 0, newItem)

        comBox = QComboBox()  # 新建一个下拉组件
        comBox.addItem("男")
        comBox.addItem("女")
        comBox.setStyleSheet("QComboBox{margin:3px};")
        comBox.currentIndexChanged.connect(self.comboxSelect) #绑定combox select 事件
        tableWidget.setCellWidget(0, 1, comBox)  # 添加下拉组件到列表（0，1）

        searchBtn = QPushButton("修改")  # 新建一个按钮
        searchBtn.setDown(True)
        searchBtn.setStyleSheet("QPushButton{margin:3px};")
        searchBtn.clicked.connect(self.butClick) #绑定按钮点击事件
        tableWidget.setCellWidget(0, 2, searchBtn)  # 添加按钮到列表（0，2）

        self.setLayout(conLayout)

    def comboxSelect(self,index):
        print("combox select index",index)

    def butClick(self):
        print("button click")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = Table()
    example.show()
    sys.exit(app.exec_())
