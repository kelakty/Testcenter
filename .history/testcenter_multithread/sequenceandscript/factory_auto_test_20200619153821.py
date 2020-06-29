import re
from globalvariable import GlobalVariable
from datetime import datetime

class FactoryAutoTestWorker(QObject):
    fac_test_to_main_trigger = pyqtSignal(object, str)  #object为需要发送到的终端
    main_to_fac_test_trigger = pyqtSignal(object, str)
    finished = pyqtSignal()
    def __init__(self,current_consolethread):
        super(FactoryAutoTestWorker,self).__init__() 
        self.current_consolethread = current_consolethread

        self.judge_over_diction = ["Ruijie#","生产测试菜单","Ruijie(config)#","Ruijie(config-if-range)#",
                                        "~ #","sdk.0>","sdk.1>","sdk.2>","e exit telnet",]
        self.judge_fail_diction = ["fail","Fail","FAIL","故障","失败"]
        self.judge_suspicious_diction = ["不在位","N/A","NA"]
        self.judge_pass_diction = ["pass","Pass","PASS","通过"]
        self.waiting_manu_press_yes = ["Yes/no","Yes/No","No/yes","No/Yes"]
        self.waiting_reload = ["请重启"]
        self.check_info = {"产品信息检测":{},
                            "温度检测":{},
                            "内存测试":{},
                            "SPI Flash测试":{},
                            "USB测试":{},
                            "EMMC测试":{},
                            "RTC测试":{},
                            "I2C接口测试":{},
                            "CPLD测试":{},
                            "端口收发帧测试":{},
                            "LED测试":{},
                            "风扇状态检测":{},
                            "电源状态检测":{},
                            "端口广播测试":{},
                            "Prbs测试":{},
                            "带外低速信号测试":{},
                            "硬件双Boot测试":{},
                            "在线升级接口测试":{},
                            "管理口收发帧测试":{}}
        with open("fac_auto_test.txt","a+") as self.fac_auto_test_log:
            pass

        self.fac_auto_test_timer = QTimer(self)
        self.fac_auto_test_timer.timeout.connect(self.timer_overtime)
        self.fac_auto_test_overtime = False
    def run_auto_fac_test(self):
        """
        生测自动跑所有测试
        """
        #判断是否为生产测试菜单
        while self.matchlog("生产测试菜单", GlobalVariable.log_data_buffer) == True: 
            #判断是否为主菜单 #判断是否为单项测试
            if self.matchlog("主菜单",GlobalVariable.log_data_buffer) == True or self.matchlog("单项测试",GlobalVariable.log_data_buffer) == True: 
                #如果是主菜单下
                #找当前菜单下有多少个测试项
                commandlist = self.search_test_item(GlobalVariable.log_data_buffer)
                if commandlist != False:
                    for command in commandlist:
                        #发送命令
                        self.fac_test_to_main_trigger.emit(self.current_consolethread, command)
                        
                        self.fac_auto_test_overtime = False 
                        self.fac_auto_test_timer.start(20*60*1000) #定时器是ms为单位，定时时间20分钟
                        #等待运行结束 或者超时20分钟未打印新字符
                        while self._judge_one_test_over != True or self.fac_auto_test_overtime == False ：
                            pass

                        #判断是否还是在相同菜单,如果是不同菜单，说明进入了二级菜单，而不是实际测试。
                        command_sub_list = self.search_test_item(GlobalVariable.log_data_buffer)
                        if command_sub_list == commandlist:
                            break
                        #判断是否出现需要用户输入的[Yes/no]等字眼，如果是则自动输入
                        if 
                        #判断测试是否pass
                        if self._judge_pass_or_not(GlobalVariable.log_data_buffer) == False:
                            #保存失败的log数据
                            self.fac_auto_test_log.write(datetime.now()+"\r\n")
                            self.fac_auto_test_log.write(GlobalVariable.log_data_buffer)
                        #测试完单项，清空log缓存
                        GlobalVariable.log_data_buffer = ""





                

        #识别菜单中的所有选项

        #依次跑遍所有选项

        #判断选项中是否含有对应字眼，并作出相应的反应

        #判断执行是否完成

    def matchlog(self, need_match_text, log_data_buffer):
        #匹配log
        # print("log缓存区：", log_data_buffer)
        matchdatalist = []
        matchdatalist = re.findall(need_match_text, log_data_buffer)
        if matchdatalist != []:
            return matchdatalist
        else:
            return False

    def search_test_item(self,log_data):
        #找当前菜单下有多少个测试项
        #找到则返回序数列表，否则返回false
        need_match_text = "    (\w). "
        match_num_list = self.matchlog(need_match_text, log_data)
        if match_num_list != False:
            return match_num_list
        else: return False
        

    def _judge_one_test_over(self):
        for i in self.judge_over_diction:
            if self.matchlog(i, GlobalVariable.log_data_buffer) != False:
                #程序运行结束
                return True
        return False

    def timer_overtime(self):
        self.fac_auto_test_overtime = True
        self.fac_auto_test_timer.stop()
        
    def _judge_pass_or_not(self,log_data_buffer):
        for i in self.judge_fail_diction:
            if self.matchlog(i, log_data_buffer) != False:
                return False
        for i in self.judge_suspicious_diction:
            if self.matchlog(i, log_data_buffer) != False:
                return False
        for i in self.judge_pass_diction:
            if self.matchlog(i,log_data_buffer) != False:
                return True
        return False
