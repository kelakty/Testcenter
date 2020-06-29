from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread,pyqtSignal
from globalvariable import GlobalVariable
import threading
import time

test_sequence = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh ver\r\n", "sh manu\r\n"],"Timeout":1, "MatchLog":"version", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"}]

class SequencerThreadWorker(QObject):
    seq_to_main_trigger = pyqtSignal(object, str)  #object为需要发送到的终端
    main_to_seq_trigger = pyqtSignal(object, str)

    def __init__(self, current_consolethread ):  #parent=None #current_consolethread
        super(SequencerThreadWorker,self).__init__() #parent

        self.current_consolethread = current_consolethread
        self.current_index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "consolethread", self.current_consolethread)
        self.current_console_name = GlobalVariable.Console[self.current_index]["name"]
        # print("开始sequencerThreadworker线程init初始化中")
        # print('%-25s: %s, %s,' % ("sequencerThread_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("sequencerThread_init", threading.current_thread().name, threading.current_thread().ident))

    def sequencer_init(self):
        #接收sequence table的数据，并存放在线程中
        self.run_sequence_table(test_sequence)
        
        # print('%-25s: %s, %s,' % ("sequencer_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("sequencer_init", threading.current_thread().name, threading.current_thread().ident))
        # while True:
        #     print(threading.current_thread().name)
        #     time.sleep(2)

    def run_sequence_table(self, test_sequence_list):
        for test_info in test_sequence_list:
            if test_info["DoIt"] == True:
                for command in test_info["Command"]:
                    #发送命令command
                    self.seq_to_main_trigger.emit(self.current_consolethread, command)
                    #是否弹出对话框

                    #超时时间
                    Timeout = GlobalVariable.Console[self.current_index]["Timeout"]
                    time.sleep(Timeout)
                    #匹配log
                    if self.received_console_log

                #清空本次log缓存

                #单独保存本次log文件

                #输出本次结果到报告

                #
    def received_console_log(self, serialobj, data):
        #接收到的回显log处理
        print("sequencer线程接收到的数据是：", data)
        return data



    def txt_import_to_sequencer_table(self):
        pass
        #导入前先检查每个数据格式是否正确

    def excel_import_to_sequencer_table(self):
        pass
        #导入前先检查每个数据格式是否正确

    def show_sequencer_table(self):
        pass
    
    def pause(self):
        pass

    def stop_run(self):
        pass

    def move_to_next_section(self):
        pass


