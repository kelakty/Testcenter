# -*- coding: utf-8 -*-

"""
Module implementing FanAndTempTest.
"""

from PyQt5.QtCore import pyqtSlot,QDir,QCoreApplication,QStandardPaths
from PyQt5.QtWidgets import QWidget,QFileDialog
import os,sys
from subdialog.Ui_fanandtemptest import Ui_fanandtemp_test
import re
import pandas as pd

encodingType='utf-8'
class FanAndTempTest(QWidget, Ui_fanandtemp_test):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(FanAndTempTest, self).__init__(parent)
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
            self.lineEdit_logfile.setText(choosefilename) 

    def choosesavedir(self):
        choosedir = QFileDialog.getExistingDirectory(self, "选取文件夹", os.getcwd()) 
            
        if choosedir:
            self.lineEdit_savedir.setText(choosedir)    

    def fanandtemp_extract(self):
        baocun="C:\\Users\\seeker\\Desktop\\result.txt"
        file=baocun.replace("\\","/")
        f2=open(file,'a+')

        # yuandizhi=r"D:\自动化开发资料\SelfTestScript\48GT.log"
        yuandizhi=self.lineEdit_logfile.text()
        dizhi=yuandizhi.replace("\\","/")
        fo=open(dizhi,encoding='UTF-8')

        exceldata=pd.DataFrame(columns=['timestamp','airinlet','board','switch','fanspeed1','fanspeed2'])
        #提取行首时间
        reg_timestamp=r'[0-9]{2}.[0-9]{2}\s+(\d\d:\d\d:\d\d)'
        re_timestamp=re.compile(reg_timestamp)
        #提取单行中温度值
        # reg_temp_air_inlet=r'air_inlet\s+(N/A|\d\d*)\s+(N/A|\d\d*)\s+(N/A|\d\d*)'
        reg_temp_air_inlet=r'air_inlet \s+(N/A|\d\d*) \s+(N/A|\d\d*) \s+(N/A|\d\d*)'
        re_temp_air_inlet=re.compile(reg_temp_air_inlet)
        reg_temp_board=r'board\s+(N/A|\d\d*)\s+(N/A|\d\d*)\s+(N/A|\d\d*)'
        re_temp_board=re.compile(reg_temp_board)
        #reg_temp_board2=r'board \s+(N/A|\d\d*) \s+(N/A|\d\d*) \s+(N/A|\d\d*)'
        reg_temp_switch=r'switch \s+(N/A|\d\d*) \s+(N/A|\d\d*) \s+(N/A|\d\d*)'
        re_temp_switch=re.compile(reg_temp_switch)

        #提取单行中的风扇转速
        reg_fan_speed1=r'1 \s+ok \s+([0-9]{1,4})\s+[0-9]{1,3}'
        re_fan_speed1=re.compile(reg_fan_speed1)
        reg_fan_speed2=r'1 \s+ok \s+([0-9]{1,4})\s+[0-9]{1,3}'
        re_fan_speed2=re.compile(reg_fan_speed2)

        #reg_alltemporfan=(reg_temp_air_inlet) | (reg_temp_board)  | (reg_temp_switch) | (reg_fan_speed1) | (reg_fan_speed2)
        reg_alltemporfan=r'(air_inlet\s+(N/A|\d\d*)\s+(N/A|\d\d*)\s+(N/A|\d\d*)) | (board\s+(N/A|\d\d*)\s+(N/A|\d\d*)\s+(N/A|\d\d*))'
        re_alltemporfan=re.compile(reg_alltemporfan)
        fanID=0
        boardTID=0
        TempID1=''
        TempID2=''
        TempID3=''
        fanspeed1=''
        fanspeed2=''
        while True:
            data=fo.readline()
            if not data:
                exceldata.to_csv(self.lineEdit_savedir.text()+"\data.csv")
                # exceldata.to_csv('D:\自动化开发资料\SelfTestScript\data.csv')   # 保存到磁盘
                break
            # find=re_alltemporfan.findall(data)
            # if find !=[]:
            #     print(find)
            #     print(data)
            find1=re_temp_air_inlet.findall(data)
            find2=re_temp_board.findall(data)
            find3=re_temp_switch.findall(data)
            find4=re_fan_speed1.findall(data)

            if find1!=[]:
                warntemp,shutdowntemp,currenttemp=find1[0]
                TempID1=currenttemp
                # print(find[0])
                # print(currenttemp)
                timestamp=re_timestamp.findall(data)
                # print(timestamp)
                # exceldata=exceldata.append([{'timestamp':timestamp[0],'airinlet':currenttemp}], ignore_index=True)   #保存温度数据到表格
                # print(exceldata)
            if find2!=[]:
                warntemp,shutdowntemp,currenttemp=find2[0]
                timestamp=re_timestamp.findall(data)   #保存温度数据到表格
                if boardTID==0:
                    TempID2=currenttemp
                    # exceldata=exceldata.append([{'timestamp':timestamp[0],'board':currenttemp}], ignore_index=True)
                    boardTID+=1
                else :
                    boardTID=0
            if find3!=[]:
                warntemp,shutdowntemp,currenttemp=find3[0]
                TempID3=currenttemp
                timestamp=re_timestamp.findall(data)   #保存温度数据到表格
                exceldata=exceldata.append([{'timestamp':timestamp[0],'airinlet':TempID1,'board':TempID2,'switch':TempID3}], ignore_index=True)
            if find4!=[]:
                # print(find4)
                timestamp=re_timestamp.findall(data)   #保存温度数据到表格
                if fanID==0:
                    fanspeed1=find4[0]
                    # exceldata=exceldata.append([{'timestamp':timestamp[0],'fanspeed1':find4[0]}], ignore_index=True)
                    fanID+=1
                else :
                    fanspeed2=find4[0]
                    exceldata=exceldata.append([{'timestamp':timestamp[0],'fanspeed1':fanspeed1,'fanspeed2':fanspeed2}], ignore_index=True)
                    fanID=0
        fo.close()
        f2.close()

    @pyqtSlot()
    def on_pushButton_selectlog_clicked(self):
        """
        Slot documentation goes here.
        """
        self.chooselogfile()
    
    @pyqtSlot()
    def on_pushButton_selectsavedir_clicked(self):
        """
        Slot documentation goes here.
        """
        self.choosesavedir()
    
    @pyqtSlot()
    def on_pushButton_startgenerate_clicked(self):
        """
        Slot documentation goes here.
        """
        self.fanandtemp_extract()

