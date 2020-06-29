


class TelnetThread(QThread):
    def __init__(self):
        super(TelnetThread,self).__init__()

class TelnetConsoleThread(Console):   #QObject
    rec_trigger = pyqtSignal(object,str)  #发送当前线程串口对象和串口接收到的数据
    send_trigger = pyqtSignal(object)
    def __init__(self,com_option_name):  #parent=None
        super(SerialConsoleThread,self).__init__() #parent
        self.threadactive = True
        print("开始SerialThread线程init初始化中")
        print('%-25s: %s, %s,' % ("SerialConsoleThread_init", QThread.currentThread(), int()))
        print('%-25s: %s, %s,' % ("SerialConsoleThread_init", threading.current_thread().name, threading.current_thread().ident))
        self.com_option_name = com_option_name
        
    def telnet_init(self):
        pass


    def sendto_comdata_slot(self,data):
        """
        在串口线程内发送数据给对应的串口对象
        """
        pass
    def onReadyRead(self):
        pass

