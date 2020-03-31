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
encodingType=GlobalVariable.defaultEncodingType

"""
串口是一个单独的线程，在线程中进行串口的创建和初始化等操作
关闭线程时需要对串口进行关闭释放
"""
class SerialThread(QThread):
    # rec_trigger = pyqtSignal(object)
    # send_trigger = pyqtSignal(object)
    def __init__(self):
        super(SerialThread,self).__init__()
        
        # rec_trigger.connect(testCenter.rec_comdata_slot)
        # self.threadname=Tname
        print("开始SerialThread线程init初始化中")


        print('%-25s: %s, %s,' % ("SerialThread_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("SerialThread_init", threading.current_thread().name, threading.current_thread().ident))
        
        #这里千万不能用run函数，用了之后就无法从主线程发射信号到从线程的slot。原因还未知。
        # def run(self):
        #     pass
        #     print("开始SerialThread线程run")
            
        #     print('%-25s: %s, %s,' % ("SerialThread_run", QThread.currentThread(), int(QThread.currentThreadId())))
        #     print('%-25s: %s, %s,' % ("SerialThread_run", threading.current_thread().name, threading.current_thread().ident))
                
        #     while True:
        #         pass


class AnalyzObject(QObject):
    rec_trigger = pyqtSignal(int,str)
    send_trigger = pyqtSignal(object)
    def __init__(self,com_treadcounter):  #parent=None
        super(AnalyzObject,self).__init__() #parent
        # #开始调用网络的信号
        # stop_analyz_signal=pyqtSignal()
        # start_print_result=pyqtSignal()
        self.com_treadcounter=com_treadcounter
        print("com_treadcounter is:")
        self.serial=[]
        print('%-25s: %s, %s,' % ("AnalyzObject_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("AnalyzObject_init", threading.current_thread().name, threading.current_thread().ident))

    def serial_init(self):
        print('%-25s: %s, %s,' % ("AnalyzObject_serial_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("AnalyzObject_serial_init", threading.current_thread().name, threading.current_thread().ident))

        try:
            self.serial[self.com_treadcounter] = QSerialPort()  # 用于连接串口的对象
        except Exception:
            self.serial.append(None)
            print("_serial列表对象是：",self.serial)
            self.serial[self.com_treadcounter] = QSerialPort() 
            print("_serial列表对象是：",self.serial[self.com_treadcounter])
        self.serial[self.com_treadcounter].setReadBufferSize(4096) #设置内部接收缓存区大小
        self.serial[self.com_treadcounter].readyRead.connect(self.onReadyRead)  # 绑定数据读取信号

        # 根据配置连接串口
        port = GlobalVariable.ComINFO[GlobalVariable.SelectCom]    #self._ports[self.com_option.currentText()]
        print(port)
        print(GlobalVariable.ComINFO)
        print(GlobalVariable.SelectCom)
        # 根据名字设置串口（也可以用上面的函数）
        self.serial[self.com_treadcounter].setPortName(port.systemLocation())
        # print(port.systemLocation())
        # 设置波特率
        self.serial[self.com_treadcounter].setBaudRate(  # 动态获取,类似QSerialPort::Baud9600这样的吧
            getattr(QSerialPort, 'Baud' + GlobalVariable.setting_baud_rate_option))
        # print(self._serial.baudRate())
        # 设置校验位
        self.serial[self.com_treadcounter].setParity(  # QSerialPort::NoParity
            getattr(QSerialPort, GlobalVariable.setting_checksum_bits + 'Parity'))
        # print(self._serial.parity())
        # 设置数据位
        self.serial[self.com_treadcounter].setDataBits(  # QSerialPort::Data8
            getattr(QSerialPort, 'Data' + GlobalVariable.setting_data_bits))
        # print(self._serial.dataBits())
        # 设置停止位
        self.serial[self.com_treadcounter].setStopBits(  # QSerialPort::Data8
            getattr(QSerialPort, GlobalVariable.setting_stop_bit))
        # print(self._serial.stopBits())

        # NoFlowControl          没有流程控制
        # HardwareControl        硬件流程控制(RTS/CTS)
        # SoftwareControl        软件流程控制(XON/XOFF)
        # UnknownFlowControl     未知控制
        self.serial[self.com_treadcounter].setFlowControl(QSerialPort.NoFlowControl)
        # 读写方式打开串口
        ok = self.serial[self.com_treadcounter].open(QIODevice.ReadWrite) 
        # print(ok)
        if ok:
            #发送打开串口成功
            print("创建线程并打开串口成功")
            print("当前的线程ID是：",int(QThread.currentThreadId()))
            GlobalVariable.opencomlist.append(GlobalVariable.SelectCom)
        else:   #如果串口被占用等打开失败了。需要回退新建的MDItab和textedit widget，同时删除全局变量列表信息
            pass
        
            GlobalVariable.opencom_objlist.pop()
            GlobalVariable.mdisubwindow_objlist.pop()

        

    def sendto_comdata_slot(self,data):
        
        # print("发送信号槽函数:",data)
        self.serial[self.com_treadcounter].write(data)
        print('%-25s: %s, %s,' % ("AnalyzObject_senddata_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("AnalyzObject_senddata_slot", threading.current_thread().name, threading.current_thread().ident))
         
        # self.start_print_result.emit()		
        # self.stop_analyz_signal.emit()

    def onReadyRead(self):
        # 数据接收响应
        print('%-25s: %s, %s,' % ("AnalyzObject_onReadyRead_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("SerialThread_onReadyRead_slot", threading.current_thread().name, threading.current_thread().ident))
        
        if self.serial[self.com_treadcounter].bytesAvailable():

            try:
                GlobalVariable.serialreaddata = self.serial[self.com_treadcounter].readAll() #self._serial.readLine()会出现转码错误，不知道为啥
                GlobalVariable.receivebuffer+=GlobalVariable.serialreaddata

                #原始的处理终端显示部分---已弃用
                #gb2312b编码，正常在python中print出来出来print(b'\x32\x33\x34\x08 \x08\x35\x36'.decode('gb2312'))结果为2356，
                #也就是\x08 \x08会执行退格空格退格操作，但是使用insertPlainText或者append进QTextEdit时，无法达到想要的效果，
                #退格无效只保留了空格,因此此处退格删除操作用自定义指令实现。
                if GlobalVariable.serialreaddata != b'\x08 \x08':
                    if GlobalVariable.serialreaddata.contains(b'\r\r\n'):
                        # self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
                        self.rec_trigger.emit(self.com_treadcounter,GlobalVariable.serialreaddata.data().decode('gb2312').replace("\r\r\n", "\r\n"))
                    #self.console_terminal.append(b'\x31\x32\x33'.decode('gb2312'))
                    else:
                        print("准备发射接收信号")
                        # self.console_terminal.insertPlainText(GlobalVariable.serialreaddata.data().decode('gb2312')) #.strip('\r') insertPlainText
                        self.rec_trigger.emit(self.com_treadcounter,GlobalVariable.serialreaddata.data().decode('gb2312'))
                    #print('无退格')
                
            
            except  Exception:
                pass
                # QMessageBox.critical(self, '','转码出错!')
                return 

            """
            cursor = self.console_terminal.textCursor()
            if(cursor != cursor.End):
                cursor.movePosition(cursor.End)
                self.console_terminal.setTextCursor(cursor)"""



    def getAvailablePorts(self):
        print('%-25s: %s, %s,' % ("AnalyzObject_getAvailablePorts_slot", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("SerialThread_getAvailablePorts_slot", threading.current_thread().name, threading.current_thread().ident))
        
        # 获取可用的串口
        self._ports = {}  # 用于保存串口的信息与对应地址信息的字典
        infos = QSerialPortInfo.availablePorts() #返回的是可用串口对象地址信息列表
        #infos.reverse()  # 逆序
        self.com_option.clear()
        for info in infos:
            # 通过串口名字-->关联串口变量
            self._ports[info.portName()] = info
            #print("串口名",info.portName())  #显示的是串口对象地址对应的串口名
            self.com_option.addItem(info.portName())