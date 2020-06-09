# -*- coding: utf-8 -*-

"""
Module implementing KeyCombination.
"""

from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtWidgets import QDialog

from .Ui_keycombination import Ui_Dialog


class KeyCombination(QDialog, Ui_Dialog):
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
        pass
        # self.mainwindow.plainTextEdit.insertPlainText("sw acc vl %d\r\n" % (com_num+first_vlan+1))
    
    @pyqtSlot()
    def on_ctrlZ_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_ctrlT_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_ctrlU_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_ctrlB_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_ctrlA_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
