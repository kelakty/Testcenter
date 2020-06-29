import re

class FactoryAutoTestWorker(QObject):
    fac_test_to_main_trigger = pyqtSignal(object, str)  #object为需要发送到的终端
    main_to_fac_test_trigger = pyqtSignal(object, str)
    finished = pyqtSignal()
    def __init__(self):
        super(FactoryAutoTestWorker,self).__init__() 
        self.judge_over_diction = ["Ruijie#","生产测试菜单","Ruijie(config)#","Ruijie(config-if-range)#",
                                        "~ #","sdk.0>","sdk.1>","sdk.2>","e exit telnet",]
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

    def run_auto_fac_test(self):
        """
        生测自动跑所有测试
        """




    def judge_over(self):
        
        return True

