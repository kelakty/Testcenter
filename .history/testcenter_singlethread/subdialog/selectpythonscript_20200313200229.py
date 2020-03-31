# -*- coding: utf-8 -*-

"""
Module implementing selectpythonscript.
"""

from PyQt5.QtCore import pyqtSlot,QMetaObject,Qt,QGenericArgument,QThread
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,QDir,QCoreApplication,QStandardPaths,QByteArray 
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
import os
from globalvariable import GlobalVariable
from AutomationScript import CRT
from .Ui_selectpythonscript import Ui_form_selectpythonscript
from serial_thread import SerialThread
import threading
encodingType=GlobalVariable.defaultEncodingType

class selectpythonscript(QWidget, Ui_form_selectpythonscript):
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(selectpythonscript, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Dialog)
        self.get_filename=''
        

    def setMain(self, main_window):
        self.mainwindow=main_window

    def brosescriptdir(self):
        #选择单个脚本文件。如果使用的是QFileDialog.getOpenFileNames则可以同时选择多个文件
        choosefilename, _ = QFileDialog.getOpenFileName(self, "选取文件",QStandardPaths.standardLocations(0)[0],
                            "pythonscript Files (*.py *.txt);;All Files (*)")
        # print(choosefilename)
        if choosefilename:
            self.lineEdit_selectpythonscript.setText(choosefilename) 
            self.get_filename=self.lineEdit_selectpythonscript.text()
        else:
            self.get_filename=''

    @pyqtSlot()
    def on_pushButton_selectpythonscript_clicked(self):
        """
        Slot documentation goes here.
        """
        self.brosescriptdir()
    
    @pyqtSlot()
    def on_pushButton_runscript_clicked(self):
        """
        Slot documentation goes here.
        """
        # num1=100
        # num2=200
        # print("self.mainwindow.crt的对象为：",self.mainwindow.crt)

        print("getfilename is :",self.get_filename)
        # self.get_filename=self.get_filename.replace('/','\\')
        # print("getfilename is :",self.get_filename)
        # command="python "+self.get_filename+" "+"%s"+" "+"%s"
        # print('待测python文件命令为：',command)

        # results=os.system(command % (num1,self.mainwindow.crt))
        # print('执行python文件命令结果为：',results)
        
        f = open(self.get_filename,'rb')
        for script_command in f.readlines():
            count+=1
            exec(script_command)

        # exec(open(self.get_filename,'rb').read())

        #以下为临时测试脚本功能
        """
        self.CRT = CRT()
        self.CRT.Send("abc\r\n")
        print("开始运行testautoscript脚本")
        print('%-25s: %s, %s,' % ("selectscipt_win_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("selectscipt_win_slot", threading.current_thread().name, threading.current_thread().ident))

        # QMetaObject.invokeMethod(self.mainwindow.newthread, "sendto_comdata_slot", Qt.QueuedConnection, QtCore.Q_ARG(int, progress))

        results=self.CRT.SendAndWaitString("sh ver\r\n",1,"aBc",CompileFlag="IGNORECASE",EmptyBuffer=1)
        print("运行结果为：",results)
        results=self.CRT.SendAndWaitString("sh ver detail\r\n",1,"description",CompileFlag="IGNORECASE",EmptyBuffer=1)
        print("运行结果为：",results)
        results=self.CRT.SendAndWaitString("sh in st\r\n",1,"duplex",CompileFlag="IGNORECASE",EmptyBuffer=1)
        print("运行结果为：",results)
        results=self.CRT.SendAndWaitString("sh pow\r\n",1,"Invalid",CompileFlag="IGNORECASE",EmptyBuffer=1)
        print("运行结果为：",results)
        results=self.CRT.SendAndWaitString("sh manu\r\n",1,"Location",CompileFlag="IGNORECASE",EmptyBuffer=1)
        print("运行结果为：",results)
        print("结束运行testautoscript脚本")
        """