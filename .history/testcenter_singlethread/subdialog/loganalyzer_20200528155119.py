# -*- coding: utf-8 -*-

"""
Module implementing LogAnalyzer.
"""

from PyQt5.QtCore import pyqtSlot,QStandardPaths,Qt
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
import re
import os,sys
from datetime import datetime, timedelta

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
        self.setWindowFlags(self.windowFlags() | Qt.Dialog)  #重要！让窗口置顶显示
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

    def logextracttolog(self):
        """
        打开log文件 匹配要查找的字符并 提取查找到文字的后面第几行

        """
        #打开log文件
        logfilepath=self.lineEdit_logpath.text()
        self.logfilepathname=logfilepath.replace("\\","/")
        openlogfile=open(self.logfilepathname,encoding='UTF-8')
        #with open('lumberjack.txt','w') as openlogfile:

        #生成要保存的log文件 替换原文件名带日期时间
        date = datetime.now().date()   #- timedelta(days=1)
        time=datetime.now().time()
        self.savefilepathname=self.logfilepathname.replace('.log', '')
        self.savefilepathname=self.logfilepathname.replace('.txt', '')
        self.savefilepathname+="_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second)+".log"
        savelogfile=open(self.savefilepathname,'a+')

        #提取查找到文字的后面第几行： lineEdit_saveline
        savelinenum=self.lineEdit_saveline.text().split(',')
        savelinenum.sort() 
        print("savelinenum:",savelinenum)
        maximumlinenum=savelinenum[-1]
        print("maximumlinenum:",maximumlinenum)

        #匹配log
        searchchar =  self.lineEdit_searchchar.text()  #"EYE\(L,R,U,D\)"
        re_searchchar=re.compile(searchchar)
        while True:
            data=openlogfile.readline()
            if not data:
                savelogfile.write(data)
                break
            find1=re_searchchar.findall(data)
            
            if find1 != []:
                #保存匹配到的那一行
                print("有匹配到文字")
                savelogfile.write(data)
                for i in range(int(maximumlinenum)):
                    data=openlogfile.readline() # 暂时不支持向上查找保存
                    for j in savelinenum:
                        if i+1 == int(j):
                            savelogfile.write(data)
                        
        openlogfile.close()
        savelogfile.close()



    @pyqtSlot()
    def on_selectpath_clicked(self):
        """
        Slot documentation goes here.
        """
        self.chooselogfile()

    @pyqtSlot()
    def on_selectsavepath_clicked(self):
        """
        Slot documentation goes here.
        """
        self.choosesavedir()
    
    @pyqtSlot()
    def on_pushButton_gen_clicked(self):
        """
        匹配要查找的字符并保存需要的log文本到文件
        """
        #判断文本框中是否都有填写了
        if self.lineEdit_logpath.text() == "" or self.lineEdit_savepath.text() == "" or self.lineEdit_searchchar.text() == "":
            QMessageBox.information(self,'警告','请填入所有内容',QMessageBox.Ok) 
            return
        #匹配要查找的字符
        self.logextracttolog()

