# -*- coding: utf-8 -*-

"""
Module implementing DialogCharacterRecognition.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_characterrecognition import Ui_DialogCharacterRecognition


class DialogCharacterRecognition(QDialog, Ui_DialogCharacterRecognition):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogCharacterRecognition, self).__init__(parent)
        self.setupUi(self)
        
    def setMain(self, main_window):
        self.mainwindow=main_window
    
    @pyqtSlot()
    def on_pushButton_addTest_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
