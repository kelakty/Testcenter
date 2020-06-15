

test_sequence = [{"DoIt":True, "Name":"COM2", "SerialObj":"obj", "Command":["sh ver","sh manu"],
                "Timeout":1, "MatchLog":"version", "ClearLogBuffer":True, "SaveFile":"xxx.log"
                "Report":"xxx.xls"}]

class  Sequencer(object):
    
    def run_sequence_table(self, test_sequence_list):
        for test_info in test_sequence_list:
            if test_info["DoIt"] == True:
                command = test_info["Command"]
                

    def sequencer_txt_import_to_table(self):
        pass

    def show_sequencer_table(self):
        pass

