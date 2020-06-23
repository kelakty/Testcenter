# -*- coding: utf-8 -*-

"""
Module implementing SendCommandDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from subdialog.Ui_addsendcommand import Ui_Dialog
from globalvariable import GlobalVariable

# from testcommandsessions import testcommandlist  #可以通过这种方法传递列表型全局变量
# from testcommandsessions import TestCommandSession


class SendCommandDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(SendCommandDialog, self).__init__(parent)
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window
           
    
    @pyqtSlot()
    def on_pushButton_addTestCommand_clicked(self):
        """
        点击添加测试命令到序列
        """
        
        case_numname="Item_"+str(GlobalVariable.case_num)
        column_num=0
        GlobalVariable.testcommandlist.append("@"+str(GlobalVariable.case_num)+
                                        "@"+str(GlobalVariable.commandlist_num)+
                                        "@"+self.lineEditSendCommand.text()+"\r\n")
        

        #显示测试命令到tree
        commandlist_treename = "Item_"+str(GlobalVariable.commandlist_num)
        self.generatetree=case_numname+"= QtWidgets.QTreeWidgetItem(self.mainwindow.treeWidget_sequencer)"
        self.setcheckstate=case_numname+".setCheckState(0, QtCore.Qt.Checked)"
        exec(self.generatetree)
        exec(self.setcheckstate)
        self.mainwindow.treeWidget_sequencer.topLevelItem(GlobalVariable.case_num).setText(column_num, QtCore.QCoreApplication.translate("MainWindow", self.lineEditSendCommand.text()))
        # self.mainwindow.treeWidget_sequencer.topLevelItem(GlobalVariable.case_num).setText(column_num+1, QtCore.QCoreApplication.translate("MainWindow", "show信息"))
        # self.mainwindow.treeWidget_sequencer.topLevelItem(GlobalVariable.case_num).setText(column_num+2, QtCore.QCoreApplication.translate("MainWindow", "客户端 dut1主"))
        print("已显示完自生成tree")

        
        # #调试单个实例：
        # item_0 = QtWidgets.QTreeWidgetItem(self.mainwindow.treeWidget_sequencer)
        # item_0.setCheckState(0, QtCore.Qt.Checked)
        # self.mainwindow.treeWidget_sequencer.topLevelItem(0).setText(0, QtCore.QCoreApplication.translate("MainWindow", "show version detail "))
        # self.mainwindow.treeWidget_sequencer.topLevelItem(0).setText(1, QtCore.QCoreApplication.translate("MainWindow", "show信息"))
        # self.mainwindow.treeWidget_sequencer.topLevelItem(0).setText(2, QtCore.QCoreApplication.translate("MainWindow", "客户端 dut1主"))
        # print("已显示完tree控件")
        
        
        print(GlobalVariable.testcommandlist)
        GlobalVariable.case_num+=1
        GlobalVariable.commandlist_num+=1
        self.close()
    
    @pyqtSlot()
    def on_pushButton_editSendCommand_cancel_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
