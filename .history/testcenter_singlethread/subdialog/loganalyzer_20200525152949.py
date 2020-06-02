# -*- coding: utf-8 -*-

"""
Module implementing LogAnalyzer.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from .Ui_loganalyzer import Ui_loganalyzer


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
        self.setupUi(self)
    
    @pyqtSlot()
    def on_selectpath_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_selectsavepath_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_pushButton_gen_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
