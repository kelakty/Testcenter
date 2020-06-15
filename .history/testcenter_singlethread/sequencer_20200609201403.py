

test_sequence = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh ver", "sh manu"],
                "Timeout":1, "MatchLog":"version", "ClearLogBuffer":True, "SaveFile":"xxx.log"
                "Report":"xxx.xls"}]

class  SequencerThread(QObject):
    rec_trigger = pyqtSignal(object,str) 
    send_trigger = pyqtSignal(object)

    def __init__(self):  #parent=None
        super(SequencerThread,self).__init__() #parent

    def run_sequence_table(self, test_sequence_list):
        for test_info in test_sequence_list:
            if test_info["DoIt"] == True:
                for command in test_info["Command"]:
                    #发送命令command
                    
                    #是否弹出对话框

                    #超时时间
                    
                    
                #匹配log

                #清空本次log缓存

                #单独保存本次log文件

                #输出本次结果到报告

                #




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


