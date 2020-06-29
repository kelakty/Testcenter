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
        if self.telnethost.text() != "" and self.telnetport.text() != "":
            self.telnet_host = self.telnethost.text()
            self.telnet_port = self.telnetport.text()
        print(self.telnet_host,self.telnet_port)
        
        #新建MDI
        if self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.telnet_host + "_" + self.telnet_port ) < 0:
            if self.tryopencom() == True: #尝试打开串口，串口没打开则新建串口线程
                #创建一个MDIarea的sub窗口
                subwindow = NewMdiSubWindow()   #subwindow对象
                subwindow.setMain(self)

                # 向sub内部添加QTextEdit控件
                subwindow.setWidget(QtWidgets.QTextEdit())
                
                #QTextEdit控件 对象
                console_terminal=subwindow.widget()
                # console_terminal.insertPlainText("self.consoleT_insert\r\n")

                #对console_terminal进行事件过滤
                console_terminal.installEventFilter(subwindow)
                console_terminal.selectionChanged.connect(lambda: self.textCopy(console_terminal))  #选择文本自动复制
                
                #对终端设置window标题
                if self.renameconsole.text() != "":
                    subwindow.setWindowTitle(self.renameconsole.text())
                else:
                    subwindow.setWindowTitle(self.com_option.currentText())
                self.mdiArea.addSubWindow(subwindow)
                
                subwindow.setAttribute(Qt.WA_DeleteOnClose) #设置subwindow属性，当点击关闭时删除对象
                subwindow.setWindowFlags(Qt.WindowTitleHint)
                subwindow.show()
                # print("当前sub窗口是：",self.mdiArea.currentSubWindow())   #TODO 后续删除

                GlobalVariable.SelectCom=self.com_option.currentText()
                # print("selectCOM is:",GlobalVariable.SelectCom)
                # print("port是:",self._ports[self.com_option.currentText()])
                GlobalVariable.setting_stop_bit=self.stop_bit.currentText()
                GlobalVariable.setting_data_bits= self.data_bits.currentText()
                GlobalVariable.setting_checksum_bits=self.checksum_bits.currentText()
                GlobalVariable.setting_baud_rate_option= self.baud_rate_option.currentText()

                #创建新线程，初始化一个串口
                self.console_terminal_threadpool.append(SerialThread())
                consolethread = SerialConsoleThread(GlobalVariable.SelectCom)  #需要传入打开的串口名self.com_option.currentText()，要用全局变量来传递。
                consolethread.moveToThread(self.console_terminal_threadpool[-1])
                self.console_terminal_threadpool[-1].started.connect(consolethread.serial_init)
                consolethread.rec_trigger.connect(self.rec_comdata_slot, Qt.QueuedConnection)  #
                consolethread.send_trigger.connect(consolethread.sendto_comdata_slot)
                self.console_terminal_threadpool[-1].start() 

                #保存所有参数到GlobalVariable.Console字典列表
                consoledict={"type":"serial",  
                            "name":self.com_option.currentText(), "customname": self.renameconsole.text(),
                            "subwindowobj": subwindow, "consoleobj":console_terminal,
                            "consolethread":consolethread, "threadpool":self.console_terminal_threadpool[-1],
                            "encodingtype":self.encodingtype.currentText()
                            }
                GlobalVariable.Console.append(consoledict)
                self.statusbar.showMessage("串口打开成功")
                self.textEdit_message.insertPlainText("%s串口打开成功\r\n" % self.com_option.currentText())
                return True  #创建串口线程成功
        else:
            self.statusbar.showMessage("串口已经打开了")
            self.textEdit_message.insertPlainText("%s串口已经打开了\r\n" % self.com_option.currentText())
