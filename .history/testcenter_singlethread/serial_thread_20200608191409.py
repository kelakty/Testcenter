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

"""
串口是一个单独的线程，在线程中进行串口的创建和初始化等操作
关闭线程时需要对串口进行关闭释放
"""
class SerialThread(QThread):
    def __init__(self):
        super(SerialThread,self).__init__()
        print("开始SerialThread线程init初始化中")
        print('%-25s: %s, %s,' % ("SerialThread_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("SerialThread_init", threading.current_thread().name, threading.current_thread().ident))

class SerialConsoleThread(Console):   #QObject
    rec_trigger = pyqtSignal(object,str)  #发送当前线程串口对象和串口接收到的数据
    send_trigger = pyqtSignal(object)
    def __init__(self,com_option_name):  #parent=None
        super(SerialConsoleThread,self).__init__() #parent
        self.threadactive = True

        

        # print('%-25s: %s, %s,' % ("AnalyzeObject_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("AnalyzeObject_init", threading.current_thread().name, threading.current_thread().ident))
        self.com_option_name = com_option_name
    def serial_init(self):
        # print('%-25s: %s, %s,' % ("AnalyzeObject_serial_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("AnalyzeObject_serial_init", threading.current_thread().name, threading.current_thread().ident))
        GeneralLogger().set_log_path('/tmp/thread/test.txt')  
        self.thread_logger = GeneralLogger().get_logger()
        self.thread_logger.info("开始记录线程log...")
        self.log_post_process = LogPostProcess()
        self.serial = QSerialPort()  # 用于连接串口的对象
        print("serial对象是：",self.serial)
        self.serial.setReadBufferSize(4096) #设置内部接收缓存区大小
        self.serial.readyRead.connect(self.onReadyRead)  # 绑定数据读取信号

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
            print("创建线程并打开串口成功")
            print("当前的线程ID是：",int(QThread.currentThreadId()))
            #保存串口obj到字典
            index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.com_option_name)
            print("self.com_option_name:",self.com_option_name)
            print("index is",GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "name", self.com_option_name))
            if index >= 0:   #如果返回的index是0，用 != False判断会出现，0会被认为是False
                print("开始添加serial对象字典列表")
                dictname = {"name":self.com_option_name, "serialobj":self.serial}
                GlobalVariable.Console[index].update(dictname)
                print("线程中串口创建完后的console：",GlobalVariable.Console)
                
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

        log = self.log_post_process.log_joint_and_decode(data,'gb2312')
        self.thread_logger.info(log)
        # print('%-25s: %s, %s,' % ("AnalyzObject_senddata_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("AnalyzObject_senddata_slot", threading.current_thread().name, threading.current_thread().ident))
         
    def onReadyRead(self):
        # 数据接收响应
        # print('%-25s: %s, %s,' % ("AnalyzObject_onReadyRead_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("SerialThread_onReadyRead_slot", threading.current_thread().name, threading.current_thread().ident))
        
        if self.serial.bytesAvailable():
            try:
                GlobalVariable.serialreaddata = self.serial.readAll() #self._serial.readLine()会出现转码错误，不知道为啥
                GlobalVariable.receivebuffer+=GlobalVariable.serialreaddata
                # log = self.log_post_process.log_joint_and_decode(GlobalVariable.serialreaddata,'gb2312')
                self.thread_logger.info(GlobalVariable.serialreaddata.decode("gb2312"))

                #原始的处理终端显示部分---已弃用
                #gb2312b编码，正常在python中print出来出来print(b'\x32\x33\x34\x08 \x08\x35\x36'.decode('gb2312'))结果为2356，
                #也就是\x08 \x08会执行退格空格退格操作，但是使用insertPlainText或者append进QTextEdit时，无法达到想要的效果，
                #退格无效只保留了空格,因此此处退格删除操作用自定义指令实现。
                if GlobalVariable.serialreaddata != b'\x08 \x08':
                    if GlobalVariable.serialreaddata.contains(b'\r\r\n'):
                        self.rec_trigger.emit(self.serial,GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
                    #self.console_terminal.append(b'\x31\x32\x33'.decode('gb2312'))
                    else:
                        # print("准备发射接收信号")
                        # self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312')) #.strip('\r') insertPlainText
                        self.rec_trigger.emit(self.serial,GlobalVariable.serialreaddata.data().decode('gb2312'))
                    #print('无退格')
                
            except  Exception:
                #ﾾ 
                # QMessageBox.critical(self, '','转码出错!')
                return 

# class SerialConsoleThread(Console):   #QObject
#     rec_trigger = pyqtSignal(int,str)
#     send_trigger = pyqtSignal(object)
#     def __init__(self,com_treadcounter):  #parent=None
#         super(SerialConsoleThread,self).__init__() #parent
#         self.threadactive = True
#         # #开始调用网络的信号
#         # stop_analyz_signal=pyqtSignal()
#         # start_print_result=pyqtSignal()
#         self.com_treadcounter=com_treadcounter
#         print("com_threadcounter is:")
        
#         print('%-25s: %s, %s,' % ("AnalyzeObject_init", QThread.currentThread(), int(QThread.currentThreadId())))
#         print('%-25s: %s, %s,' % ("AnalyzeObject_init", threading.current_thread().name, threading.current_thread().ident))

#     def serial_init(self):
#         print('%-25s: %s, %s,' % ("AnalyzeObject_serial_init", QThread.currentThread(), int(QThread.currentThreadId())))
#         print('%-25s: %s, %s,' % ("AnalyzeObject_serial_init", threading.current_thread().name, threading.current_thread().ident))

#         try:
#             GlobalVariable.serial[self.com_treadcounter] = QSerialPort()  # 用于连接串口的对象
#         except Exception:
#             GlobalVariable.serial.append(None)
#             print("_serial列表对象是：",GlobalVariable.serial)
#             GlobalVariable.serial[self.com_treadcounter] = QSerialPort() 
#             print("_serial列表对象是：",GlobalVariable.serial[self.com_treadcounter])
#         GlobalVariable.serial[self.com_treadcounter].setReadBufferSize(4096) #设置内部接收缓存区大小
#         GlobalVariable.serial[self.com_treadcounter].readyRead.connect(self.onReadyRead)  # 绑定数据读取信号

#         # 根据配置连接串口
#         port = GlobalVariable.ComINFO[GlobalVariable.SelectCom]    #self._ports[self.com_option.currentText()]
#         print(port)
#         print(GlobalVariable.ComINFO)
#         print(GlobalVariable.SelectCom)
#         # 根据名字设置串口（也可以用上面的函数）
#         GlobalVariable.serial[self.com_treadcounter].setPortName(port.systemLocation())
#         # print(port.systemLocation())
#         # 设置波特率
#         GlobalVariable.serial[self.com_treadcounter].setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
#             getattr(QSerialPort, 'Baud' + GlobalVariable.setting_baud_rate_option))
#         # print(self._serial.baudRate())
#         # 设置校验位
#         GlobalVariable.serial[self.com_treadcounter].setParity(  # QSerialPort::NoParity
#             getattr(QSerialPort, GlobalVariable.setting_checksum_bits + 'Parity'))
#         # print(self._serial.parity())
#         # 设置数据位
#         GlobalVariable.serial[self.com_treadcounter].setDataBits(  # QSerialPort::Data8
#             getattr(QSerialPort, 'Data' + GlobalVariable.setting_data_bits))
#         # print(self._serial.dataBits())
#         # 设置停止位
#         GlobalVariable.serial[self.com_treadcounter].setStopBits(  # QSerialPort::Data8
#             getattr(QSerialPort, GlobalVariable.setting_stop_bit))
#         # print(self._serial.stopBits())

#         # NoFlowControl          没有流程控制
#         # HardwareControl        硬件流程控制(RTS/CTS)
#         # SoftwareControl        软件流程控制(XON/XOFF)
#         # UnknownFlowControl     未知控制
#         GlobalVariable.serial[self.com_treadcounter].setFlowControl(QSerialPort.NoFlowControl)
#         # 读写方式打开串口
#         ok = GlobalVariable.serial[self.com_treadcounter].open(QIODevice.ReadWrite) 
#         # print(ok)
#         if ok:
#             #发送打开串口成功
#             print("创建线程并打开串口成功")
#             print("当前的线程ID是：",int(QThread.currentThreadId()))
#             GlobalVariable.opencomlist.append(GlobalVariable.SelectCom)
#         else:   #如果串口被占用等打开失败了。需要回退新建的MDItab和textedit widget，同时删除全局变量列表信息
#             pass
            
#             GlobalVariable.opencom_objlist.pop()
#             GlobalVariable.mdisubwindow_objlist.pop()


#     def sendto_comdata_slot(self,data):
        
#         # print("发送信号槽函数:",data)
#         GlobalVariable.serial[self.com_treadcounter].write(data)
#         print('%-25s: %s, %s,' % ("AnalyzObject_senddata_slot", QThread.currentThread(), int(QThread.currentThreadId())))
#         print('%-25s: %s, %s,' % ("AnalyzObject_senddata_slot", threading.current_thread().name, threading.current_thread().ident))
         
#         # self.start_print_result.emit()		
#         # self.stop_analyz_signal.emit()

#     def onReadyRead(self):
#         # 数据接收响应
#         print('%-25s: %s, %s,' % ("AnalyzObject_onReadyRead_slot", QThread.currentThread(), int(QThread.currentThreadId())))
#         print('%-25s: %s, %s,' % ("SerialThread_onReadyRead_slot", threading.current_thread().name, threading.current_thread().ident))
        
#         if GlobalVariable.serial[self.com_treadcounter].bytesAvailable():

#             try:
#                 GlobalVariable.serialreaddata = GlobalVariable.serial[self.com_treadcounter].readAll() #self._serial.readLine()会出现转码错误，不知道为啥
#                 GlobalVariable.receivebuffer+=GlobalVariable.serialreaddata

#                 #原始的处理终端显示部分---已弃用
#                 #gb2312b编码，正常在python中print出来出来print(b'\x32\x33\x34\x08 \x08\x35\x36'.decode('gb2312'))结果为2356，
#                 #也就是\x08 \x08会执行退格空格退格操作，但是使用insertPlainText或者append进QTextEdit时，无法达到想要的效果，
#                 #退格无效只保留了空格,因此此处退格删除操作用自定义指令实现。
#                 if GlobalVariable.serialreaddata != b'\x08 \x08':
#                     if GlobalVariable.serialreaddata.contains(b'\r\r\n'):
#                         # self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
#                         self.rec_trigger.emit(self.com_treadcounter,GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
#                     #self.console_terminal.append(b'\x31\x32\x33'.decode('gb2312'))
#                     else:
#                         # print("准备发射接收信号")
#                         # self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312')) #.strip('\r') insertPlainText
#                         self.rec_trigger.emit(self.com_treadcounter,GlobalVariable.serialreaddata.data().decode('gb2312'))
#                     #print('无退格')
                
            
#             except  Exception:
#                 pass
#                 #ﾾ 
#                 # QMessageBox.critical(self, '','转码出错!')
#                 return 
            # """
            # cursor = self.console_terminal.textCursor()
            # if(cursor != cursor.End):
            #     cursor.movePosition(cursor.End)
            #     self.console_terminal.setTextCursor(cursor)"""

    # def getAvailablePorts(self):
    #     print('%-25s: %s, %s,' % ("AnalyzObject_getAvailablePorts_slot", QThread.currentThread(), int(QThread.currentThreadId())))
    #     print('%-25s: %s, %s,' % ("SerialThread_getAvailablePorts_slot", threading.current_thread().name, threading.current_thread().ident))
        
    #     # 获取可用的串口
    #     self._ports = {}  # 用于保存串口的信息与对应地址信息的字典
    #     infos = QSerialPortInfo.availablePorts() #返回的是可用串口对象地址信息列表
    #     #infos.reverse()  # 逆序
    #     self.com_option.clear()
    #     for info in infos:
    #         # 通过串口名字-->关联串口变量
    #         self._ports[info.portName()] = info
    #         #print("串口名",info.portName())  #显示的是串口对象地址对应的串口名
    #         self.com_option.addItem(info.portName())