# -*- coding: utf-8 -*-

"""
Module implementing CommonTestCommand.
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QTextDocument,QTextCursor

from .Ui_testcommandillustration import Ui_TestCommandIllustration


class TestCommandIllustration(QWidget, Ui_TestCommandIllustration):
    """
    Class documentation goes here.
    """



    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        # # 搜索相关项
        self.search_content = None
        self.search_key = None
        self.search_count = 0
        self.search_current = 0
        # self.search_updown=0

        super(TestCommandIllustration, self).__init__(parent)
        self.setupUi(self)
        
    def setMain(self, main_window):
        self.mainwindow=main_window

    def searchtext(self):
        #QTextDocument.FindFlags()  cursorForward 
        #QTextDocument.FindBackward()
        flag = QTextDocument.FindFlags()   #反向搜索
        searchtextexpress= self.lineEdit_searchexpression.text()
        if searchtextexpress is not "":
            print(searchtextexpress)
            print(self.textBrowser_testcommand.cursor())
            self.textBrowser_testcommand.find(searchtextexpress,QTextDocument.FindFlag())
            print(self.textBrowser_testcommand.cursor())

        # print(self.textBrowser_testcommand.find(searchtextexpress,QTextDocument.FindFlags()))

    def select(self, start, length):
        """选中文字,高亮显示"""
        cur = QTextCursor(self.textBrowser_testcommand.textCursor())
        cur.setPosition(start)
        cur.setPosition(start + length, QTextCursor.KeepAnchor)
        self.textBrowser_testcommand.setTextCursor(cur)

    def reset_search_content(self):
        """改变待搜索内容"""
        self.search_content = None
        self.search_count = 0
        self.search_current = 0


    def search(self):
        #"""搜索"""
        key_word = self.lineEdit_searchexpression.text()
        if key_word != self.search_key:
            self.search_key = key_word
            self.search_count = 0
            self.search_current = 0
        if not self.search_content:
            self.search_content = self.textBrowser_testcommand.toPlainText() #.toPlainText()
        if not self.search_count:
            self.search_count = self.search_content.count(key_word)
            if self.search_count != 0:
                start = self.search_content.index(key_word)
                self.select(start, len(key_word))
                self.search_current += 1
        else:
            if self.search_current < self.search_count:
                start = self.search_content.find(key_word, self.textBrowser_testcommand.textCursor().position())
                if start != -1:
                    self.select(start, len(key_word))
                    self.search_current += 1
            else:
                self.search_count = 0
                self.search_current = 0
                self.search()
        self.textBrowser_testcommand.setFocus()
        # print(self.search_count,self.search_current)
        self.label_searchcount.setText("{}/{}".format(self.search_current, self.search_count))




    @pyqtSlot()
    def on_pushButton_search_clicked(self):
        """
        按下搜索按钮
        """
        self.search()
