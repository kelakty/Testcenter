# -*- coding: utf-8 -*-

"""
Module implementing About.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from .Ui_contactus import Ui_about


class About(QDialog, Ui_about):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(About, self).__init__(parent)
        self.setupUi(self)
        
    def setMain(self, main_window):
        self.mainwindow=main_window
