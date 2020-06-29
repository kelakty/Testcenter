# -*- coding: utf-8 -*-

"""
Module implementing KeyCombination.
"""

from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog
from globalvariable import GlobalVariable
from .Ui_keycombination import Ui_keycombination


class KeyCombination(QDialog, Ui_keycombination):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(KeyCombination, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.Dialog) 
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window

    @pyqtSlot()
    def on_ctrlC_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.mainwindow.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        consolethread = GlobalVariable.Console[index]["consolethread"]
        send_list = []
        send_list.append(0x03)
        input_s = bytes(send_list)
        consolethread.send_trigger.emit(input_s)
    
    @pyqtSlot()
    def on_ctrlZ_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.mainwindow.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        consolethread = GlobalVariable.Console[index]["consolethread"]
        send_list = []
        send_list.append(0x1a)
        input_s = bytes(send_list)
        print("keycombination",send_list,input_s,type(send_list),type(input_s))
        print("keycombination",bytes(0x1a),type(bytes(0x1a))
        consolethread.send_trigger.emit(input_s)
    
    @pyqtSlot()
    def on_ctrlT_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.mainwindow.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        consolethread = GlobalVariable.Console[index]["consolethread"]
        send_list = []
        send_list.append(0x14)
        input_s = bytes(send_list)
        consolethread.send_trigger.emit(input_s)
    
    @pyqtSlot()
    def on_ctrlU_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.mainwindow.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        consolethread = GlobalVariable.Console[index]["consolethread"]
        send_list = []
        send_list.append(0x15)
        input_s = bytes(send_list)
        consolethread.send_trigger.emit(input_s)
    
    @pyqtSlot()
    def on_ctrlB_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.mainwindow.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        consolethread = GlobalVariable.Console[index]["consolethread"]
        send_list = []
        send_list.append(0x02)
        input_s = bytes(send_list)
        consolethread.send_trigger.emit(input_s)
    
    @pyqtSlot()
    def on_ctrlA_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.mainwindow.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        consolethread = GlobalVariable.Console[index]["consolethread"]
        send_list = []
        send_list.append(0x01)
        input_s = bytes(send_list)
        consolethread.send_trigger.emit(input_s)

