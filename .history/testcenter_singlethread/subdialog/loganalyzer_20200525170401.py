# -*- coding: utf-8 -*-

"""
Module implementing LogAnalyzer.
"""

from PyQt5.QtCore import pyqtSlot,QStandardPaths
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
import re

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

    def logextract(self):
        """
        打开log文件 匹配要查找的字符并 提取查找到文字的后面第几行

        """
        #打开log文件
        logfilepath=self.lineEdit_logpath.text()
        logfilepathname=logfilepath.replace("\\","/")
        openlogfile=open(logfilepathname,encoding='UTF-8')
        #with open('lumberjack.txt','w') as openlogfile:


        #生成要保存的log文件 替换原文件名带日期时间
        date = datetime.now().date()   #- timedelta(days=1)
        time=datetime.now().time()
        savefilepathname=self.logfilepathname.replace('.log', '')
        savefilepathname=self.logfilepathname.replace('.txt', '')
        savefilepathname+="_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
        savelogfile=open(savefilepathname,'a+')

        #匹配log
        searchchar = self.lineEdit_searchchar.Text()
        re_searchchar=re.compile(searchchar)
        while True:
            data=openlogfile.readline()
            if not data:
                getdata.write()
                break
            find1=re_searchchar.findall(data)

            if find1!=[]:
                warntemp,shutdowntemp,currenttemp=find1[0]
                
          
                exceldata=exceldata.append([{'timestamp':timestamp[0],'airinlet':TempID1,'board':TempID2,'switch':TempID3}], ignore_index=True)
           
        openlogfile.close()
        savelogfile.close()



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
            break
    
        
        #匹配要查找的字符


        #保存需要的log文件到文本


        
