# -*- coding: utf-8 -*-

"""
Module implementing LogAnalyzer.
"""

from PyQt5.QtCore import pyqtSlot,QStandardPaths,Qt
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
from PyQt5 import QtWidgets
import re
import os,sys
from datetime import datetime, timedelta
import pandas as pd

from Ui_loganalyzer import Ui_loganalyzer


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
    
    def logextracttoexcel(self):
        """
        打开log文件 根据表格设置的匹配规则匹配log填入表格
        """
        #打开log文件
        logfilepath=self.lineEdit_logpath.text()
        self.logfilepathname=logfilepath.replace("\\","/")
        openlogfile=open(self.logfilepathname,encoding='UTF-8')
        #with open('lumberjack.txt','w') as openlogfile:

        #生成要保存的excel文件名带日期时间
        date = datetime.now().date()  
        time=datetime.now().time()
        self.savefilepathname=self.logfilepathname.replace('.log', '')
        self.savefilepathname=self.logfilepathname.replace('.txt', '')
        self.savefilepathname+="_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second)+".csv"
        

        #生成表格的列名
        for i in range(self.tableWidget.columnCount()):
            pass
        exceldata=pd.DataFrame(columns=['SLOTID','Address',"EYE"]) 
        exceldata=pd.DataFrame(columns=["L"]) 
        exceldata=exceldata.append([{'SLOTID':1,'Address':1,"EYE":1}], ignore_index=True) 
        print("exceldata是：",exceldata)
        exceldata.to_csv(self.savefilepathname)

        #编译所需的正则表达式
        SLOTID = 'physical slotid:( ?\d\d ?)'
        Address = 'Address = ( ?0x\w\w)'
        EYE = "16, 68,16, 0, 0, 0     ( ?\d+),( ?\d+),( ?\d+),( ?\d+)"
        re_SLOTID = re.compile(SLOTID)
        re_Address = re.compile(Address)
        re_EYE = re.compile(EYE)

        #开始匹配正则算法



        while False:
            data=openlogfile.readline()
            if not data:
                exceldata.to_csv(self.savefilepathname)
                # exceldata.to_csv('D:\自动化开发资料\SelfTestScript\data.csv')   # 保存到磁盘
                break
            if re_SLOTID.findall(data) != []:
                find1 = re_SLOTID.findall(data)
                print("找到SLOTID是：",find1)

                #开始往找到SLOTID的地方继续向下查找address
                while True:
                    data=openlogfile.readline()
                    if not data:
                        exceldata.to_csv(self.savefilepathname)
                        # exceldata.to_csv('D:\自动化开发资料\SelfTestScript\data.csv')   # 保存到磁盘
                        break
                    if re_SLOTID.findall(data) != [] or re_Address.findall(data) != []:
                        #如果找到新的SLOTID则保存新的slotID，如果没有找到新的，则按旧的slotID进行保存
                        if re_SLOTID.findall(data) != []:
                            find1 = re_SLOTID.findall(data)
                        if re_Address.findall(data) != []:
                            find2 = re_Address.findall(data)
                            print("找到Address是：",find2)
                        #开始往找到Address的地方继续向下查找EYE
                        while True:
                            data=openlogfile.readline()
                            if not data:
                                exceldata.to_csv(self.savefilepathname)
                                # exceldata.to_csv('D:\自动化开发资料\SelfTestScript\data.csv')   # 保存到磁盘
                                break
                            if re_EYE.findall(data) != [] or re_Address.findall(data) != []:
                                if re_Address.findall(data) != []:
                                    find2 = re_Address.findall(data)
                                if re_EYE.findall(data) != []:
                                    find3 = re_EYE.findall(data)
                                    exceldata=exceldata.append([{'SLOTID':find1[0],'Address':find2[0],"EYE":find3[0]}], ignore_index=True) 
                                    #开始往找到EYE的地方继续向下查找 EYE
                                    for i in range(3):
                                        data=openlogfile.readline()
                                        if not data:
                                            exceldata.to_csv(self.savefilepathname)
                                            # exceldata.to_csv('D:\自动化开发资料\SelfTestScript\data.csv')   # 保存到磁盘
                                            break
                                        if re_EYE.findall(data) != []:
                                            find3=re_EYE.findall(data)
                                            print("下面第%d 行找到EYE是：%s" % (i,find3))
                                            print("该行log是：",data)
                                            
                                            exceldata=exceldata.append([{'SLOTID':find1[0],'Address':find2[0],"EYE":find3[0]}], ignore_index=True) #'L':find3[0],'R':find3[0],'U':find3[0],'D':find3[0]
                                            # print("exceldata是：",exceldata)
                                            exceldata.to_csv(self.savefilepathname)
                                break

        openlogfile.close()

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
    def on_addColumn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tableWidget.insertColumn(self.tableWidget.columnCount())
    
    @pyqtSlot()
    def on_deleteColumn_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tableWidget.removeColumn(self.tableWidget.currentColumn())

    
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
    
    @pyqtSlot()
    def on_pushButton_gen_2_clicked(self):
        """
        匹配要查找的字符并保存需要的log文本到excel文件
        """
        self.tablelist = [[0 for i in range(self.tableWidget.rowCount())] for j in range(self.tableWidget.columnCount())]
        print(self.tablelist)

        #判断表格至少有一列信息，每列信息完整，否则返回错误提示

        # 读取表格信息
        print("表格列行数：",self.tableWidget.columnCount(), self.tableWidget.rowCount())
        for i in range(self.tableWidget.columnCount()):
            for j in range(self.tableWidget.rowCount()):
                print("表格内容",self.tableWidget.item(j,i).text())
                self.tablelist[i][j] = self.tableWidget.item(j,i).text()
        


        #匹配要查找的字符
        self.logextracttoexcel()

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # loganalyzer = QtWidgets.QWidget()
    LogAnalyzer = LogAnalyzer()
    LogAnalyzer.show()
    sys.exit(app.exec_())
    