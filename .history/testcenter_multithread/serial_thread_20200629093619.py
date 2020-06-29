import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
from PyQt5.QtCore import QIODevice,QObject
from PyQt5.QtCore import QThread,Qt,pyqtSignal
from globalvariable import GlobalVariable
from PyQt5.QtWidgets import QMessageBox
import threading
from loggerbythread import GeneralLogger
from loggerbythread import LogPostProcess
from Console import Console
from datetime import datetime

"""
串口是一个单独的线程，在线程中进行串口的创建和初始化等操作
关闭线程时需要对串口进行关闭释放
"""
class SerialThread(QThread):
    def __init__(self):
        super(SerialThread,self).__init__()
        # print("开始SerialThread线程init初始化中")
        # print('%-25s: %s, %s,' % ("SerialThread_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("SerialThread_init", threading.current_thread().name, threading.current_thread().ident))

class SerialConsoleThread(Console):   #QObject
    rec_trigger = pyqtSignal(object,str)  #发送当前线程串口对象和串口接收到的数据
    send_trigger = pyqtSignal(object)
    def __init__(self,com_option_name):  #parent=None
        super(SerialConsoleThread,self).__init__() #parent
        self.threadactive = True
        print("开始SerialThread线程init初始化中")
        

        print('%-25s: %s, %s,' % ("SerialConsoleThread_init", QThread.currentThread(), int()))
        print('%-25s: %s, %s,' % ("SerialConsoleThread_init", threading.current_thread().name, threading.current_thread().ident))
        self.com_option_name = com_option_name
    def serial_init(self):
        print('%-25s: %s, %s,' % ("AnalyzeObject_serial_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("AnalyzeObject_serial_init", threading.current_thread().name, threading.current_thread().ident))
        #初始化待保存log处理的中间全局变量
        GlobalVariable.waiting_to_send.update({str(threading.current_thread().ident) : {"senddata":[], "residue":""}})
        # print("初始化waitingtosend是：",GlobalVariable.waiting_to_send)
        # print(GlobalVariable.mainwindow.savelogdir.text())
        if GlobalVariable.mainwindow.checkBox_savelog.checkState():
            if GlobalVariable.mainwindow.savelogdir.text() == "":
                # print("savelogdir是空的")
                currentdatetime = "_%d%02d%02d_%d_%02d_%02d" % (datetime.now().year,
                                datetime.now().month, datetime.now().day,
                                datetime.now().hour,datetime.now().minute,datetime.now().second)
                GeneralLogger().set_log_path(self.com_option_name + currentdatetime + '.log')  
            else:
                save_log_path = GlobalVariable.mainwindow.savelogdir.text()
                print("保存log文件路径是：",save_log_path)
                GeneralLogger().set_log_path(save_log_path)
                GlobalVariable.mainwindow.savelogdir.clear()
        self.thread_logger = GeneralLogger().get_logger()
        self.thread_logger.info("开始记录线程log...")  #TODO 暂时关闭log
        self.log_post_process = LogPostProcess()
        self.send_log_stub = ""
        self.receive_log_stub= ""

        self.serial = QSerialPort()  # 用于连接串口的对象
        # print("serial对象是：",self.serial)
        self.serial.setReadBufferSize(4096) #设置内部接收缓存区大小
        self.serial.readyRead.connect(self.onReadyRead)  # 绑定数据读取信号
        #连接sequencer的信号
        # self.serial.readyRead.connect(self.)

        # 根据配置连接串口
        port = GlobalVariable.ComINFO[GlobalVariable.SelectCom]
        print(port)

        # 根据名字设置串口（也可以用上面的函数）
        self.serial.setPortName(port.systemLocation())
        
        # 设置波特率
        self.serial.setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
            getattr(QSerialPort, 'Baud' + GlobalVariable.setting_baud_rate_option))
        
        # 设置校验位
        self.serial.setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, GlobalVariable.setting_checksum_bits + 'Parity'))
        
        # 设置数据位
        self.serial.setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + GlobalVariable.setting_data_bits))
        
        # 设置停止位
        self.serial.setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, GlobalVariable.setting_stop_bit))
        
        # NoFlowControl          没有流程控制
        # HardwareControl        硬件流程控制(RTS/CTS)
        # SoftwareControl        软件流程控制(XON/XOFF)
        # UnknownFlowControl     未知控制
        self.serial.setFlowControl(QSerialPort.NoFlowControl)
        
        # 读写方式打开串口
        ok = self.serial.open(QIODevice.ReadWrite) 
        if ok:
            #发送打开串口成功
            # print("创建线程并打开串口成功")
            # print("当前的线程ID是：",int(QThread.currentThreadId()))
            #保存串口obj到字典
            self.index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.com_option_name)
            # print("self.com_option_name:",self.com_option_name)
            # print("index is",GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.com_option_name))
            if self.index >= 0:   #如果返回的index是0，用 != False判断会出现，0会被认为是False
                # print("开始添加serial对象字典列表")
                dictname = {"name":self.com_option_name, "serialobj":self.serial}
                GlobalVariable.Console[self.index].update(dictname)
                # print("线程中串口创建完后的console：",GlobalVariable.Console)
                self.encodingtype = GlobalVariable.Console[self.index]["encodingtype"]
                
        else:   #如果串口被占用等打开失败了。需要回退新建的MDItab和textedit widget，同时删除全局变量列表信息
            pass
            # GlobalVariable.opencom_objlist.pop()
            # GlobalVariable.mdisubwindow_objlist.pop()


    def sendto_comdata_slot(self,data):
        """
        在串口线程内发送数据给对应的串口对象
        """
        # print("发送信号槽函数:",data)
        self.serial.write(data)

        # GlobalVariable.waiting_to_send.update(self.log_post_process.log_joint_and_decode(
        #     str(threading.current_thread().ident), GlobalVariable.waiting_to_send, data, 'gb2312'))
        # for i in GlobalVariable.waiting_to_send[str(threading.current_thread().ident)]["senddata"]:
        #     self.thread_logger.info(i)
        datalist = (self.send_log_stub + data.decode(self.encodingtype)).split("\r\n")
        self.send_log_stub = datalist[-1]
        datalist.pop()
        for i in datalist:
            self.thread_logger.info(i)  #TODO log暂时关闭
         
    def onReadyRead(self):
        # 数据接收响应
        # print('%-25s: %s, %s,' % ("AnalyzObject_onReadyRead_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("SerialThread_onReadyRead_slot", threading.current_thread().name, threading.current_thread().ident))
        
        if self.serial.bytesAvailable():
            
            GlobalVariable.serialreaddata.append(self.serial.readAll()) #self._serial.readLine()会出现转码错误，不知道为啥
            if GlobalVariable.openreceivebuffer == True :
                GlobalVariable.receivebuffer += GlobalVariable.serialreaddata
                # log = self.log_post_process.log_joint_and_decode(GlobalVariable.serialreaddata,'gb2312')
                # self.thread_logger.info(GlobalVariable.serialreaddata.decode("gb2312"))

                #原始的处理终端显示部分---已弃用
                #gb2312b编码，正常在python中print出来出来print(b'\x32\x33\x34\x08 \x08\x35\x36'.decode('gb2312'))结果为2356，
                #也就是\x08 \x08会执行退格空格退格操作，但是使用insertPlainText或者append进QTextEdit时，无法达到想要的效果，
                #退格无效只保留了空格,因此此处退格删除操作用自定义指令实现。
            # print("发送前字符：",GlobalVariable.serialreaddata)
            # self.rec_trigger.emit(self.serial,GlobalVariable.serialreaddata.data().decode(encoding=self.encodingtype,errors="ignore"))
            try:
                if GlobalVariable.serialreaddata != b'\x08 \x08':
                    if GlobalVariable.serialreaddata.contains(b'\r\r\n'):
                        data = GlobalVariable.serialreaddata.data().decode(encoding=self.encodingtype).replace("\r\r\n", "\r\n")
                        self.rec_trigger.emit(self.serial,data)
                        GlobalVariable.serialreaddata.clear()
                        datalist = (self.receive_log_stub + data).split("\r\n")
                        self.receive_log_stub = datalist[-1]
                        datalist.pop()
                        for i in datalist:
                            self.thread_logger.info(i)
                    #self.console_terminal.append(b'\x31\x32\x33'.decode('gb2312'))
                    else:
                        # print("准备发射接收信号")
                        # self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312')) #.strip('\r') insertPlainText
                        data = GlobalVariable.serialreaddata.data().decode(encoding=self.encodingtype)
                        self.rec_trigger.emit(self.serial,data)
                        GlobalVariable.serialreaddata.clear()
                        datalist = (self.receive_log_stub + data).split("\r\n")
                        self.receive_log_stub = datalist[-1]
                        datalist.pop()
                        for i in datalist:
                            self.thread_logger.info(i)
                    #print('无退格')
                
            except  Exception:
                #ﾾ
                
                # QMessageBox.critical(self, '','转码出错!')
                return 
