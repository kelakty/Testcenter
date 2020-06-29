from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread,pyqtSignal,QStandardPaths
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
from globalvariable import GlobalVariable
import threading
import time
import re
import pandas as pd
from datetime import datetime 

# test_sequence = [{"是否测试":True, "Name":"COM2", "SerialObj":"obj", "发送指令":"1","等待回显时间":1, "需匹配文本":"", "NoMatchLog":"Fail", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"},
#                 {"是否测试":True, "Name":"COM2", "SerialObj":"obj", "发送指令":"2","等待回显时间":1, "需匹配文本":"interface", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"}
#                 ]

class SequencerThreadWorker(QObject):
    seq_to_main_trigger = pyqtSignal(object, str)  #object为需要发送到的终端
    main_to_seq_trigger = pyqtSignal(object, str)
    finished = pyqtSignal()
    choose_file_trigger = pyqtSignal()
    def __init__(self,current_consolethread):  #parent=None #current_consolethread
        super(SequencerThreadWorker,self).__init__() #parent
        #初始化时还未跑在线程中

        #TODO 暂时关闭。以下代码会导致无法进入线程sequencer_init。原因未知
        self.current_consolethread = current_consolethread
        # print("当前终端线程是：", self.current_consolethread)
        # self.current_index = GlobalVariable.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "consolethread", self.current_consolethread)
        # self.current_console_name = GlobalVariable.Console[self.current_index]["name"]
        # print("开始sequencerThreadworker线程init初始化中")
        # print('%-25s: %s, %s,' % ("sequencerThread_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("sequencerThread_init", threading.current_thread().name, threading.current_thread().ident))

    def sequencer_worker(self): #test_sequence
        # print('%-25s: %s, %s,' % ("sequencer_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("sequencer_init", threading.current_thread().name, threading.current_thread().ident))
        # while True:
        print(threading.current_thread().name)
        time.sleep(3)
        self.sequence_table(GlobalVariable.table_dict_list)  #GlobalVariable.table_dict_list
        # print('%-25s: %s, %s,' % ("sequencer_init", QThread.currentThread(), int(QThread.currentThreadId())))
        # print('%-25s: %s, %s,' % ("sequencer_init", threading.current_thread().name, threading.current_thread().ident))
        # self.test_sequence = test_sequence
        # #接收sequence table的数据，并存放在线程中
        # self.run_sequence_table(test_sequence)
        
        self.finished.emit() 
        GlobalVariable.sequencer_working = False
        
    def sequence_table(self, test_sequence_list):
        print(test_sequence_list)
        for test_info in test_sequence_list:
            print("是否测试：",test_info["是否测试"])
            if int(test_info["是否测试"]) != False:   #表格读取到的是字符型，需要转换为整形
                
                #是否有保存报告的路径，有则先选择保存报告路径.不能在线程中选择。
                if int(test_info["选择报告文件"]) != False and test_info["选择报告文件"] != "nan":
                    self.choose_file_trigger.emit()
                    GlobalVariable.sequencer_waiting_for_main = True
                    while GlobalVariable.sequencer_waiting_for_main == True:
                        pass #等待main的槽函数执行完sequencer_waiting_for_main ==False
                print("发送指令：",test_info["发送指令"])
                #发送指令不为空才发送
                if test_info["发送指令"] != "" and test_info["发送指令"] != "nan":
                    # for command in test_info["发送指令"]:
                    # 发送命令command
                    command = str(test_info["发送指令"]).replace("\\r\\n", "\r\n")
                    print(command)
                    print(str(command))
                    # self.seq_to_main_trigger.emit(GlobalVariable.Console[0]["consolethread"], command )#self.current_consolethread
                    self.seq_to_main_trigger.emit(self.current_consolethread, command )
                    
                    #是否弹出对话框

                    #超时时间
                    if test_info["等待回显时间"] != "nan":
                        Timeout = int(test_info["等待回显时间"])
                        time.sleep(Timeout)
                    print("log缓存区：", GlobalVariable.log_data_buffer)
                    
                    # 匹配log
                    if self.matchlog(test_info,GlobalVariable.log_data_buffer) == True and self.nomatchlog(test_info,GlobalVariable.log_data_buffer) == False:
                        #代表测试通过
                        print("匹配到所需log同时不匹配到fail等表测试通过")
                    if self.nomatchlog(test_info,GlobalVariable.log_data_buffer) == True:
                        print("匹配到fail的log")

                    #单独保存本次log文件
                    
                

                #清空本次log缓存
                GlobalVariable.log_data_buffer = ""
                
                #输出本次结果到报告
                self.report_df = pd.read_excel(GlobalVariable.sequencer_choosefilename, sheet_name = '机框式交换机生测checklist')
                print(self.report_df)
                self.report_name = GlobalVariable.sequencer_choosefilename+"_%d%02d%02d_%d_%02d_%02d"% (datetime.now().year, datetime.now().month, datetime.now().day,datetime.now().hour,datetime.now().minute,datetime.now().second)+".xlsx"
                self.report_writer = pd.ExcelWriter(self.report_name, engine='xlsxwriter')


                self.report_df.to_excel(self.report_writer, sheet_name='机框式交换机生测checklist')
                self.report_writer.save()
        

        
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

    def nomatchlog(self, test_info, log_data_buffer):
        if re.findall(test_info["不能匹配到文本"], log_data_buffer) != []:
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



