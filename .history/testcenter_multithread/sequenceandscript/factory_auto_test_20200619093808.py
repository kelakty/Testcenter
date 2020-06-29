

class FactoryAutoTest():

    def __init__(self):
        
        self.judge_over_diction = ["Ruijie#","生产测试菜单","Ruijie(config)#","Ruijie(config-if-range)#",
                                        "~ #","sdk.0>","sdk.1>","sdk.2>","e exit telnet",]


    def run(self):
        """
        生测自动跑所有测试
        """

    def judge_over(self):
        #判断执行是否结束，通过是否出现"Ruijie#"、"生产测试菜单"、"Ruijie(config)#"、"~ #"
