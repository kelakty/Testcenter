# -*- coding: utf-8 -*-

"""
Module implementing AddQuickCommand.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets,QtCore
from globalvariable import GlobalVariable
import os
from .Ui_addquickcommand import Ui_AddQuickCommand
from functools import partial

class AddQuickCommand(QDialog, Ui_AddQuickCommand):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AddQuickCommand, self).__init__(parent)
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window

    def addquickcommand(self):
        quickcommand = self.lineEdit_quickcommand.text()
        print("新添加quickcommand命令是:",quickcommand)
        GlobalVariable.mainwindow.textEdit_message.insertPlainText("新添加quickcommand命令是:" % quickcommand) #TODO 不知道是否正确
        if quickcommand != "":     #此处用None并不能真正的拦截输入为空
            # self.quickcommand = QtWidgets.QAction(MainWindow)
            print("准备添加quickcommand命令是:",quickcommand)
            GlobalVariable.quickcommand_list.append(quickcommand)  #先将命令存入列表
            GlobalVariable.quickcommand_namelist.append(self.lineEdit_commandname.text())  
            print("按下添加快速命令确认按钮")
            createaction_command="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+" = QtWidgets.QAction()"
            exec(createaction_command)
            setobjectname_command="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+".setObjectName(\"action"+str(GlobalVariable.quickcommand_number+1)+ "\")"
            exec(setobjectname_command)
            toolbar_addaction="self.mainwindow.toolBar_quickcommand.addAction(self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+")"
            exec(toolbar_addaction)
            toolbar_settext="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+".setText(QtCore.QCoreApplication.translate(\"MainWindow\",\""+GlobalVariable.quickcommand_namelist[len(GlobalVariable.quickcommand_namelist)-1]+"\"))"
            exec(toolbar_settext)
            
            # self.mainwindow.actionshow_manu = QtWidgets.QAction()
            # self.mainwindow.actionshow_manu.setObjectName("actionshow_manu")
            # self.mainwindow.toolBar_quickcommand.addAction(self.mainwindow.actionshow_manu)
            # self.mainwindow.actionshow_manu.setText(QtCore.QCoreApplication.translate("MainWindow", quickcommand))
            # self.mainwindow.actionshow_manu.triggered.connect(partial(self.mainwindow.actiontoolbar_sendcommand_triggered,quickcommand))
            
            toolbar_command_trigger="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+".triggered.connect(partial(self.mainwindow.actiontoolbar_sendcommand_triggered,GlobalVariable.quickcommand_list[len(GlobalVariable.quickcommand_list)-1]))"
            # toolbar_command_trigger="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+".triggered.connect(partial(self.mainwindow.actiontoolbar_sendcommand_triggered,self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+"))"
            exec(toolbar_command_trigger)

            #创建一个hover的事件，用于后面的选中删除该按钮。传递的是一个action对象
            # toolbar_hoveraction="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+".hovered.connect(partial(self.mainwindow.action_hoverd,GlobalVariable.quickcommand_list["+str(GlobalVariable.quickcommand_number)+"]))"
            toolbar_hoveraction="self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+".hovered.connect(partial(self.mainwindow.action_hoverd,self.mainwindow.action"+str(GlobalVariable.quickcommand_number+1)+"))"
            exec(toolbar_hoveraction)       

            #保存以上配置命令,需要将所有的配置命令添加到列表中
            GlobalVariable.quickcommand_setting_list.append([createaction_command,setobjectname_command,toolbar_addaction,toolbar_settext,toolbar_command_trigger,toolbar_hoveraction])
            
            print("global_quickcommand_setting_list:",GlobalVariable.quickcommand_setting_list)
            print(str(GlobalVariable.quickcommand_number))

            #实时保存到配置文件中
            print("list[num]:",GlobalVariable.quickcommand_setting_list[GlobalVariable.quickcommand_number])
            print("list[num][0]:",GlobalVariable.quickcommand_setting_list[GlobalVariable.quickcommand_number][0])
            kk=[]
            kk.append("quickcommand"+str(GlobalVariable.quickcommand_number)+":{\n")  #开始标志
            kk.append(self.lineEdit_commandname.text()+"\n")  #快速命令标签命名
            kk.append(quickcommand+"\n")  #将quickcommand保存到文件，为了从初始文件中恢复GlobalVariable.quickcommand_list
            
            for v in GlobalVariable.quickcommand_setting_list[GlobalVariable.quickcommand_number]:  #因为有5个才遍历到5，如果更改了数量，需要此处更改
                kk.append(v + "\n")
                
            kk.append("}"+"quickcommand"+str(GlobalVariable.quickcommand_number)+"\n")
            print("kk:",kk)
            
            configfile=open(GlobalVariable.configfilename, 'a+')
            configfile.writelines(kk)
            configfile.close()
            GlobalVariable.quickcommand_number+=1


    @pyqtSlot()
    def on_pushButton_confirm_clicked(self):
        """
        Slot documentation goes here.
        """
        self.addquickcommand()
