# -*- coding: utf-8 -*-

"""
Module implementing AddDelayDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_adddelaydialog import Ui_AddDelayDialog


class AddDelayDialog(QDialog, Ui_AddDelayDialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AddDelayDialog, self).__init__(parent)
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window
    
    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    

    @pyqtSlot()
    def on_pushButton_addDelayTime_clicked(self):
        """
        Slot documentation goes here.
        """
        testCommandList.append(self.lineEdit_delayTime.text())
        print(testCommandList)
        self.close()
