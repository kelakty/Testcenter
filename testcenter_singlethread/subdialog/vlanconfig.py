# -*- coding: utf-8 -*-

"""
Module implementing VlanConfig.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from subdialog.Ui_vlanconfig import Ui_VlanConfig
#from  import MainWindow


class VlanConfig(QDialog, Ui_VlanConfig):
    """
    Class documentation goes here.
    """
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(VlanConfig, self).__init__(parent)
       
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window
        
    @pyqtSlot()
    def on_cancel_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    @pyqtSlot()
    def on_auto_gen_clicked(self):
        """
        Slot documentation goes here.
        """
        slot_num=int(self.slot_num.text())
        print(slot_num)
        com_type=self.com_type.text()
        print(com_type)
        first_vlan=int(self.first_vlan.text())
        print(first_vlan)
        com_num=int(self.com_num.text())
        print(com_num)
        print("开始计算vlan")
        a=range(com_num)
        for i in a[2::2]:
            print("int range %s%d/%d,%d/%d" % (com_type,slot_num,i,slot_num,i+1))
            print("sw acc vl %d" % (i+first_vlan))
            self.mainwindow.plainTextEdit.insertPlainText("int range %s%d/%d,%d/%d\r\n" % (com_type,slot_num,i,slot_num,i+1))
            self.mainwindow.plainTextEdit.insertPlainText("sw acc vl %d\r\n" % (i+first_vlan))
    
        print("int range %s%d/%d,%d/1" % (com_type,slot_num,com_num,slot_num))
        print("sw acc vl %d" % (com_num+first_vlan+1))
        self.mainwindow.plainTextEdit.insertPlainText("int range %s%d/%d,%d/1\r\n" % (com_type,slot_num,com_num,slot_num)) 
        self.mainwindow.plainTextEdit.insertPlainText("sw acc vl %d\r\n" % (com_num+first_vlan+1))
        
        self.close()
    
    @pyqtSlot()
    def on_com_num_editingFinished(self):
        """
        Slot documentation goes here.
        """
        #con_num,ok=QInputDialog.getText(self,"输入字符串","请输入一个字符串",QLineEdit.Normal,'请在此输入') #文本框输入对话框
        #下拉对话框
        #my_list = QStringList()
        #my_list.append("slot1")
        #my_list.append("slot2")
        #my_str=QInputDialog.getItem(self,"下拉框","请选择",my_list)
        
        #con_num,ok=QInputDialog.getInteger(self,"输入整数","请输入一个整数",30,0,100) #限定默认值以及上下限
        
#        self.com_num=self.com_num.text()
#        print(self.com_num)
        
    
    @pyqtSlot()
    def on_first_vlan_editingFinished(self):
        """
        Slot documentation goes here.
        """
#        self.first_vlan=self.first_vlan.text()
#        print(self.first_vlan)
    
    @pyqtSlot()
    def on_com_type_editingFinished(self):
        """
        Slot documentation goes here.
        """
#        self.com_type=self.com_type.text()
#        print(self.com_type)
    
    @pyqtSlot()
    def on_slot_num_editingFinished(self):
        """
        Slot documentation goes here.
        """
#        self.slot_num=self.slot_num.text()
#        print(self.slot_num)
