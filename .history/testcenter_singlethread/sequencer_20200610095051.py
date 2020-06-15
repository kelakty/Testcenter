from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread,pyqtSignal

test_sequence = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh ver", "sh manu"],"Timeout":1, "MatchLog":"version", "ClearLogBuffer":True, "SaveFile":"xxx.log", "Report":"xxx.xls"}]

class SequencerThread(QObject):
    seq_to_main_trigger = pyqtSignal(str) 
    main_to_seq_trigger = pyqtSignal(str)

    def __init__(self, current_consolethread):  #parent=None
        super(SequencerThread,self).__init__() #parent
        self.current_consolethread = current_consolethread

    def sequencer_init(self):
        #接收sequence table的数据，并存放在线程中
        self.run_sequence_table(test_sequence)

    def run_sequence_table(self, test_sequence_list):
        for test_info in test_sequence_list:
            if test_info["DoIt"] == True:
                for command in test_info["Command"]:
                    #发送命令command
                    self.seq_to_main_trigger.emit(self,command)
                    #是否弹出对话框

                    #超时时间
                    
                    
                #匹配log

                #清空本次log缓存

                #单独保存本次log文件

                #输出本次结果到报告

                #
    def received_console_log(self, serialobj, data):
        #接收到的回显log处理
        print("sequencer线程接收到的数据是：", data)



    def txt_import_to_sequencer_table(self):
        pass

    def show_sequencer_table(self):
        pass
    
    def pause(self):
        pass

    def stop_run(self):
        pass

    def move_to_next_section(self):
        pass



