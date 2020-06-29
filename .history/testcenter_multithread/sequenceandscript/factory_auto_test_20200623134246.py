# -*- coding: utf-8 -*-
# @Author:Jiukui Feng

import re
from PyQt5.QtCore import QObject,QThread,pyqtSignal,QStandardPaths,QTimer
import threading
from globalvariable import GlobalVariable
from datetime import datetime
from sequenceandscript.multiTreeRecursion import TreeNode
from sequenceandscript.multiTreeRecursion import MultiTree
import time 
import queue

class FactoryAutoTestWorker(QObject):
    fac_test_to_main_trigger = pyqtSignal(object, str)  #object为需要发送到的终端
    main_to_fac_test_trigger = pyqtSignal(object, str)
    finished = pyqtSignal()
    def __init__(self,current_consolethread):
        super(FactoryAutoTestWorker,self).__init__() 
        self.current_consolethread = current_consolethread

        self.judge_over_diction = ["Ruijie#","生产测试菜单","*************************************","Ruijie(config)#","Ruijie(config-if-range)#",
                                        "~ #","sdk.0>","sdk.1>","sdk.2>","e exit telnet",]
        self.judge_fail_diction = ["fail","Fail","FAIL","故障","失败"]
        self.judge_suspicious_diction = ["不在位","N/A","NA"]
        self.judge_pass_diction = ["pass","Pass","PASS","通过","成功"]
        self.waiting_manu_press_yes_list = ["Yes/no","Yes/No","No/yes","No/Yes"]
        self.waiting_reload_list = ["请重启"]
        self.send_info = {"0. 设置RTC时间":"2020 12 31 23:59:59\r"}
                        
        self.check_info = { "设置RTC时间":{},
                            "产品信息检测":{},
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
        

        self.fac_auto_test_timer = QTimer(self)
        self.fac_auto_test_timer.timeout.connect(self.timer_overtime)
        self.fac_auto_test_overtime = False
        print("线程初始化完成")

    def PreOrderWithoutRecursion(root):
        stacknode = queue.LifoQueue()
        while(root is not None or not stacknode.empty()):
            if(root is not None):
                visit(root)
                stacknode.put(root.right)
                root = root.left
            else:
                root = stacknode.get()
                
    def run_auto_fac_test(self):
        """
        生测自动跑所有测试
        """
        print("开始生测自动化测试...")
        self.fac_auto_test_log = open("fac_auto_test.txt","a+")
        self.stacknode = queue.LifoQueue()
        self.fac_test_to_main_trigger.emit(self.current_consolethread,"\r")
        time.sleep(2)
        self.tree = MultiTree('主菜单',"")
        #一直等待直到进入生产测试菜单
        while self.matchlog("生产测试菜单", GlobalVariable.log_data_buffer) != False: 
            print("进入生测测试菜单测试")
            #判断是否为主菜单 或 是否为单项测试
            if self.matchlog("主菜单",GlobalVariable.log_data_buffer) != False or self.matchlog("单项测试\r\n***",GlobalVariable.log_data_buffer) != False: 
                #如果是单项测试菜单下，则ctrl+z返回到上级菜单，即主菜单
                if self.matchlog("单项测试\r\n***",GlobalVariable.log_data_buffer) != False: 
                    print("找到单项测试菜单")
                    # self.fac_test_to_main_trigger.emit(self.current_consolethread,"ctrl+z")  #TODO 这里快捷键的发送需要怎么发送？
                
                #如果是主菜单下
                if self.matchlog("主菜单",GlobalVariable.log_data_buffer) != False:
                    commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                    command_dictionary = GlobalVariable.mainwindow.two_list_convert_to_keyvalue_dict(test_name_list,commandlist)
                    print("找到的命令和测试项:",commandlist,test_name_list)
                    if commandlist != False:
                        if len(commandlist) == len(test_name_list):
                            #存入多叉树
                            node_name = [None for _ in range(len(commandlist))]
                            print("node_name is :",node_name)
                            for i in range(len(commandlist)):
                                node_name[i] = test_name_list[i]
                                #建立TreeNode
                                node_name[i] = TreeNode(test_name_list[i],commandlist[i])
                                
                                print("节点名是：",node_name[i].name)
                                #添加TreeNode
                                self.tree.add(node_name[i])
                            
                            #将树逆序放入堆栈
                            for i in range(len(commandlist)-1,-1,-1):
                                self.stacknode.put(commandlist[i])
                                
                    #开始正式测试循环
                    while True:
                        #如果菜单不同，不存在树中，则加入tree，放入stack
                        commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                        sub_command_dictionary = GlobalVariable.mainwindow.two_list_convert_to_keyvalue_dict(test_name_list,commandlist)
                        if list(sub_command_dictionary.keys()) != list(command_dictionary.keys()):
                            #菜单不同则生成tree，放入stack
                            GlobalVariable.log_data_buffer = ""
                            self.fac_test_to_main_trigger.emit(self.current_consolethread,"\r")
                            commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                            print("找到的命令和测试项:",commandlist,test_name_list)
                            if commandlist != False:
                                if len(commandlist) == len(test_name_list):
                                    #存入多叉树
                                    node_name = [None for _ in range(len(commandlist))]
                                    print("node_name is :",node_name)
                                    for i in range(len(commandlist)):
                                        node_name[i] = test_name_list[i]
                                        #建立TreeNode
                                        node_name[i] = TreeNode(test_name_list[i],commandlist[i])
                                        
                                        print("节点名是：",node_name[i].name)
                                        #添加TreeNode
                                        self.tree.add(node_name[i])
                                    
                                    #将树逆序放入堆栈
                                    for i in range(len(commandlist)-1,-1,-1):
                                        self.stacknode.put(commandlist[i])

                        else:
                            
                    #找当前菜单下有多少个测试项，并存入多叉树Tree
                    print("找到主菜单,开始建多叉树")
                    print("先打印树",self.tree.tree.name)
                    commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                    print("找到的命令和测试项:",commandlist,test_name_list)
                    if commandlist != False:
                        if len(commandlist) == len(test_name_list):
                            #存入多叉树
                            node_name = [None for _ in range(len(commandlist))]
                            print("node_name is :",node_name)
                            for i in range(len(commandlist)):
                                node_name[i] = test_name_list[i]
                                #建立TreeNode
                                node_name[i] = TreeNode(test_name_list[i],commandlist[i])
                                
                                print("节点名是：",node_name[i].name)
                                #添加TreeNode
                                self.tree.add(node_name[i])
                            
                            #将树逆序放入堆栈
                            for i in range(len(commandlist)-1,-1,-1):
                                self.stacknode.put(commandlist[i])

                            # self.tree.show_tree()


                            #发送命令
                            if not self.stacknode.empty():
                                self.fac_test_to_main_trigger.emit(self.current_consolethread,self.stacknode.get())
                            # for command_index in range(len(commandlist)):
                                # self.fac_test_to_main_trigger.emit(self.current_consolethread, commandlist[command_index])
                                self.fac_auto_test_overtime = False 
                                self.fac_auto_test_timer.start(20*60*1000) #定时器是ms为单位，定时时间20分钟
                                
                                #从运行字典中查找是否有需要运行所需发送内容
                                print("待测试信息名",test_name_list[command_index])
                                print("need_send_command_key",self.find_dict_value_of_key(self.send_info,test_name_list[command_index]))
                                needed_send_command_key = self.find_dict_value_of_key(self.send_info,test_name_list[command_index])
                                if needed_send_command_key != None:
                                    needed_send_command = self.send_info[needed_send_command_key]
                                    time.sleep(5)
                                    print("needed_send_command",needed_send_command)
                                    GlobalVariable.log_data_buffer = ""
                                    self.fac_test_to_main_trigger.emit(self.current_consolethread, needed_send_command)

                                #等待运行结束 或者超时20分钟未打印新字符
                                print(self._judge_one_test_over(),self.fac_auto_test_overtime)
                                while self._judge_one_test_over() != True and self.fac_auto_test_overtime == False:
                                    print("等待运行结束...")
                                    time.sleep(5)

                                # #判断是否还是在相同菜单,如果是不同菜单，说明进入了二级菜单，而不是实际测试。
                                # command_sub_list = self.search_test_item(GlobalVariable.log_data_buffer)
                                # if command_sub_list == commandlist:
                                #     break
                                
                                #判断是否出现需要用户输入的[Yes/no]等字眼，如果是则自动输入
                                for i in self.waiting_manu_press_yes_list:
                                    if self.matchlog(i,GlobalVariable.log_data_buffer) != False:
                                        GlobalVariable.log_data_buffer = ""
                                        #发送yes
                                        self.fac_test_to_main_trigger.emit(self.current_consolethread, "yes")

                                
                                #判断测试是否pass
                                if self._judge_pass_or_not(GlobalVariable.log_data_buffer) == False:
                                    #保存失败的log数据
                                    print("开始保存失败log信息...")
                                    self.fac_auto_test_log.write(str(datetime.now())+":\r\n")
                                    self.fac_auto_test_log.write(GlobalVariable.log_data_buffer)
                                #测试完单项，清空log缓存
                                GlobalVariable.log_data_buffer = ""


                        else:
                            print("查找到的生测菜单出错！！！")

        self.finished.emit() 
        self.fac_auto_test_log.close()

                        
                        
                        
                        

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
        need_match_name = "    (\w. .*)\r\n"
        match_num_list = self.matchlog(need_match_text, log_data)
        match_name_list = self.matchlog(need_match_name, log_data)
        if match_num_list != False:
            return match_num_list, match_name_list
        else: return False
        

    def _judge_one_test_over(self):
        for i in self.judge_over_diction:
            print("进行匹配：",self.matchlog(i, GlobalVariable.log_data_buffer))
            if self.matchlog(i, GlobalVariable.log_data_buffer) != False:
                #程序运行结束
                print("命令发送且该命令测试结束")
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

    def find_dict_value_of_key(self,dictionary,findname):
        print("待找的字典和key名：",dictionary,findname)
        key_list = list(dictionary.keys())
        for i in range(len(key_list)):
            print("索引值",i)
            if re.findall(findname,key_list[i]) != []: 
                print("返回完整key值：",dictionary[list(dictionary.keys())[i]])
                return list(dictionary.keys())[i]
        # return False


