from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread,pyqtSignal
from globalvariable import GlobalVariable
import threading
import time
import re

# test_sequence = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["1"],"Timeout":1, "MatchLog":"", "NoMatchLog":"Fail", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"},
#                 {"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["2"],"Timeout":1, "MatchLog":"interface", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"}
#                 ]

# test_sequence1 = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh ver\r\n", "sh manu\r\n"],"Timeout":1, "MatchLog":"Networks", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"},
#                 {"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh in st\r\n"],"Timeout":1, "MatchLog":"interface", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"}
#                 ]

class SequencerThreadWorker(QObject):
    seq_to_main_trigger = pyqtSignal(object, str)  #object为需要发送到的终端
    main_to_seq_trigger = pyqtSignal(object, str)

    def __init__(self, current_consolethread):  #parent=None #current_consolethread
        super(SequencerThreadWorker,self).__init__() #parent
        #初始化时还未跑在线程中

        #TODO 暂时关闭
        # self.current_consolethread = current_consolethread
        # print("当前终端线程是：", self.current_consolethread)
        # self.current_index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "consolethread", self.current_consolethread)
        # self.current_console_name = GlobalVariable.Console[self.current_index]["name"]
        print("开始sequencerThreadworker线程init初始化中")
        print('%-25s: %s, %s,' % ("sequencerThread_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("sequencerThread_init", threading.current_thread().name, threading.current_thread().ident))

    def sequencer_init(self): #test_sequence
        print('%-25s: %s, %s,' % ("sequencer_init", QThread.currentThread(), int(QThread.currentThreadId())))
        print('%-25s: %s, %s,' % ("sequencer_init", threading.current_thread().name, threading.current_thread().ident))
        while True:
            print(threading.current_thread().name)
            time.sleep(2)
            print('%-25s: %s, %s,' % ("sequencer_init", QThread.currentThread(), int(QThread.currentThreadId())))
            print('%-25s: %s, %s,' % ("sequencer_init", threading.current_thread().name, threading.current_thread().ident))
        # self.test_sequence = test_sequence
        # #接收sequence table的数据，并存放在线程中
        # self.run_sequence_table(test_sequence)
        
        
    def run_sequence_table(self, test_sequence_list):
        for test_info in test_sequence_list:
            print("是否测试：",test_info["是否测试"])
            if int(test_info["是否测试"]) != False:   #表格读取到的是字符型，需要转换为整形
                print("发送指令：",test_info["发送指令"])
                # for command in test_info["发送指令"]:
                #发送命令command
                command = str(test_info["发送指令"]).replace("\\r\\n", "\r\n")
                print(command)
                print(str(command))
                self.seq_to_main_trigger.emit(self.current_consolethread, command )
                
                #是否弹出对话框

                #超时时间
                Timeout = int(test_info["等待回显时间"])
                time.sleep(Timeout)
                # print("log缓存区：", GlobalVariable.log_data_buffer)
                #匹配log
                if self.matchlog(test_info,GlobalVariable.log_data_buffer) == True:
                    #匹配到log后
                    print("匹配到所需log")

                #清空本次log缓存
                GlobalVariable.log_data_buffer = ""
                #单独保存本次log文件
                
                #输出本次结果到报告
                #
        
    def received_console_log(self, serialobj, data):
        #接收到的回显log处理
        pass
        # if data != False:
        # print("sequencer线程接收到的数据是：", data)
        # self.log_data_buffer += data
        





    
    def matchlog(self, test_info, log_data_buffer):
        #匹配log
        # print("log缓存区：", log_data_buffer)
        if re.findall(test_info["需匹配文本"], log_data_buffer) != []:
            return True
        else:
            return False







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


