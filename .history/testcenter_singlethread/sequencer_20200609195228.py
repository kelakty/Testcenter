

test_sequence = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh ver","sh manu"],
                "Timeout":1, "MatchLog":"version", "ClearLogBuffer":True, "SaveFile":"xxx.log"
                "Report":"xxx.xls"}]

class  Sequencer(object):
    
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




    def sequencer_txt_import_to_table(self):
        pass

    def show_sequencer_table(self):
        pass

