# -*- coding: utf-8 -*-

"""
Module implementing NewTelnet.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from Console import Console
from .Ui_newtelnet import Ui_NewTelnet


class NewTelnet(QDialog, Ui_NewTelnet, Console):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(NewTelnet, self).__init__(parent)
        self.setupUi(self)

    def setMain(self, main_window):
        self.mainwindow=main_window
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.newtelnetconsole()

    def newtelnetconsole(self):
        """
        新建telnet控制台
        """
        pass
        #新建MDI
