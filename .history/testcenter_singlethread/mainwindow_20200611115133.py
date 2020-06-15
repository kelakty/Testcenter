# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
#import serial
# import vt102
import pyte
from pyte.streams import Stream
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QIODevice, QByteArray,QPoint,QObject,QStandardPaths
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QWidget,QMainWindow,QFileDialog,QMenu,QApplication,QTableWidgetItem
from PyQt5.QtGui import QIcon,QCursor
from PyQt5 import QtGui
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import QTimer,QThread
from PyQt5.QtCore import QMetaType
from PyQt5.QtCore import Qt,QPoint
from PyQt5 import QtCore

import os 
from functools import partial
from PyQt5.QtWidgets import QMessageBox,QAction
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import pyqtSignal,QEvent
import pandas as pd
import re
import threading

from ui_mainwindow import Ui_MainWindow
from myui_mainwindow import MyUi_MainWindow
from subdialog.newtelnet import NewTelnet
from subdialog.vlanconfig import VlanConfig
from subdialog.keycombination import KeyCombination
from subdialog.addsendcommand import AddSendCommandWidgetandWaitingEcho
from subdialog.adddelaydialog import AddDelayDialog
from subdialog.characterrecognition import DialogCharacterRecognition
from subdialog.testcommandillustration import TestCommandIllustration
from subdialog.registerbaselinecheck import RegisterBaseLineCheck
from subdialog.fanandtemptest import FanAndTempTest
from subdialog.addquickcommand import AddQuickCommand
from subdialog.selectpythonscript import selectpythonscript
from AutomationScript import CRT
from serial_thread import SerialThread, SerialConsoleThread
from sequencer import SequencerThreadWorker
from console_init import ConsoleInit
from subdialog.loganalyzer import LogAnalyzer

from init import Init
import time
from globalvariable import GlobalVariable
from testcommandsessions import TestCommandSession
# from testcommandsessions import testcommandlist
# from testcommandsessions import commandlist_num
# from testcommandsessions import case_num

import logging
from logging import handlers
# import logger
from datetime import datetime
from loggerbythread import GeneralLogger


class NewMdiSubWindow(QtWidgets.QMdiSubWindow):
    """对QMdiSubWindow类重写，实现关闭窗口时执行其他功能"""
    # def __init__(self):
    #     super(NewMdiSubWindow,self).__init__() #parent
        
    def setMain(self, main_window):
        self.mainwindow=main_window

    def closeEvent(self, event):
        # print("准备关闭tab窗口...")
        # if GlobalVariable.Console == []:
        result = QtWidgets.QMessageBox.question(self, "Robot", "Do you want to close?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if(result == QtWidgets.QMessageBox.Yes):
            event.accept()
            #需要对打开的串口进行关闭等操作，删除全局变量中的串口信息
            index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console,"subwindowobj",self)
            if index >= 0:
                #此处需要关闭线程，删除线程、Mdi窗体、等相关对象的变量值
                GlobalVariable.Console[index]["consolethread"].rec_trigger.disconnect(self.mainwindow.rec_comdata_slot) 
                GlobalVariable.Console[index]["consolethread"].send_trigger.disconnect(GlobalVariable.Console[index]["consolethread"].sendto_comdata_slot)
                GlobalVariable.Console[index]["serialobj"].close() #关闭串口
                GlobalVariable.Console[index]["threadpool"].quit()
                GlobalVariable.Console[index]["threadpool"].wait()
                # print("线程是否finish",GlobalVariable.Console[index]["threadpool"].isFinished()) #查看线程是否已经finished
                GlobalVariable.Console[index]["threadpool"].deleteLater()

                # self.mainwindow.console_terminal_threadpool.remove(GlobalVariable.Console[index]["threadpool"])
                GlobalVariable.Console.remove(GlobalVariable.Console[index])
                # print('关闭后总共有哪些线程：',threading.enumerate())    #查看有哪些线程
                # print("串口线程已关闭")
        else:
            event.ignore()

    def eventFilter(self, obj, event):
        
        # if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
        #     self.close()
        #     return True  # 说明这个事件已被处理，其他控件别插手
        # else:
        #     return QObject.eventFilter(self, obj, event)  # 交由其他控件处理
        
        #处理console_terminal键盘按下事件
        #判断该窗口的串口对象是否在已打开串口列表
        if event.type() == event.KeyPress:
            #判断哪个窗口按下的事件
            # print("当前窗口对象是：",obj)
            index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "consoleobj", obj)
            if  index >= 0:
                consolethread = GlobalVariable.Console[index]["consolethread"]
                if event.key() == QtCore.Qt.Key_Up:
                    send_list = []
                    send_list.append(0x1b)
                    send_list.append(0x5b)
                    send_list.append(0x41)
                    input_s = bytes(send_list)
                    consolethread.send_trigger.emit(input_s)
                elif event.key() == QtCore.Qt.Key_Down:
                    #down 0x1b5b42 向下箭头
                    send_list = []
                    send_list.append(0x1b)
                    send_list.append(0x5b)
                    send_list.append(0x42)
                    input_s = bytes(send_list)
                    consolethread.send_trigger.emit(input_s)
                elif event.key() == QtCore.Qt.Key_Backspace:   #删除键处理
                    send_list = []
                    send_list.append(0x08)
                    input_s = bytes(send_list)
                    consolethread.send_trigger.emit(input_s)
                    terminal_cursor = GlobalVariable.Console[index]["consoleobj"].textCursor()
                    if terminal_cursor.hasSelection():
                        terminal_cursor.movePosition(QTextCursor.NoMove, QTextCursor.KeepAnchor, 
                            terminal_cursor.selectionStart() - terminal_cursor.selectionStart())
                    else:
                        terminal_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, 1)
                    GlobalVariable.Console[index]["consoleobj"].setTextCursor(terminal_cursor)
                    GlobalVariable.Console[index]["consoleobj"].copy() 
                    #clipboard = QtGui.QApplication.clipboard()  #剪贴板
                else:    
                    #获取按键对应的字符进行发送
                    char = event.text()
                    try:
                        consolethread.send_trigger.emit(char.encode(GlobalVariable.Console[index]["encodingtype"]))
                    except Exception :
                        # print("发送字符信号发射出错")
                        
                        self.textEdit_message.insertPlainText("%s发送字符出错\r\n" % GlobalVariable.Console[index]["name"])
                    # print('%-25s: %s, %s,' % ("mainwin_event", QThread.currentThread(), int(QThread.currentThreadId())))
                    # print('%-25s: %s, %s,' % ("mainwin_event", threading.current_thread().name, threading.current_thread().ident))
                    
            else:
                pass
            return True
        else:
            return QObject.eventFilter(self, obj, event)  # 交由其他控件处理


class MainWindow(QMainWindow, Ui_MainWindow, MyUi_MainWindow):
    """
    Class documentation goes here.
    """
    
    def __init__(self, *args, **kwargs):
        """
              
        @param parent reference to the parent widget
        @type QWidget
        """
        
        super(MainWindow, self).__init__(*args, **kwargs)
        #QtWidgets.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)#加上该句后窗口始终在其他所有窗口上层显示
        self.setupUi(self)
        self.setupUi2(self)
        GlobalVariable.mainwindow=self

        currentdatetime = "TestCenter_%d%02d%02d" % (datetime.now().year,
                            datetime.now().month, datetime.now().day)
        GeneralLogger().set_log_path(currentdatetime + '.log') 
        GeneralLogger().set_log_by_thread_log(True)
        GeneralLogger().set_log_level(logging.DEBUG)
        self.main_logger = GeneralLogger().get_logger()
        self.main_logger.info('开始记录主线程log...')
        # self.crt=CRT()
        # self.crt.setMain(self)
        self.console_terminal_threadpool = [] #创建一个空线程池管理线程
        self.sequencer_threadpool = []
        self.sequencer_thread = object
        # self.subwindow=[]
        # self.console_terminal=[]
        self.analyze=[]
        self.toolBar_quickcommand.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # 加载初始化配置文件,初始化窗体等
        # try:
        self.config_init()
        # self.init=Init()
        # self.init.setMain(self)
        # self.init.config_init()
        # except Exception :
        #     QMessageBox.critical(self,'critical','初始化配置文件出错，请删除程序目录下的config.ini初始化配置文件后重试')

        #控制台接收数据Queue
        
        self.getAvailablePorts()
        self.open_close_buttom.setStyleSheet("color:rgb(255, 0, 0);\n"
"font: 9pt \"黑体\";\n"
"selection-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        
        #实例化一个定时发送的定时器
        self.timer_send = QTimer(self)
        #定时发送
        self.timer_send.timeout.connect(self.on_send_button_clicked)
        #实例化一个LCD时钟显示的定时器
        self.lcdtimer = QTimer(self)
        self.lcdtimer.timeout.connect(self.clock)
        self.lcdtimer.start()


        # #VT102终端初始化
        # self.stream = vt102.stream()
        # self.screen = vt102.screen((30,94))
        # self.screen.attach(self.stream)
        '''#pyte：
        data=u"\u001b7\u001b[?47h\u001b)0\u001b[H\u001b[2J\u001b[H" +\
               u"\u001b[2;1HNetHack, Copyright 1985-2003\r\u001b[3;1" +\
               u"H         By Stichting Mathematisch Centrum and M. " +\
               u"Stephenson.\r\u001b[4;1H         See license for de" +\
               u"tails.\r\u001b[5;1H\u001b[6;1H\u001b[7;1HShall I pi" +\
               u"ck a character's race, role, gender and alignment f" +\
               u"or you? [ynq] "

        #pyte终端初始化
        # self.screen = pyte.Screen(90, 20)
        self.screen = pyte.Screen(pyte.DebugScreen())
        # self.screen.dirty   ##{0, 1} 显示的好像是屏幕现有哪些行
        # self.screen.dirty.clear()    
        self.stream = pyte.Stream(self.screen)  #流不会将事件分派给创建流之后添加到屏幕上的方法。
        # self.stream.attach(self.screen)  #这是多余的，在创建stream时初始化如果判断screen非空则自动attach
        self.stream.feed(data)   ##stream.feed只接收text文本输入，如果是接收byte则要使用pyte.streams.ByteStream
        #Get index of last line containing text
        last = max(self.screen.dirty)   #读取最后一行的编号，好像上面创建了屏幕大小是多少，dirty就是多少。设置20行，dirty的max就是19
        print("初始状态屏的行数：",last)
        # self.console_terminal.insertPlainText(self.screen.display)
        #Gather lines, stripping trailing whitespace
        lines = [self.screen.display[i].rstrip() for i in range(last + 1)]
        # print('\n'.join(lines))
        
        self.console_terminal.insertPlainText('\n'.join(lines))
        # self.screen.dirty.clear()
        # self.screen.erase_in_display(1) 
        '''



        #测试VT102库是否可用----测试OK
        # self.stream.process(u"\u001b7\u001b[?47h\u001b)0\u001b[H\u001b[2J\u001b[H" +
        #        u"\u001b[2;1HNetHack, Copyright 1985-2003\r\u001b[3;1" +
        #        u"H         By Stichting Mathematisch Centrum and M. " +
        #        u"Stephenson.\r\u001b[4;1H         See license for de" +
        #        u"tails.\r\u001b[5;1H\u001b[6;1H\u001b[7;1HShall I pi" +
        #        u"ck a character's race, role, gender and alignment f" +
        #        u"or you? [ynq] ")
        # self.console_terminal.insertPlainText(str(self.screen))
    def textCopy(self,consoleobj):  #选择文本自动复制
        consoleobj.copy()
        # command = QApplication.clipboard().text().upper()
        # print(command)

    def clock(self):
        t = time.strftime("%m%d %H:%M:%S")
        self.lcd.display(t)


    def action_hoverd(self,actionis):
        # print("hoverd action is: " , actionis)
        GlobalVariable.hoverd_action=actionis

    def find_dictionarylist_keyvalue_index(self,dictionarylist, keyname, keyvalue):
        """
        从字典列表中查找 是否存在 某一个key 且对应的值正确 则返回字典所在列表的索引，否则返回-1，由于0 == False，所以不能返回False
        如果字典列表为空也返回-1
        找到匹配的键值对 立马返回不再向下查找
        Args：
            dictionarylist: 一个字典列表
            keyname: 字典中的key名字
            keyvalue:字典中key名字对应的value值
        Return：
            index: 找到的键值对字典 所在列表的索引值
            False ： 没找到
            
        """
        if dictionarylist == []:
            return -1

        for index in range(len(dictionarylist)):
            for key in dictionarylist[index]:
                # print("%s--%s" % (key,dictionarylist[index][key]))
                if key == keyname:
                    if dictionarylist[index][key] == keyvalue:
                        return index
        return -1


    @pyqtSlot()
    def on_open_close_buttom_clicked(self):
        # 打开或关闭串口按钮
        #判断串口是否已经是打开的,如果不是已打开的则创建一个线程打开串口初始化，否则打印提示到底部状态栏
        #consoleinit=ConsoleInit():

        #判断GlobalVariable.Console是否为空，为空表示没有创建任何console
        #如果self.com_option.currentText()不在Console字典列表中，则开始新建串口
        # print("打开串口前是否在字典列表里找到：",self.find_dictionarylist_keyvalue_index(GlobalVariable.Console,"name",self.com_option.currentText()))
        if self.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.com_option.currentText()) < 0:
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

                # print('%-25s: %s, %s,' % ("mainwindow_slot", QThread.currentThread(), int(QThread.currentThreadId())))
                # print('%-25s: %s, %s,' % ("mainwindow_slot", threading.current_thread().name, threading.current_thread().ident))
                
                #创建新线程，初始化一个串口
                self.console_terminal_threadpool.append(SerialThread())
                consolethread=SerialConsoleThread(self.com_option.currentText())  #需要传入打开的串口名self.com_option.currentText()
                consolethread.moveToThread(self.console_terminal_threadpool[-1])
                self.console_terminal_threadpool[-1].started.connect(consolethread.serial_init)
                consolethread.rec_trigger.connect(self.rec_comdata_slot, Qt.QueuedConnection)  #
                consolethread.send_trigger.connect(consolethread.sendto_comdata_slot)
                self.console_terminal_threadpool[-1].start() 

                #sequencer相关的信号槽
                

                #保存所有参数到GlobalVariable.Console字典列表
                consoledict={"type":"serial",  
                            "name":self.com_option.currentText(), "customname": self.renameconsole.text(),
                            "subwindowobj": subwindow, "consoleobj":console_terminal,
                            "consolethread":consolethread, "threadpool":self.console_terminal_threadpool[-1],
                            "encodingtype":self.encodingtype.currentText()
                            }
                GlobalVariable.Console.append(consoledict)
                # print("consoledictlist is :", GlobalVariable.Console)

                # consolethread.send_trigger.emit("test_emit:".encode(encodingType)) # TODO:后续需要删除
                # subwindow.sendanalyze_arg(consolethread)
                # self.console_terminal[comThreadCounter].selectionChanged.connect(lambda: self.console_terminal[comThreadCounter].copy())  #选择文本自动复制
                
                # subwindow.widget().insertPlainText("%s is %s\r\n" % (GlobalVariable.Console,subwindow)) # TODO:后续需要删除
                self.statusbar.showMessage("串口打开成功")
                self.textEdit_message.insertPlainText("%s串口打开成功\r\n" % self.com_option.currentText())
                # self.textEdit_message.insertPlainText("\r\r\n")   
                # self.textEdit_message.insertPlainText("插入")
                # self.textEdit_message.insertPlainText("插入")
                # self.textEdit_message.insertPlainText("\r\n")
                # self.textEdit_message.insertPlainText("插入\r")
                # self.textEdit_message.insertPlainText("插入")
                # self.textEdit_message.insertPlainText("插入\n")
                # self.textEdit_message.insertPlainText("插入")
                return True  #创建串口线程成功
        else:
            # print(self.com_option.currentText(),"串口已经打开了")
            self.statusbar.showMessage("串口已经打开了")
            self.textEdit_message.insertPlainText("%s串口已经打开了\r\n" % self.com_option.currentText())

  
    @pyqtSlot()
    def on_send_button_clicked(self):
        if self.timer_send_checkbox.checkState(): #如果勾选定时发送，则定时发送。否则发送后清空发送缓冲区
            self.sendtoconsole()
        else:
            self.sendtoconsole()
            #清空发送区
            self.plainTextEdit.clear()
            
    def sendtoconsole(self):
        # 发送消息
        if self.mdiArea.currentSubWindow() != None:  #判断是否有可用终端
            index = self.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mdiArea.currentSubWindow())
            text = self.plainTextEdit.toPlainText()
            # text+="\r\n"   #TODO 这里是否要加回车换行取决于 ctrl+C等组合键是否能够正常发送
            if not text:
                return
            GlobalVariable.Console[index]["consolethread"].send_trigger.emit(text.encode(GlobalVariable.Console[index]["encodingtype"]))
        
        else:
            self.textEdit_message.insertPlainText("无可用终端\r\n")
        
            
    """全部移入线程内
    def onReadyRead(self):
        # 数据接收响应
        if self.serial.bytesAvailable():
            
            # 当数据可读取时
            # 这里只是简单测试少量数据,如果数据量太多了此处readAll其实并没有读完
            # 需要自行设置粘包协议
            # if self._serial.canReadLine():    #此处为判断数据有换行符，读取整行，如果无换行符，代表不是整行，则没法读。
                                            #因为--More-- \x08\x08\x08\x08\x08\x08\x08\x08\x08\x08   
                                            # #没有换行，没法实时显示，所以不用canreadline函数，而是实时显示
                
            try:
                GlobalVariable.serialreaddata = self.serial.readAll() #self._serial.readLine()会出现转码错误，不知道为啥
                GlobalVariable.receivebuffer+=GlobalVariable.serialreaddata
                # print("buffer",id(GlobalVariable.receivebuffer))
                # print("serialdata",id(GlobalVariable.serialreaddata))
                # print(type(serialreaddata))  #收到的数据类型是<class 'PyQt5.QtCore.QByteArray'>
                # return data2
                #print(data2.strip('\r'))
                #print(b'\x08 \x08'.decode('gbk'))
                
                # #粘包协议：
                # GlobalVariable.receivebuffer += serialreaddata
                # print(GlobalVariable.receivebuffer)

                # #VT102处理
                # self.stream.process(serialreaddata.data().decode('gb2312'))
                # self.console_terminal.insertPlainText(str(self.screen))
                '''
                #pyte处理
                serialreaddata = serialreaddata.data().decode('utf-8')
                print(serialreaddata)
                # self.stream.feed(serialreaddata.data().decode('gb2312'))
                # self.console_terminal.insertPlainText(str(self.screen))
                print(self.screen.dirty)
                self.screen.dirty.clear() 
                print(self.screen.dirty)
                # self.stream.feed('HELLO THIS IS T TEST\x1b[16D                \x1b[16D  ')  
                self.stream.feed(serialreaddata)
                #Get index of last line containing text
                last = max(self.screen.dirty)
                print("缓存屏的行数：",last)
                #Gather lines, stripping trailing whitespace
                # one_lines = [self.screen.display[i].rstrip() for i in range(last + 1)]
                one_lines = [self.screen.display[0]]
                # print('\n'.join(one_lines))
                self.console_terminal.insertPlainText('\r\n'.join(one_lines))
                '''

                #原始的处理终端显示部分---已弃用
                #gb2312b编码，正常在python中print出来出来print(b'\x32\x33\x34\x08 \x08\x35\x36'.decode('gb2312'))结果为2356，
                #也就是\x08 \x08会执行退格空格退格操作，但是使用insertPlainText或者append进QTextEdit时，无法达到想要的效果，
                #退格无效只保留了空格,因此此处退格删除操作用自定义指令实现。
                #此处打印console terminal到log文件应该需要进行粘包，按照换行来，
                # 只有有换行则打印一条log，没有换行则等待下一个字符直到有换行
                print("调试串口接收到：",GlobalVariable.serialreaddata)
                # self.console_terminal.insertPlainText("这是一个测试第一行")
                # self.console_terminal.insertPlainText("这是一个测试第二行")
                # self.console_terminal.insertPlainText("这是一个测试第三行")
                #以上插入信息时不会换行
                #将console_terminal光标移动到末尾
                # if(self.console_terminal.textCursor() != self.console_terminal.textCursor().End):
                #     self.console_terminal.textCursor().movePosition(self.console_terminal.textCursor().End)
                #     self.console_terminal.setTextCursor(self.console_terminal.textCursor())
                cursor = self.console_terminal.textCursor()
                if(cursor != cursor.End):
                    cursor.movePosition(cursor.End)
                    self.console_terminal.setTextCursor(cursor)
                loginfo=""
                if GlobalVariable.serialreaddata != b'\x08 \x08':
                    if GlobalVariable.serialreaddata.contains(b'\r\r\n'):
                        self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
                        loginfo=GlobalVariable.serialreaddata.data().decode('gb2312')
                        print("处理后的log信息",loginfo)
                        logger.info("\r\n"+GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
                    #self.console_terminal.append(b'\x31\x32\x33'.decode('gb2312'))
                    else:
                        self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312')) #.strip('\r') insertPlainText
                        logger.info("\r\n"+GlobalVariable.serialreaddata.data().decode('gb2312'))
                    #print('无退格')
                
            
            except  Exception:
                pass
                # QMessageBox.critical(self, '','转码出错!')
                return 

            # #移动光标到VT102末尾(未成功待开发)
            # print(self.console_terminal.textCursor())
            # cursor = self.console_terminal.textCursor()
            # cursor.(vt102.screen.cursor)
            # self.console_terminal.setTextCursor(cursor)

    #            print(data2)
    #            self.console_terminal.append(data2.data().decode('gb2312').strip('\r\n')) #使用append方法插入会导致排版显示出现问题
    #            '''data = self._serial.readAll()
    #            if self.hex_receive.isChecked():
    #                # 如果勾选了hex显示
    #                data = data.toHex()
    #            data = data.data()'''
    #            # 解码显示（中文啥的）
    #            #print("接收处理前",data)
    #            #data=string(data.strip('\r'))
    #            '''try:
    #                data=data.decode('gb2312').strip('\r\n')
    #                #print("处理中",type(data))
    #                #print("处理中",data)
    #                self.console_terminal.append(data.strip('\n'))
    #            except:
    #                # 解码失败
    #                self.console_terminal.append(repr(data))'''
    """#全部移入线程内                
                    
    #ports_dict = {}  # 用于保存串口名与对应地址信息的字典
    def getAvailablePorts(self):
        # 获取可用的串口
        self._ports = {}  # 用于保存串口的信息
        infos = QSerialPortInfo.availablePorts() #返回的是可用串口对象地址信息列表
        #infos.reverse()  # 逆序
        self.com_option.clear()
        for info in infos:
            # 通过串口名字-->关联串口变量
            self._ports[info.portName()] = info
            GlobalVariable.ComINFO[info.portName()] = info
            #print("串口名",info.portName())  #显示的是串口对象地址对应的串口名
            self.com_option.addItem(info.portName())

    #该关闭事件为整体窗口的关闭事件重写，非MDI子窗口重写的关闭事件
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self, "Robot", "是否断开所有连接并关闭", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if(result == QtWidgets.QMessageBox.Yes):
            # if self._serial.isOpen():
            #     self._serial.close()
            event.accept()
        else:
            event.ignore()
        #这里放的位置不知道对不对
        # super(MainWindow, self).closeEvent(event)



    @pyqtSlot()
    def on_check_com_clicked(self):
        """
        获取可用的串口列表
        """
        self.getAvailablePorts()
            
    @pyqtSlot()
    def on_newTelnet_clicked(self):
        """
        点击新建Telnet连接
        """
        newTelnet = NewTelnet()
        newTelnet.setMain(self)
        newTelnet.exec_()
 

    @pyqtSlot()
    def on_timer_send_checkbox_clicked(self):
        """
        定时发送
        """
        if self.timer_send_checkbox.checkState():
            # try:
            time = self.timer_lineEdit.text()
            if float(time) < 1:
                time_val = float(time)*1000
                time_val = int(time_val)
            #定时器是ms为单位，需要将s转换为ms
            else :
                time_val = int(time, 10)*1000 #base=10 十进制
            if time_val == 0:
                QMessageBox.critical(self, 'pycom','定时时间必须大于零!')
                return None
            else:
                #定时间隔发送
                self.timer_send.start(time_val)
            # except  Exception:
            #     QMessageBox.critical(self, 'pycom','请输入有效的定时时间!')
            #     return    
        else:
            self.timer_send.stop()

    @pyqtSlot()
    def on_timer_lineEdit_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.on_timer_send_checkbox_clicked()

    @pyqtSlot()
    def on_clearsendbuffer_clicked(self):
        """
        清空发送缓冲区
        """
        self.plainTextEdit.clear()

    @pyqtSlot()
    def on_keycombination_clicked(self):
        """
        Slot documentation goes here.
        """
        keycombination = KeyCombination()  #由于不需要设置任何对象的属性，所以不需要参数
        keycombination.setMain(self)
        keycombination.exec_()

    @pyqtSlot()
    def on_select_logdir_clicked(self):
        """
        Slot documentation goes here.
        """
        
        fileName, type = QFileDialog.getSaveFileName(self, "Save as", os.getcwd(),   
                    "Log files (*.log);;Text files (*.txt);;All files (*.*)")
        self.savelogdir.clear()           
        self.savelogdir.insert(fileName)
        


    @pyqtSlot()
    def on_actionvlan_config_triggered(self):
        """
        Slot documentation goes here.
        """
        vlanConfig1 = VlanConfig()  #由于不需要设置任何对象的属性，所以不需要参数
        vlanConfig1.setMain(self)
        vlanConfig1.exec_()

#######显示菜单########
    @pyqtSlot()
    def on_active_serial_setting_triggered(self):
        """
        显示终端设置
        """
        if self.active_serial_setting.isChecked() == True:
            self.clientSetting.show()
        else:
            self.clientSetting.close()

    @pyqtSlot(bool)
    def on_clientSetting_visibilityChanged(self, visible):
        """
        Slot documentation goes here.
        
        @param visible DESCRIPTION
        @type bool
        """
        # print(self.clientSetting.isHidden())
        if self.clientSetting.isHidden()==True:
            self.active_serial_setting.setChecked(0)    
        else :
            self.active_serial_setting.setChecked(1)

    @pyqtSlot()
    def on_active_sequencer_triggered(self):
        """
        显示sequencer区
        """
        if self.active_sequencer.isChecked() == True:
            self.Sequencer.show()
            #print("显示sequencer控件")
        else:
            self.Sequencer.close()
            #print("关闭显示")

    @pyqtSlot()
    def on_actionShowToolBar_triggered(self):
        """
        菜单栏-显示-显示工具栏
        """
        pass

    @pyqtSlot()
    def on_actionshow_send_buffer_area_changed(self):
        """
        显示发送缓冲区
        """
        if self.actionshow_send_buffer_area.isChecked() == True:
            self.sendbuffer_dockwidget.show()
        else:
            self.sendbuffer_dockwidget.close()
    
    @pyqtSlot()
    def on_actionshow_message_area_changed(self):
        """
        显示message消息区
        """
        if self.actionshow_message_area.isChecked() == True:
            self.message_dockwidget.show()
        else:
            self.message_dockwidget.close()




    @pyqtSlot(bool)
    def on_Sequencer_visibilityChanged(self, visible):
        """
        Slot documentation goes here.
        
        @param visible DESCRIPTION
        @type bool
        """
        if self.Sequencer.isHidden()==True:
            self.active_sequencer.setChecked(0)    
        else :
            self.active_sequencer.setChecked(1)


#######设置菜单########    
    @pyqtSlot()
    def on_menuComSetting_triggered(self):
        """
        菜单-设置-串口设置
        """
        self.clientSetting.show()

    @pyqtSlot()
    def on_menuComSearch_triggered(self):
        """
        菜单-设置-串口设置
        """
        self.clientSetting.show()

    @pyqtSlot()
    def on_menuTelnetSetting_triggered(self):
        """
        菜单-设置-Telnet设置
        """
        self.clientSetting.show()
        
####工具菜单########
    @pyqtSlot()
    def on_actionvlan_triggered(self):
        """
        vlan配置
        """
        vlanConfig1 = VlanConfig()  #由于不需要设置任何对象的属性，所以不需要参数
        vlanConfig1.setMain(self)
        vlanConfig1.exec_()

    @pyqtSlot()
    def on_actionloganalyzer_triggered(self):
        """
        Slot documentation goes here.
        """
        self.loganalyze=LogAnalyzer(self)
        self.loganalyze.setMain(self)
        self.loganalyze.show()


####帮助菜单########
    @pyqtSlot()
    def on_actionshow_command_triggered(self):
        """
        Slot documentation goes here.
        """
        self.showcommoncommand = TestCommandIllustration()  #由于不需要设置任何对象的属性，所以不需要参数
        self.showcommoncommand.setMain(self)
        self.showcommoncommand.show()

###测试向导-创建测试###
    @pyqtSlot()
    def on_create_test_triggered(self):
        """
        Slot documentation goes here.
        """

    @pyqtSlot()
    def on_actionSendCommand_triggered(self):
        """
        Slot documentation goes here.
        """
        self.on_actionAddTest_triggered()
    
    @pyqtSlot()
    def on_actionCharactorRecognition_triggered(self):
        """
        Slot documentation goes here.
        """
        self.on_actionLogRecognition_triggered()
    
    @pyqtSlot()
    def on_actionDelay_triggered(self):
        """
        Slot documentation goes here.
        """
        self.on_actionSettingDelay_triggered()

    @pyqtSlot()
    def on_actionSpecialTest_2_triggered(self):
        """
        Slot documentation goes here.
        """
        self.on_actionSpecialTest_triggered()
    
    @pyqtSlot()
    def on_actionExpertScan_2_triggered(self):
        """
        Slot documentation goes here.
        """
        self.on_actionExpertScan_triggered()
    
    @pyqtSlot()
    def on_actionDeleteTest_2_triggered(self):
        """
        Slot documentation goes here.
        """
        self.on_actionDeleteTest_triggered()

    @pyqtSlot()
    def on_actionStartSession_triggered(self):
        """
        开始队列测试
        """
        TestCommandSession_obj=TestCommandSession()
        TestCommandSession_obj.setMain(self)
        TestCommandSession_obj.sendcommandlist(GlobalVariable.testcommandlist)

    @pyqtSlot()
    def on_actionLoad_Base_Line_triggered(self):
        """
        Slot documentation goes here.
        """
        self.registerbaselinecheck_obj=RegisterBaseLineCheck(self)
        self.registerbaselinecheck_obj.setMain(self)
        self.registerbaselinecheck_obj.show()

    @pyqtSlot()
    def on_actionFan_Test_triggered(self):
        """
        Slot documentation goes here.
        """
        self.fan_temp_test_obj=FanAndTempTest()
        self.fan_temp_test_obj.setMain(self)
        self.fan_temp_test_obj.show()
###脚本工具####
    @pyqtSlot()
    def on_actionPython_triggered(self):
        """
        Slot documentation goes here.
        """
        self.selectpythons=selectpythonscript(self)
        self.selectpythons.setMain(self)
        # self.crt=CRT()
        # self.crt.setMain(self)
        # print('%-25s: %s, %s,' % ("mainwind_actionscript_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("mainwind_actionscript_slot", threading.current_thread().name, threading.current_thread().ident))
         
        self.selectpythons.show()
        # self.selectpythons.exec_()


###工具栏按键###
    @pyqtSlot()
    def on_actionAddTest_triggered(self):
        """
        按下工具栏上的+按钮，开始添加测试命令到测试序列
        """
        #print("按下添加测试")
        self.sendCommand = AddSendCommandWidgetandWaitingEcho(self)  #从mainwindow继承，这样可以让窗口始终在mainwindow上方。
        self.sendCommand.setMain(self)
        self.sendCommand.show()
        
    @pyqtSlot()
    def on_actionSettingDelay_triggered(self):
        """
        添加延时
        """
        #print("按下添加延时")
        settingDelay = AddDelayDialog()
        settingDelay.setMain(self)
        settingDelay.exec_()
    
    @pyqtSlot()
    def on_actionLogRecognition_triggered(self):
        """
        添加log识别指令
        """
        #print("按下log识别")
        logRecognition = DialogCharacterRecognition()
        logRecognition.setMain(self)
        logRecognition.exec_()
    
    @pyqtSlot()
    def on_actionSpecialTest_triggered(self):
        """
        按下添加特殊测试
        """
        #print("按下添加特殊测试")
    
    @pyqtSlot()
    def on_actionExpertScan_triggered(self):
        """
        按下高级log扫描
        """
        #print("按下高级log扫描")
    
    @pyqtSlot()
    def on_actionDeleteTest_triggered(self):
        """
        按下删除单项测试
        """
        #print("按下删除单项测试")

    @pyqtSlot()
    def on_actionAddQuickCommand_triggered(self):
        """
        添加快速发送命令
        """
        # print("按下工具栏添加快速命令")
        addquickcommand_obj = AddQuickCommand()
        addquickcommand_obj.setMain(self)
        addquickcommand_obj.exec_()

    @pyqtSlot(QPoint)
    def on_toolBar_quickcommand_customContextMenuRequested(self, pos):
        """
        Slot documentation goes here.
        
        @param pos DESCRIPTION
        @type QPoint
        """
        self.quickcommand_right_menu(QCursor.pos())

#####quickcommand快速命令栏######
    @pyqtSlot()
    def actiontoolbar_sendcommand_triggered(self,command):
        # print("command is :",command)
        char=command+"\r\n"
        #获取最前端激活的窗口
        index = self.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mdiArea.currentSubWindow())
        GlobalVariable.Console[index]["consolethread"].send_trigger.emit(char.encode(GlobalVariable.Console[index]["encodingtype"]))
        # self._serial.write(char.encode(encodingType))

    #工具栏右键菜单    
    def quickcommand_right_menu(self,pos):
        menu = QMenu()
        opt1 = menu.addAction("编辑")
        opt2 = menu.addAction("删除")
        action = menu.exec_(pos)  #self.toolBar_quickcommand.mapToGlobal(pos)
        # # The get the coordinates of the mouse pointer from the event object.
        # # The mapToGlobal() method translates the widget coordinates
        # # to the global screen coordinates.
        # action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == opt1:
            # do something
            # print("opt1")
            GlobalVariable.hoverd_action = ""
            return
        elif action == opt2:
            # 判断悬停的是哪个对象，并删除该对象
            # print("opt2")
            if GlobalVariable.hoverd_action != "" :
                #删除对应的对象
                delete_obj=GlobalVariable.hoverd_action
                # exec(deletecommand)
                delete_obj.deleteLater()
                #更新quickcommand_setting_list
                # quickcommand_setting_list=[]     #快速命令的配置生成信息
                #找quickcommand_setting_list中匹配待删除action的序号
                delete_command=delete_obj.objectName()
                delete_num=None
                for i in range(len(GlobalVariable.quickcommand_setting_list)):
                    for j in range(len(GlobalVariable.quickcommand_setting_list[i])):
                        # print(GlobalVariable.quickcommand_setting_list[i][j])
                        if re.search(delete_command,GlobalVariable.quickcommand_setting_list[i][j]) != None:
                            # print("找到命令列表中的i，j:",i,j)
                            delete_num=i
                if delete_num != None:
                    #删除对应列表中的值
                    GlobalVariable.quickcommand_setting_list.remove(GlobalVariable.quickcommand_setting_list[delete_num])

                    #更新quickcommand_list
                    # quickcommand_list=[]  
                    GlobalVariable.quickcommand_list.remove(GlobalVariable.quickcommand_list[delete_num])
                    #更新quickcommand_namelist
                    # quickcommand_namelist=[]
                    GlobalVariable.quickcommand_namelist.remove(GlobalVariable.quickcommand_namelist[delete_num])
                    #更新quickcommand_number
                    GlobalVariable.quickcommand_number-=1
                    #更新配置文件
                    configfile=open(GlobalVariable.configfilename, 'w+')
                    configfile.truncate()
                    configfile.close()
                    for k in range(len(GlobalVariable.quickcommand_list)):
                        kk=[]
                        kk.append("quickcommand"+str(k)+":{\n")  #开始标志
                        kk.append(GlobalVariable.quickcommand_namelist[k]+"\n")  #快速命令标签命名
                        kk.append(GlobalVariable.quickcommand_list[k]+"\n")  #将quickcommand保存到文件，为了从初始文件中恢复GlobalVariable.quickcommand_list
                        
                        for v in GlobalVariable.quickcommand_setting_list[k]:  #因为有5个才遍历到5，如果更改了数量，需要此处更改
                            kk.append(v + "\n")
                            # kk.append(v[0] + "\n")
                            # kk.append(v[1] + "\n")
                            # kk.append(v[2] + "\n")
                            # kk.append(v[3] + "\n")
                            # kk.append(v[4] + "\n")
                            # #kk.append(v[5] + "\n")
                            
                        kk.append("}"+"quickcommand"+str(k)+"\n")
                        # print("kk:",kk)
                        
                        configfile=open(GlobalVariable.configfilename, 'a+')
                        configfile.writelines(kk)
                        configfile.close()
                #self.abac.deleteLater()
            return
        else:
            # print("opt3")
            GlobalVariable.hoverd_action = ""
            return    
         
#######Sequencer测试序列功能########
    @pyqtSlot()
    def on_run_test_sequence_clicked(self):
        """
        Slot documentation goes here.
        """
        #获取当前激活的终端
        print("当前子窗口是：",self.mdiArea.currentSubWindow())
        if self.mdiArea.currentSubWindow() != None:
            self.current_console_index = self.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mdiArea.currentSubWindow())
            print("当前串口索引值：", self.current_console_index)
            print(GlobalVariable.Console[self.current_console_index])
            if self.current_console_index >= 0:
                #串口线程中发送信号过来，通过sequencer相关的槽函数进行接收
                GlobalVariable.Console[self.current_console_index]["consolethread"].rec_trigger.connect(self.sequencer_receive_data_slot, Qt.QueuedConnection) 

                #新建sequencer线程
                self.sequencer_threadpool.append(QThread())
                self.sequencer_thread = SequencerThreadWorker(GlobalVariable.Console[self.current_console_index]["consolethread"])   #需要传入当前激活的终端名
                self.sequencer_thread.moveToThread(self.sequencer_threadpool[-1])
                self.sequencer_threadpool[-1].started.connect(self.sequencer_thread.sequencer_init)
                self.sequencer_thread.seq_to_main_trigger.connect(self.sequencer_data_to_console_thread_slot, Qt.QueuedConnection)  #
                self.sequencer_thread.main_to_seq_trigger.connect(self.sequencer_thread.received_console_log)
                self.sequencer_threadpool[-1].start() 
                
        else:
            self.textEdit_message.insertPlainText("无可用终端")
            QtWidgets.QMessageBox.warning(self, "提示", "请打开并连接一个终端", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    def sequencer_receive_data_slot(self, serialobj, data):
        # self.sequencer_thread.main_to_seq_trigger.emit(serialobj, data)
        GlobalVariable.log_data_buffer += data
        
    def sequencer_data_to_console_thread_slot(self, current_consolethread, data):
        #把Sequencer发过来的数据发送给对应console线程
        # GlobalVariable.Console[self.current_console_index]["consolethread"].send_trigger.emit(data.encode(GlobalVariable.Console[self.current_console_index]["encodingtype"]))
        current_consolethread.send_trigger.emit(data.encode(GlobalVariable.Console[self.current_console_index]["encodingtype"]))
    
    @pyqtSlot()
    def on_pause_test_sequence_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_move_to_previous_section_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_move_to_next_section_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_stop_test_sequence_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_import_to_sequencer_clicked(self):
        """
        Slot documentation goes here.
        """
        #选择单个excel文件。如果使用的是QFileDialog.getOpenFileNames则可以同时选择多个文件
        choosefilename, _ = QFileDialog.getOpenFileName(self, "选取文件",QStandardPaths.standardLocations(0)[0],
                            "Excel Files (*.xlsx *.xls);;All Files (*)")
        if choosefilename:
            #读取文件
            self.test_sequence = pd.read_excel(choosefilename, sheet_name = '测试用例')
            print("测试序列表格是：\r\n",self.test_sequence)
        self.sequencertable.setRowCount(len(self.test_sequence.index))
        self.sequencertable.setColumnCount(len(self.test_sequence.columns))
        print("index:",len(self.test_sequence.index))
        print("columns:",self.test_sequence.columns) #这个len  columns会多一个
        for i in range(len(self.test_sequence.index)):
            for j in range(len(self.test_sequence.columns)):
                self.sequencertable.setItem(i,j,QTableWidgetItem(str(self.test_sequence.iloc[i,j])))
        
        # print(self.sequencertable.rowCount(),self.sequencertable.columnCount())


    @pyqtSlot()
    def on_update_sequence_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSlot()
    def on_save_sequence_to_txt_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError

    @pyqtSlot()
    def on_add_one_row_clicked(self):
        """
        Slot documentation goes here.
        """
        self.sequencertable.insertRow(self.sequencertable.rowCount())
        print("插入一行")
    
    @pyqtSlot()
    def on_delete_one_row_clicked(self):
        """
        Slot documentation goes here.
        """
        self.sequencertable.removeRow(self.sequencertable.currentRow())
        print("删除一行")




    def rec_comdata_slot(self,serialobj,data):
        """
        接收串口数据的槽函数，并将数据插入到console_terminal上显示
        Args:
            serialobj:线程中的串口对象
            data：线程中串口发送过来的数据
        """
        # print("rec_comdata_slot serialobj is", serialobj)
        index = self.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "serialobj", serialobj)
        
        if index >= 0:
            console_terminal = GlobalVariable.Console[index]["consoleobj"]
            
            #插入文本前需要先把光标移动到最后，否则当光标在中间时，会在文本中间直接插入文本信息
            cursor = console_terminal.textCursor()
            if(cursor != cursor.End):
                cursor.movePosition(cursor.End)
                console_terminal.setTextCursor(cursor)

            console_terminal.insertPlainText(data)   #TODO 是否需要编解码.encode(GlobalVariable.Console[index]["encodingtype"])
            
            cursor = console_terminal.textCursor()
            if(cursor != cursor.End):
                cursor.movePosition(cursor.End)
                console_terminal.setTextCursor(cursor)

    def tryopencom(self):
        self._serial = QSerialPort(self)  # 用于连接串口的对象
        port = self._ports[self.com_option.currentText()]
        # 根据名字设置串口（也可以用上面的函数）
        self._serial.setPortName(port.systemLocation())
        # 设置波特率
        self._serial.setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
            getattr(QSerialPort, 'Baud' + self.baud_rate_option.currentText()))
        # 设置校验位
        self._serial.setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, self.checksum_bits.currentText() + 'Parity'))
        # 设置数据位
        self._serial.setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + self.data_bits.currentText()))
        # 设置停止位
        self._serial.setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, self.stop_bit.currentText()))
        # NoFlowControl          没有流程控制
        # HardwareControl        硬件流程控制(RTS/CTS)
        # SoftwareControl        软件流程控制(XON/XOFF)
        # UnknownFlowControl     未知控制
        self._serial.setFlowControl(QSerialPort.NoFlowControl)

        if self._serial.isOpen():
            # 如果串口是打开状态则关闭
            self._serial.close()
            # print("串口已经打开，关闭串口")
            return False
        elif self._serial.open(QIODevice.ReadWrite) == True:
            # print("串口打开成功说明串口未被占用，先关闭串口")
            self._serial.close()
            return True
        else:
            # print("串口对象是",self._serial)
            # print("串口被占用无法打开")
            self.textEdit_message.insertPlainText("%s串口被占用无法打开\r\n" % self.com_option.currentText())
            return False

    def config_init(self):
        """
        加载初始化配置文件
        """ 
        if  not os.path.exists(GlobalVariable.configfilename): 
            read_line_configfile=open(GlobalVariable.configfilename, "w")
            read_line_configfile.close()
        else: 
            read_line_configfile= open(GlobalVariable.configfilename, "r")
            i=0
            find=0
            commandlist=[]
            for j in read_line_configfile:
                # print("oneline:",j)
                # print("onelinetype:",type(j))
                j=j.replace("\n","")
                if re.search("}quickcommand\d+",j) != None:
                    find=0
                    i=0
                    GlobalVariable.quickcommand_setting_list.append(commandlist)
                    commandlist=[]
                if find==1:   
                    if i==0:  #第0行指令，为了提取标签名到list
                        GlobalVariable.quickcommand_namelist.append(j) 
                        i+=1  
                        continue 
                    if i==1:
                        GlobalVariable.quickcommand_list.append(j) 
                        i+=1  
                        continue 
                    j=j.replace(".mainwindow","")
                    # print(j)
                    # print(GlobalVariable.quickcommand_list)
                    exec(j)
                    commandlist.append(j)
                if re.search("quickcommand\d+:{",j) != None:
                    find=1
                    number=re.findall("(\d+)",j)
                    if number != []:    
                        GlobalVariable.quickcommand_number=int(number[0])+1  #提取命令编号
                    commandlist=[]
            #打印调试
            # print("打印调试quickcommand_setting_list:",GlobalVariable.quickcommand_setting_list)
            
            # print("打印调试quickcommand_list:",GlobalVariable.quickcommand_list)
            
            # print("打印调试quickcommand_namelist:",GlobalVariable.quickcommand_namelist)
            read_line_configfile.close()  


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    testCenter = MainWindow()
    testCenter.show()
    sys.exit(app.exec_())
