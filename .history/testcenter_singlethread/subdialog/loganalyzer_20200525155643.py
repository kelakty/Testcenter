# -*- coding: utf-8 -*-

"""
Module implementing LogAnalyzer.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox

from .Ui_loganalyzer import Ui_loganalyzer


class LogAnalyzer(QWidget, Ui_loganalyzer):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(LogAnalyzer, self).__init__(parent)
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window

    def chooselogfile(self):
        # fileName, path = QFileDialog.getOpenFileName(self, "Open File",QCoreApplication.applicationDirPath())
        # print(QStandardPaths.standardLocations(0))
        # print(QStandardPaths.standardLocations(0)[0])

        #选择单个待测Baseline的excel文件。如果使用的是QFileDialog.getOpenFileNames则可以同时选择多个文件
        choosefilename, _ = QFileDialog.getOpenFileName(self, "选取log文件",QStandardPaths.standardLocations(0)[0],
                            "Text Files (*.txt *.log);;All Files (*)")
        # print(choosefilename)
        if choosefilename:
            self.lineEdit_logpath.setText(choosefilename) 

    def choosesavedir(self):
        choosedir = QFileDialog.getExistingDirectory(self, "选取文件夹", os.getcwd()) 
            
        if choosedir:
            self.lineEdit_savepath.setText(choosedir)   

    @pyqtSlot()
    def on_selectpath_clicked(self):
        """
        Slot documentation goes here.
        """
        self.chooselogfile

    @pyqtSlot()
    def on_selectsavepath_clicked(self):
        """
        Slot documentation goes here.
        """
        self.choosesavedir
    
    @pyqtSlot()
    def on_pushButton_gen_clicked(self):
        """
        匹配要查找的字符并保存需要的log文本到文件
        """
        #判断文本框中是否都有填写了
        if self.lineEdit_logpath == None or self.lineEdit_savepath == None or self.lineEdit_searchchar == None:
            QMessageBox.information('警告','寄存器基线值行数与实际读出值行数不同，请修改',QMessageBox.Ok) 
        #匹配要查找的字符

        #保存需要的log文件到文本


        
