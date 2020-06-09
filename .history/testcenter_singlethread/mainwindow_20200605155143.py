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
from PyQt5.QtCore import pyqtSlot, QIODevice, QByteArray,QPoint,QObject
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtWidgets import QWidget,QMainWindow,QFileDialog,QMenu,QApplication
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
from PyQt5.QtCore import QTimer,pyqtSignal,QEvent
import pandas as pd
import re
import threading

from ui_mainwindow import Ui_MainWindow
from myui_mainwindow import MyUi_MainWindow
from subdialog.newtelnet import NewTelnet
from subdialog.vlanconfig import VlanConfig
from subdialog.addsendcommand import AddSendCommandWidgetandWaitingEcho
from subdialog.adddelaydialog import AddDelayDialog
from subdialog.characterrecognition import DialogCharacterRecognition
from subdialog.testcommandillustration import TestCommandIllustration
from subdialog.registerbaselinecheck import RegisterBaseLineCheck
from subdialog.fanandtemptest import FanAndTempTest
from subdialog.addquickcommand import AddQuickCommand
from subdialog.selectpythonscript import selectpythonscript
from AutomationScript import CRT
from serial_thread import SerialThread,SerialConsoleThread
from console_init import ConsoleInit
from subdialog.loganalyzer import LogAnalyzer

from init import Init
from globalvariable import GlobalVariable
from testcommandsessions import TestCommandSession
# from testcommandsessions import testcommandlist
# from testcommandsessions import commandlist_num
# from testcommandsessions import case_num

import logging
from logging import handlers
from datetime import datetime

logger= logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler= logging.handlers.TimedRotatingFileHandler('Testcenter.log',when='midnight',interval=1,backupCount=30)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s ： %(message)s'))
logger.addHandler(handler)


encodingType=GlobalVariable.defaultEncodingType

class NewMdiSubWindow(QtWidgets.QMdiSubWindow):
    """对QMdiSubWindow类重写，实现关闭窗口时执行其他功能"""
    # def __init__(self):
    #     super(NewMdiSubWindow,self).__init__() #parent
        

    def setMain(self, main_window):
        self.mainwindow=main_window

    # def sendanalyze_arg(self,analyzeobj):
    #     self.analyzeobj=analyzeobj
    #     # self.com_threadCounter=comThreadCounter

    def closeEvent(self, event):
        print("准备关闭tab窗口...")
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
                print("线程是否finish",GlobalVariable.Console[index]["threadpool"].isFinished()) #查看线程是否已经finished
                GlobalVariable.Console[index]["threadpool"].deleteLater()

                # self.mainwindow.console_terminal_threadpool.remove(GlobalVariable.Console[index]["threadpool"])
                GlobalVariable.Console.remove(GlobalVariable.Console[index])
                print('关闭后总共有哪些线程：',threading.enumerate())    #查看有哪些线程
                print("串口线程已关闭")
        else:
            event.ignore()

        #     obj_index=GlobalVariable.mdisubwindow_objlist.index(self)
        #     print("当前对象地址：",self)
        #     print('关闭前总共有哪些线程：',threading.enumerate())    #查看有哪些线程
        #     #此处需要关闭线程，删除线程、Mdi窗体、等相关对象的变量值
        #     print("当前线程的comThreadCounter是：",self.com_threadCounter)
        #     self.analyzeobj.rec_trigger.disconnect(self.mainwindow.rec_comdata_slot)  #
        #     self.analyzeobj.send_trigger.disconnect(self.analyzeobj.sendto_comdata_slot)

        #     print("销毁前线程池：",self.mainwindow.console_terminal_threadpool)
        #     print("销毁前线程对象:",self.mainwindow.analyze)
        #     print("销毁前子窗口：",self.mainwindow.subwindow)
        #     print("销毁前计数：",GlobalVariable.comThreadCounter)

        #     print("待销毁的线程是：", QThread.currentThread(),self.mainwindow.console_terminal_threadpool[obj_index])

        #     self.mainwindow.console_terminal_threadpool[obj_index].quit()
        #     self.mainwindow.console_terminal_threadpool[obj_index].wait()
        #     print("线程是否finish",self.mainwindow.console_terminal_threadpool[obj_index].isFinished()) #查看线程是否已经finished
        #     self.mainwindow.console_terminal_threadpool[obj_index].deleteLater()
            
        #     print("销毁后线程池：",self.mainwindow.console_terminal_threadpool)
        #     print("销毁后线程对象:",self.mainwindow.analyze)
        #     print("销毁后子窗口：",self.mainwindow.subwindow)
        #     print("销毁后计数：",GlobalVariable.comThreadCounter)
        #     print("MDIsubwin_objlist:",GlobalVariable.mdisubwindow_objlist)
        #     print("opencom_objlist:",GlobalVariable.opencom_objlist)
        #     print("opencom_list:",GlobalVariable.opencomlist)
        #     print("subwin对象的索引：",GlobalVariable.mdisubwindow_objlist.index(self))
            
        #     print("对象列表索引是：",obj_index)
        #     print("待关闭串口是：",GlobalVariable.opencom_objlist[obj_index],GlobalVariable.opencom_objlist)
        #     GlobalVariable.serial[obj_index].close() #关闭串口
        #     GlobalVariable.opencom_objlist.remove(GlobalVariable.opencom_objlist[obj_index])
        #     GlobalVariable.opencomlist.remove(GlobalVariable.opencomlist[obj_index])
        #     GlobalVariable.mdisubwindow_objlist.remove(self)
        #     print("待关闭串口是：",GlobalVariable.opencom_objlist)

            
            

        #     print("MDIsubwin_objlist:",GlobalVariable.mdisubwindow_objlist)
        #     print("opencom_objlist:",GlobalVariable.opencom_objlist)
        #     print("opencom_list:",GlobalVariable.opencomlist)
            
        #     self.mainwindow.analyze.remove(self.mainwindow.analyze[obj_index])
        #     self.mainwindow.console_terminal_threadpool.remove(self.mainwindow.console_terminal_threadpool[obj_index])
        #     self.mainwindow.subwindow.remove(self.mainwindow.subwindow[obj_index])
        #     GlobalVariable.comThreadCounter-=1

        #     print('关闭后总共有哪些线程：',threading.enumerate())    #查看有哪些线程
        #     print("串口线程已关闭")
        # else:
        #     event.ignore()
        
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
            index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "console_terminal", obj)
            if  index >= 0:
                consolethread = GlobalVariable.Console[index]["consolethread"]
            # if obj in GlobalVariable.opencom_objlist:
            #if self.serial != None:
                if event.key() == QtCore.Qt.Key_Up:
                    send_list = []
                    send_list.append(0x1b)
                    send_list.append(0x5b)
                    send_list.append(0x41)
                    input_s = bytes(send_list)
                    #print("转换前", send_list)
                    #print("转换后", input_s)
                    #self.console_terminal.
                    #self.serial.write(input_s)
                    consolethread.send_trigger.emit(input_s)
                elif event.key() == QtCore.Qt.Key_Down:
                    #down 0x1b5b42 向下箭头
                    send_list = []
                    send_list.append(0x1b)
                    send_list.append(0x5b)
                    send_list.append(0x42)
                    input_s = bytes(send_list)
                    #self.serial.write(input_s)
                    consolethread.send_trigger.emit(input_s)
                elif event.key() == QtCore.Qt.Key_Backspace:   #删除键处理，目前对于命令的删除还未做处理，无法进行命令删除编辑等
                    send_list = []
                    send_list.append(0x08)
                    input_s = bytes(send_list)
                    # print("back转换前", send_list)
                    # print("back转换后", input_s)
                    #self.serial.write(input_s)
                    consolethread.send_trigger.emit(input_s)

                    # terminal_cursor = self.console_terminal[self.com_threadCounter].textCursor()#注意textCursor是一个类，因此要新建一个对象
                    # if terminal_cursor.hasSelection():
                    #     terminal_cursor.movePosition(QTextCursor.NoMove, QTextCursor.KeepAnchor, terminal_cursor.selectionStart() - terminal_cursor.selectionStart())
                    # else:
                    #     terminal_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, 1)
                    # self.console_terminal[self.com_threadCounter].setTextCursor(terminal_cursor)
                    # self.console_terminal[self.com_threadCounter].cut()
#                    
#                    
#                    #self.console_terminal.cut()
#                    cursor = self.console_terminal.textCursor()#注意textCursor是一个类，因此要新建一个对象
#                    self.console_terminal.moveCursor(QTextCursor.Left, QTextCursor.KeepAnchor)
#                    cursor.removeSelectedText()
#                    print('删除一个字符', cursor)
#                    print(self.console_terminal.cursorForPosition())
#                    cursor.movePosition(cursor.Left)
#                    self.console_terminal.setTextCursor(cursor)
#                    print('删除移动后', cursor)
#                    print(self.console_terminal.cursorForPosition())
#                    self.console_terminal.setTextCursor(cursor)
                    #self.console_terminal.setFocus()
#                    cursor = self.console_terminal.textCursor()
#                    if(cursor != cursor.End):
#                        cursor.movePosition(cursor.End)
#                        self.console_terminal.setTextCursor(cursor)
                   
                else:    
                    #获取按键对应的字符
                    char = event.text()
                    #print('获取的按键值：', char)
                    #self.serial.write(char.encode(encodingType))
                    try:
                        # self.analyzeobj.send_trigger.emit(char.encode(encodingType))
                        consolethread.send_trigger.emit(char.encode(encodingType))
                    except Exception :
                        print("发送字符信号发射出错")
                    print('%-25s: %s, %s,' % ("mainwin_event", QThread.currentThread(), int(QThread.currentThreadId())))
                    print('%-25s: %s, %s,' % ("mainwin_event", threading.current_thread().name, threading.current_thread().ident))
                    


#                self.send_num = self.send_num + num
#                dis = '发送：'+ '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
#                self.statusBar.showMessage(dis)
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
        # self.serialreaddata=""
        GlobalVariable.mainwindow=self
        # self.crt=CRT()
        # self.crt.setMain(self)
        self.console_terminal_threadpool=[] #创建一个空线程池管理线程
        # self.subwindow=[]
        # self.console_terminal=[]
        self.analyze=[]
        self.toolBar_quickcommand.setContextMenuPolicy(Qt.CustomContextMenu)
        #加载初始化配置文件,初始化窗体等
        try:
            self.init=Init()
            self.init.config_init()
        except Exception :
            QMessageBox.critical(self,'critical','初始化配置文件出错，请删除程序目录下的config.ini初始化配置文件后重试')

        #控制台接收数据Queue
        
        self.getAvailablePorts()
        self.open_close_buttom.setStyleSheet("color:rgb(255, 0, 0);\n"
"font: 9pt \"黑体\";\n"
"selection-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        

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

        """#将该段全部移植到独立的串口线程文件中
        self.serial = QSerialPort(self)  # 用于连接串口的对象
        self.serial.setReadBufferSize(4096) #设置内部接收缓存区大小
        self.serial.readyRead.connect(self.onReadyRead)  # 绑定数据读取信号
        #self._serial.getData.connect(self.on_send_button_clicked)  # 绑定写数据信号
        # 首先获取可用的串口列表
        self.getAvailablePorts()
        #self.labelStatus.setProperty("isOn", False)
        #MainWindow.setStyleSheet(self,"#labelStatus{border-radius:20px;background-color:gray;}""#labelStatus[isOn=\"true\"]{background-color: green;}")    
        self.open_close_buttom.setStyleSheet("color:rgb(255, 0, 0);\n"
"font: 9pt \"黑体\";\n"
"selection-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
            
        self.send_num = 0
        self.receive_num = 0
        
        #测试命令序列处理
        #self.TestCommandSessions


        #对console_terminal进行事件过滤
        self.console_terminal.installEventFilter(self)

        self.console_terminal.selectionChanged.connect(self.textCopy)  #选择文本自动复制
        # self.console_terminal.copyAvailable.connect(self.textCopy) #双击文本自动复制
#
#        self.timer_send= QTimer(self)
#        #定时器调用读取串口接收数据
#        self.timer.timeout.connect(self.recv)
#
        #实例化一个定时器
        self.timer_send = QTimer(self)
        #定时发送
        self.timer_send.timeout.connect(self.on_send_button_clicked)
        将该段全部移植到独立的串口线程文件中"""

        #使用快速命令时连接信号与槽函数的方法：
        # command="show versi"
        # self.actionshow_version.triggered.connect(lambda: self.show_version_triggered(command))

        #测试VT102库是否可用----测试OK
        # self.stream.process(u"\u001b7\u001b[?47h\u001b)0\u001b[H\u001b[2J\u001b[H" +
        #        u"\u001b[2;1HNetHack, Copyright 1985-2003\r\u001b[3;1" +
        #        u"H         By Stichting Mathematisch Centrum and M. " +
        #        u"Stephenson.\r\u001b[4;1H         See license for de" +
        #        u"tails.\r\u001b[5;1H\u001b[6;1H\u001b[7;1HShall I pi" +
        #        u"ck a character's race, role, gender and alignment f" +
        #        u"or you? [ynq] ")
        # self.console_terminal.insertPlainText(str(self.screen))
    # def textCopy(self):  #选择文本自动复制
    #     self.console_terminal.copy()
        # command = QApplication.clipboard().text().upper()
        # print(command)

    # def textCopy(self,status):  #双击文本自动复制
    #     if status == True:
    #         self.console_terminal.copy()
    #         command = QApplication.clipboard().text().upper()
    #         print(command)


    def action_hoverd(self,actionis):
        print("hoverd action is: " , actionis)
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
                print("%s--%s" % (key,dictionarylist[index][key]))
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
        print("打开串口前是否在字典列表里找到：",self.find_dictionarylist_keyvalue_index(GlobalVariable.Console,"name",self.com_option.currentText()))
        if self.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.com_option.currentText()) < 0:
            if self.tryopencom() == True: #尝试打开串口，串口没打开则新建串口线程
                #创建一个MDIarea的sub窗口
                subwindow = NewMdiSubWindow()   #subwindow对象
                subwindow.setMain(self)

                # 向sub内部添加QTextEdit控件
                subwindow.setWidget(QtWidgets.QTextEdit())
                subwindow.widget().insertPlainText("%s is %s\r\n" % (GlobalVariable.Console,subwindow))
                #QTextEdit控件 对象
                console_terminal=subwindow.widget()
                # console_terminal.insertPlainText("self.consoleT_insert\r\n")

                #对console_terminal进行事件过滤
                console_terminal.installEventFilter(subwindow)

                #对终端设置window标题
                if self.renameconsole.text() != "":
                    subwindow.setWindowTitle(self.renameconsole.text())
                else:
                    subwindow.setWindowTitle(self.com_option.currentText())
                self.mdiArea.addSubWindow(subwindow)
                
                subwindow.setAttribute(Qt.WA_DeleteOnClose) #设置subwindow属性，当点击关闭时删除对象
                subwindow.setWindowFlags(Qt.WindowTitleHint)
                subwindow.show()

                GlobalVariable.SelectCom=self.com_option.currentText()
                # print("selectCOM is:",GlobalVariable.SelectCom)
                # print("port是:",self._ports[self.com_option.currentText()])
                GlobalVariable.setting_stop_bit=self.stop_bit.currentText()
                GlobalVariable.setting_data_bits= self.data_bits.currentText()
                GlobalVariable.setting_checksum_bits=self.checksum_bits.currentText()
                GlobalVariable.setting_baud_rate_option= self.baud_rate_option.currentText()

                print('%-25s: %s, %s,' % ("mainwindow_slot", QThread.currentThread(), int(QThread.currentThreadId())))
                print('%-25s: %s, %s,' % ("mainwindow_slot", threading.current_thread().name, threading.current_thread().ident))
                
                #创建新线程，初始化一个串口
                self.console_terminal_threadpool.append(SerialThread())
                consolethread=SerialConsoleThread(self.com_option.currentText())  #需要传入打开的串口名self.com_option.currentText()
                consolethread.moveToThread(self.console_terminal_threadpool[-1])
                self.console_terminal_threadpool[-1].started.connect(consolethread.serial_init)
                consolethread.rec_trigger.connect(self.rec_comdata_slot,Qt.QueuedConnection)  #
                consolethread.send_trigger.connect(consolethread.sendto_comdata_slot)
                self.console_terminal_threadpool[-1].start() 

                #保存所有参数到GlobalVariable.Console字典列表
                consoledict={"type":"serial",  
                            "name":self.com_option.currentText(), "customname": self.renameconsole.text(),
                            "subwindowobj": subwindow, "consoleobj":console_terminal,
                            "consolethread":consolethread, "threadpool":self.console_terminal_threadpool[-1]
                            }
                GlobalVariable.Console.append(consoledict)
                # print("consoledictlist is :", GlobalVariable.Console)

                # consolethread.send_trigger.emit("test_emit:".encode(encodingType))
                # subwindow.sendanalyze_arg(consolethread)
                # self.console_terminal[comThreadCounter].selectionChanged.connect(lambda: self.console_terminal[comThreadCounter].copy())  #选择文本自动复制
                
                self.statusbar.showMessage("")
                return True  #创建串口线程成功
        else:
            # print(self.com_option.currentText(),"串口已经打开了")
            self.statusbar.showMessage("串口已经打开了")
            self.textEdit_message.insertPlainText("%s串口已经打开了\r\n" % self.com_option.currentText())


        # if self.com_option.currentText() in GlobalVariable.opencomlist:
        #     #说明串口已经打开了
        #     print(self.com_option.currentText(),"串口已经打开了")
        #     self.statusbar.showMessage("串口已经打开了")
        #     self.textEdit_message.insertPlainText("%s串口已经打开了\r\n" % self.com_option.currentText())
            
        # elif self.tryopencom() == True: #尝试打开串口，串口没打开则新建串口线程
        #     try:
        #         if self.console_terminal_threadpool[GlobalVariable.comThreadCounter] != None:
        #             GlobalVariable.comThreadCounter+=1
        #             self.console_terminal_threadpool.append(None)
        #     except Exception:
        #         self.console_terminal_threadpool.append(None)

        #     if self.console_terminal_threadpool[GlobalVariable.comThreadCounter] == None:
        #         print("开始创建com线程")
        #         ok=self.newCom_MdiThread(GlobalVariable.comThreadCounter) 
        #         if ok == True:
        #             GlobalVariable.comThreadCounter+=1
        #         else:
        #             pass  #创建串口线程不成功，需要另外处理
        #     else:
        #         print("当前线程池不为空")
        #         self.console_terminal_threadpool.append(None)
        #         ok=self.newCom_MdiThread(GlobalVariable.comThreadCounter+1) 
        #         if ok == True:
        #             GlobalVariable.comThreadCounter+=1
        #         else:
        #             pass  #创建串口线程不成功，需要另外处理
                
    
    # def newCom_MdiThread(self,comThreadCounter):  #新建Mdi页串口和新线程
    #     #创建一个MDIarea的sub窗口
    #     try:
    #         self.subwindow[comThreadCounter] = NewMdiSubWindow()
    #     except Exception:
    #         self.subwindow.append(None)
    #         self.subwindow[comThreadCounter] = NewMdiSubWindow()
    #     self.subwindow[comThreadCounter].setMain(self)
        
    #     # 向sub内部添加QTextEdit控件
    #     self.subwindow[comThreadCounter].setWidget(QtWidgets.QTextEdit())
    #     # print("subwidget_objname:",sub.widget().objectName())
    #     self.subwindow[comThreadCounter].widget().insertPlainText("%d is %s\r\n" % (comThreadCounter,self.subwindow[comThreadCounter]))
        
    #     try:
    #         self.console_terminal[comThreadCounter]=self.subwindow[comThreadCounter].widget()
    #     except Exception:
    #         self.console_terminal.append(None)
    #         self.console_terminal[comThreadCounter]=self.subwindow[comThreadCounter].widget()

    #     # print("self.console_terminal",self.console_terminal)
    #     # print("self.cstext_cur",self.console_terminal.textCursor())
    #     self.console_terminal[comThreadCounter].insertPlainText("self.consoleT_insert\r\n")
        

    #     GlobalVariable.mdisubwindow_objlist.append(self.subwindow[comThreadCounter])
    #     GlobalVariable.opencom_objlist.append(self.console_terminal[comThreadCounter])  #####临时放这里！！！
    #     #对console_terminal进行事件过滤
    #     self.console_terminal[comThreadCounter].installEventFilter(self.subwindow[comThreadCounter])

    #     self.subwindow[comThreadCounter].setWindowTitle(self.com_option.currentText())
    #     self.mdiArea.addSubWindow(self.subwindow[comThreadCounter])
    #     # objectname="subwindow"+str(self.count+1)
    #     # sub.setObjectName(objectname)
    #     self.subwindow[comThreadCounter].setAttribute(Qt.WA_DeleteOnClose) #设置subwindow属性，当点击关闭时删除对象
    #     self.subwindow[comThreadCounter].setWindowFlags(Qt.WindowTitleHint)
    #     self.subwindow[comThreadCounter].show()

    #     #将选项卡中的com名传递到线程内
    #     GlobalVariable.SelectCom=self.com_option.currentText()
    #     print("selectCOM is:",GlobalVariable.SelectCom)
    #     # GlobalVariable.SelectComINFO=self._ports[self.com_option.currentText()]
    #     print("port是:",self._ports[self.com_option.currentText()])
    #     GlobalVariable.setting_stop_bit=self.stop_bit.currentText()
    #     GlobalVariable.setting_data_bits= self.data_bits.currentText()
    #     GlobalVariable.setting_checksum_bits=self.checksum_bits.currentText()
    #     GlobalVariable.setting_baud_rate_option= self.baud_rate_option.currentText()

    #     print('%-25s: %s, %s,' % ("mainwindow_slot", QThread.currentThread(), int(QThread.currentThreadId())))
    #     print('%-25s: %s, %s,' % ("mainwindow_slot", threading.current_thread().name, threading.current_thread().ident))
    #     #创建新线程，初始化一个串口
    #     # self.console_terminal_threadpool[comThreadCounter] = None
    #     self.console_terminal_threadpool[comThreadCounter] = SerialThread() #self.com_option.currentText()
    #     try:
    #         self.analyze[comThreadCounter]=SerialConsoleThread(comThreadCounter)
    #     except Exception:
    #         self.analyze.append(None)
    #         self.analyze[comThreadCounter]=SerialConsoleThread(comThreadCounter)
    #     self.analyze[comThreadCounter].moveToThread(self.console_terminal_threadpool[comThreadCounter])
    #     self.console_terminal_threadpool[comThreadCounter].started.connect(self.analyze[comThreadCounter].serial_init)
    #     self.analyze[comThreadCounter].rec_trigger.connect(self.rec_comdata_slot,Qt.QueuedConnection)  #
    #     self.analyze[comThreadCounter].send_trigger.connect(self.analyze[comThreadCounter].sendto_comdata_slot)
    #     self.console_terminal_threadpool[comThreadCounter].start() 

    #     self.subwindow[comThreadCounter].sendanalyze_arg(self.analyze[comThreadCounter],comThreadCounter)
    #     # self.console_terminal[comThreadCounter].selectionChanged.connect(lambda: self.console_terminal[comThreadCounter].copy())  #选择文本自动复制
    #     # self.analyze.send_trigger.emit("test_emit:".encode(encodingType))
    #     return True  #创建串口线程成功
        """
        if self.serial.isOpen():
            # 如果串口是打开状态则关闭
            self.serial.close()
            self.console_terminal.append('串口已关闭')        #textBrowser.append('串口已关闭')
            logger.info("串口已关闭")
            self.open_close_buttom.setText('点击打开串口')
            #self.labelStatus.setProperty('isOn', False)
            #self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
            self.open_close_buttom.setStyleSheet("color:rgb(255, 0, 0);\n"
"font: 9pt \"黑体\";\n"
"selection-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
            
            return
        """

        #发送连接串口信号在线程中配置串口
        """
        # 根据配置连接串口
        port = self._ports[self.com_option.currentText()]
        print("port:",port)
#         self._serial.setPort(port)
        # 根据名字设置串口（也可以用上面的函数）
        self.serial.setPortName(port.systemLocation())
        print("syslocation:",port.systemLocation())
        # 设置波特率
        self.serial.setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
            getattr(QSerialPort, 'Baud' + self.baud_rate_option.currentText()))
        # 设置校验位
        self.serial.setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, self.checksum_bits.currentText() + 'Parity'))
        # 设置数据位
        self.serial.setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + self.data_bits.currentText()))
        # 设置停止位
        self.serial.setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, self.stop_bit.currentText()))

        # NoFlowControl          没有流程控制
        # HardwareControl        硬件流程控制(RTS/CTS)
        # SoftwareControl        软件流程控制(XON/XOFF)
        # UnknownFlowControl     未知控制
        self.serial.setFlowControl(QSerialPort.NoFlowControl)
        # 读写方式打开串口
        ok = self.serial.open(QIODevice.ReadWrite) 
        print(ok)
        """
        """
        if ok:
            self.console_terminal.append('打开串口成功')
            logger.info("打开串口成功")
            self.statusbar.showMessage("打开串口成功")
            self.open_close_buttom.setText('点击关闭串口')
            #self.labelStatus.setProperty('isOn', True)
            #self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
            self.open_close_buttom.setStyleSheet("color:rgb(0, 0, 255);\n"
"font: 9pt \"黑体\";\n"
"selection-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        
            #状态栏显示串口信息
            self.statusbar.showMessage("Connected in %s of %s "% (getattr(QSerialPort, 'Baud' + self.baud_rate_option.currentText()),self.com_option.currentText()))
            self.clientSetting.close() 

        else:
            self.console_terminal.append('打开串口失败')
            logger.info("打开串口失败")
            self.statusbar.showMessage("打开串口失败")
            self.open_close_buttom.setText('点击打开串口')
            #self.labelStatus.setProperty('isOn', False)
            #self.labelStatus.style().polish(self.labelStatus)  # 刷新样式
            self.open_close_buttom.setStyleSheet("color:rgb(255, 0, 0);\n"
"font: 9pt \"黑体\";\n"
"selection-color: qconicalgradient(cx:0, cy:0, angle:135, stop:0 rgba(255, 255, 0, 69), stop:0.375 rgba(255, 255, 0, 69), stop:0.423533 rgba(251, 255, 0, 145), stop:0.45 rgba(247, 255, 0, 208), stop:0.477581 rgba(255, 244, 71, 130), stop:0.518717 rgba(255, 218, 71, 130), stop:0.55 rgba(255, 255, 0, 255), stop:0.57754 rgba(255, 203, 0, 130), stop:0.625 rgba(255, 255, 0, 69), stop:1 rgba(255, 255, 0, 69));")
        
        #MainWindow.setStyleSheet(self,"#labelStatus{border-radius:20px;background-color:gray;}""#labelStatus[isOn=\"true\"]{background-color: green;}")    
        """
  
    @pyqtSlot()
    def on_send_button_clicked(self):
        if self.timer_send_checkbox.checkState():
            self.sendtoconsole()
        else:
            self.sendtoconsole()
            #清空发送区
            self.plainTextEdit.clear()
            
    def sendtoconsole(self):
        # 发送消息
        if not self._serial.isOpen():
            print('串口未连接')
            return
        text = self.plainTextEdit.toPlainText()
        if not text:
            return
        """
        以下代码引入VT102后 需要修改
        """
        #print('发送数据前:', text)
        #print('切片数据前:', type(text))
        text=text.split('\n')
        #print('切片后:', text)
        #print('切片后:', type(text))
        text2 = []
        #print('初始化text2:', text2)
        for index in range(len(text)):
            text2.append(text[index])   #encode('utf-8')   'gb2312' emmm windows 测试的工具貌似是这个编码
        #print('发送前:', text2)
        #print('发送前:', type(text2))
        
        if self.hex_send.isChecked():
            # 如果勾选了hex发送            
            
            text = text.toHex()
        # 发送数据
        #print('发送数据:', text2)
        for key2 in range(len(text2)):
            #print("准备发送：",text2[key2])
            self._serial.write(QByteArray((text2[key2].strip()+'\r').encode('gb2312')))
            #print("发送：",text2[key2].encode('gb2312'))
            
        
        #显示发送与接收的字符数量
                
        #在状态栏显示收发数量
        #dis = '发送：'+ '{:d}'.format(self.send_num) + '  接收:' + '{:d}'.format(self.receive_num)
        #dis=5
        #self.statusbar.showMessage(dis)
        
        #采用VT102终端后 此段删除
        #将光标移动到最后--此处接收控件应该是QTextEdit，注意区别，需要用console_terminal对象
        cursor = self.console_terminal.textCursor()
        if(cursor != cursor.End):
            cursor.movePosition(cursor.End)
            self.console_terminal.setTextCursor(cursor)
            #print('光标已移动到最后')

            
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
    def on_clear_button_clicked(self):
        """
        清除接收显示
        """
        self.console_terminal.clear()
        #self.clear_button.clicked.connect(self.textBrowser.clear)

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
    def on_btnSaveLog_clicked(self):
        """
        点击保存log
        """
        fileName, type = QFileDialog.getSaveFileName(self, "Save as", os.getcwd(),   
            "Log files (*.log);;Text files (*.txt);;All files (*.*)")
        if fileName:
            import codecs
            f = codecs.open(fileName, 'w', 'utf-8')
            f.write(self.console_terminal.toPlainText())
            f.close()

        
    # @pyqtSlot(QTreeWidgetItem, int)
    # def on_treeWidget_itemClicked(self, item, column):
    #     """
    #     Slot documentation goes here.
        
    #     @param item DESCRIPTION
    #     @type QTreeWidgetItem
    #     @param column DESCRIPTION
    #     @type int
    #     """
    #     print("item clicked")   
    #     self.plainTextEdit.clear()
    #     if (self.treeWidget.topLevelItem(0).child(0).checkState(0) ==2):
    #         #print("测试0")
    #         self.plainTextEdit.insertPlainText('\r\n')
    #         self.plainTextEdit.insertPlainText('en\r\n')
    #         self.plainTextEdit.insertPlainText('show version\r\n')
    #         self.plainTextEdit.insertPlainText('show manu\r\n')
    #     if (self.treeWidget.topLevelItem(0).child(1).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('show version slot\r\n')
            
            
    #     if (self.treeWidget.topLevelItem(0).child(2).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('show cpld version\r\n')
            
    #     if (self.treeWidget.topLevelItem(0).child(3).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('dir\r\n')
    #     if (self.treeWidget.topLevelItem(0).child(4).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('show clock\r\n')
    #         self.plainTextEdit.insertPlainText('clock set 18:00:00 01 01 2019\r\n')
    #     if (self.treeWidget.topLevelItem(0).child(5).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('con\r\n')
    #         self.plainTextEdit.insertPlainText('int r gi0/1\r\n')
    #         self.plainTextEdit.insertPlainText('no switchport\r\n')
    #         self.plainTextEdit.insertPlainText('ip address 10.10.10.1 255.255.255.0\r\n')
    #         self.plainTextEdit.insertPlainText('show ip interface\r\n')
    #         self.plainTextEdit.insertPlainText('no ip address\r\n')
    #         self.plainTextEdit.insertPlainText('switchport\r\n')
            
    #     if (self.treeWidget.topLevelItem(0).child(6).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('switchport\r\n')
    #         self.plainTextEdit.insertPlainText('mac-address-table static \
    #         00d0.f800.1001 vlan 1 interface gi00/1\r\n')
    #         self.plainTextEdit.insertPlainText('show mac-address-table static\r\n')
    #         self.plainTextEdit.insertPlainText('no mac-address-table static \
    #         00d0.f800.1001 vlan 1 interface gi0/1\r\n')
    #         self.plainTextEdit.insertPlainText('show mac-address-table static\r\n')
    #     if (self.treeWidget.topLevelItem(0).child(7).checkState(0)==2):   
    #         print('poe测试')
            
    #     if (self.treeWidget.topLevelItem(0).child(8).checkState(0)==2):
    #         self.plainTextEdit.insertPlainText('int r gi0/1\r\n')
    #         self.plainTextEdit.insertPlainText('speed ?\r\n')#根据读取到的速率进行相应的设置
    #         pass
    #         self.plainTextEdit.insertPlainText('speed 1000\r\n')#配置速率1000M
    #         self.plainTextEdit.insertPlainText('show int status\r\n')
    #         #弹出对话框提示等待几秒，接着切换下一个速率进行测试
            
    #     if (self.treeWidget.topLevelItem(0).child(9).checkState(0)==2): 
    #         print('扩展模块测试')
    #         self.plainTextEdit.insertPlainText('show version slot\r\n')
            
    #     if (self.treeWidget.topLevelItem(0).child(10).checkState(0)==2): 
    #         print('连通性测试')
        
    #     if (self.treeWidget.topLevelItem(0).child(11).checkState(0)==2): 
    #         print('cpld在线升级测试')
        
    #     if (self.treeWidget.topLevelItem(0).child(12).checkState(0)==2): 
    #         print('风扇模块测试')
    #         self.plainTextEdit.insertPlainText('show fan\r\n')
    #         self.plainTextEdit.insertPlainText('show fan speed\r\n')
    #         self.plainTextEdit.insertPlainText('show fan detail\r\n')
    #     if (self.treeWidget.topLevelItem(0).child(13).checkState(0)==2): 
    #         print('电源模块测试')
    #         self.plainTextEdit.insertPlainText('show power\r\n')
            
    #     if (self.treeWidget.topLevelItem(0).child(14).checkState(0)==2): 
    #         print('USB接口测试')
    #         self.plainTextEdit.insertPlainText('en\r\n')
    #         self.plainTextEdit.insertPlainText('show usb\r\n')
    #         self.plainTextEdit.insertPlainText('dir usb0\r\n')
    #         #复制一组不同大小的文件到交换机，显示后，再删除
    #         self.plainTextEdit.insertPlainText('copy flash:/config.txt usb0\r\n')
    #         self.plainTextEdit.insertPlainText('dir usb0\r\n')
    #         self.plainTextEdit.insertPlainText('del usb0:/config.txt\r\n')
    #     if (self.treeWidget.topLevelItem(0).child(15).checkState(0)==2): 
    #         print('SD卡接口测试')
            
    #     if (self.treeWidget.topLevelItem(0).child(16).checkState(0)==2): 
    #         print('复位测试')#最好放置到最后额外测试，需要反复重启多次
    #         self.plainTextEdit.insertPlainText('en\r\n')
    #         self.plainTextEdit.insertPlainText('reload\r\n')
    #         self.plainTextEdit.insertPlainText('y\r\n')
        
    #     if (self.treeWidget.topLevelItem(0).child(17).checkState(0)==2): 
    #         print('reset按键测试')#弹出对话提示测试人员按下reset按键
            
    #     if (self.treeWidget.topLevelItem(0).child(18).checkState(0)==2): 
    #         print('黏贴命令测试')#原则上上面测试已经包含
            
    #     if (self.treeWidget.topLevelItem(0).child(19).checkState(0)==2): 
    #         print('指示灯测试')#弹出对话框提示测试人员查看各指示灯是否正常，并切换速率查看端口与MGMT
            
    #     if (self.treeWidget.topLevelItem(0).child(20).checkState(0)==2): 
    #         print('VSL链路测试')#
            
    #     if (self.treeWidget.topLevelItem(0).child(21).checkState(0)==2): 
    #         print('MGMT口生测下测试')#切换到生测下用自环线进行MGMT口测试
            
    #     if (self.treeWidget.topLevelItem(0).child(22).checkState(0)==2): 
    #         print('整机测试说明文档测试项测试')#查看整机测试说明中有哪些附加测试项
           
    @pyqtSlot()
    def on_timer_send_checkbox_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.timer_send_checkbox.checkState():
            try:
                time = self.timer_lineEdit.text()
                print(time)
                time_val = int(time, 10) #base=10 十进制
                print(time_val)
                if time_val == 0:
                    QMessageBox.critical(self, 'pycom','定时时间必须大于零!')
                    return None
                else:
                    #定时间隔发送
                    self.timer_send.start(time_val)
            except  Exception:
                QMessageBox.critical(self, 'pycom','请输入有效的定时时间!')
                return    
        else:
            self.timer_send.stop()

    @pyqtSlot()
    def on_timer_lineEdit_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.on_timer_send_checkbox_clicked()

    @pyqtSlot()
    def on_actionvlan_triggered(self):
        """
        vlan配置
        """
        vlanConfig1 = VlanConfig()  #由于不需要设置任何对象的属性，所以不需要参数
        vlanConfig1.setMain(self)
        vlanConfig1.exec_()
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
        Slot documentation goes here.
        """
        if self.active_serial_setting.isChecked()==True:
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
        # print("visibility_change")
        # print(self.clientSetting.isHidden())
        if self.clientSetting.isHidden()==True:
            self.active_serial_setting.setChecked(0)    
        else :
            self.active_serial_setting.setChecked(1)

    @pyqtSlot()
    def on_active_sequencer_triggered(self):
        """
        Slot documentation goes here.
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
        print('%-25s: %s, %s,' % ("mainwind_actionscript_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("mainwind_actionscript_slot", threading.current_thread().name, threading.current_thread().ident))
         
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
        print("按下工具栏添加快速命令")
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
            print("opt1")
            GlobalVariable.hoverd_action = ""
            return
        elif action == opt2:
            # 判断悬停的是哪个对象，并删除该对象
            print("opt2")
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
                        print(GlobalVariable.quickcommand_setting_list[i][j])
                        if re.search(delete_command,GlobalVariable.quickcommand_setting_list[i][j]) != None:
                            print("找到命令列表中的i，j:",i,j)
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
                        print("kk:",kk)
                        
                        configfile=open(GlobalVariable.configfilename, 'a+')
                        configfile.writelines(kk)
                        configfile.close()
                #self.abac.deleteLater()
            return
        else:
            print("opt3")
            GlobalVariable.hoverd_action = ""
            return    
         
    def rec_comdata_slot(self,serialobj,data):
        """
        接收串口数据的槽函数，并将数据插入到console_terminal上显示
        Args:
            serialobj:线程中的串口对象
            data：线程中串口发送过来的数据
        """
        # print("rec_comdata_slot serialobj is", serialobj)
        index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "serialobj", serialobj)
        if index >= 0:
            console_terminal = GlobalVariable.Console[index]["consoleobj"]
            cursor = console_terminal.textCursor()
            if(cursor != cursor.End):
                cursor.movePosition(cursor.End)
                console_terminal.setTextCursor(cursor)

            console_terminal.insertPlainText(data)


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
            return False

        

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    testCenter = MainWindow()
    testCenter.show()
    sys.exit(app.exec_())
    
