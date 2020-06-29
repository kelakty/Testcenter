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
    fac_test_to_main_trigger = pyqtSignal(object, object)  #object为需要发送到的终端
    main_to_fac_test_trigger = pyqtSignal(object, str)
    finished = pyqtSignal()
    def __init__(self,current_consolethread):
        super(FactoryAutoTestWorker,self).__init__() 
        self.current_consolethread = current_consolethread

        self.judge_over_diction = ["Ruijie#","生产测试菜单","Ruijie(config)#","Ruijie(config-if-range)#",
                                        "~ #","sdk.0>","sdk.1>","sdk.2>","e exit telnet",]
        self.judge_fail_diction = ["fail","Fail","FAIL","故障","失败","端口没有link"]
        self.judge_suspicious_diction = ["不在位","N/A","NA"]
        self.judge_pass_diction = ["pass","Pass","PASS","通过","成功"]
        self.waiting_manu_press_yes_list = ["Yes/no","No/yes"] #,"Yes/No","No/yes","No/Yes"
        self.waiting_manu_press_space_key_list = ["按任意键继续"]
        self.waiting_reload_list = ["请重启"]
        self.send_info = {"0. 设置RTC时间":"2020 12 31 23:59:59\r"}
        self.do_not_test = []#'0. 产品信息检测', '1. 温度检测', '2. 内存测试',
                            #  '3. SPI Flash测试', '4. USB测试', '5. EMMC测试', 
                            #  '6. RTC测试', '7. I2C接口测试', '8. CPLD测试', 
                            #  '9. 端口收发帧测试', 'a. LED测试', 'b. 风扇状态检测', 
                            #  'c. 电源状态检测', 'd. 端口广播测试', 'e. Prbs测试', 
                            #  'f. 带外低速信号测试',
                            #  'g. 硬件双Boot测试', 
                            #  'h. CPLD/FPGA在线升级接口测试'   #'i. 管理口收发帧测试'
        self.check_info = { #"设置RTC时间":{},
                            # "产品信息检测":{},
                            # "温度检测":{},
                            # "内存测试":{},
                            # "SPI Flash测试":{},
                            # "USB测试":{},
                            # "EMMC测试":{},
                            # "RTC测试":{},
                            # "I2C接口测试":{},
                            # "CPLD测试":{},
                            # "端口收发帧测试":{},
                            # "LED测试":{},
                            # "风扇状态检测":{},
                            # "电源状态检测":{},
                            # "端口广播测试":{},
                            # "Prbs测试":{},
                            # "带外低速信号测试":{},
                            "硬件双Boot测试":{"longwaiting":1,"check":["Boot:   ","进入生产测试升级模式","进入生产测试","等待设备初始化",],"if":"No/yes","send":"yes\r"},
                            "进入调试程序界面":{"longwaiting":0,"check":["Factory>"],"if":"Factory>","send":"exit\r"}
                            # "在线升级接口测试":{},
                            # "管理口收发帧测试":{}
                            }
        

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
        # while True:
        #     self.fac_test_to_main_trigger.emit(self.current_consolethread, bytes([0x1a]))
        #     time.sleep(5)
        #     self.fac_test_to_main_trigger.emit(self.current_consolethread,"1")
        self.test_menu = {}
        do_not_test_flag = 0
        self.fac_auto_test_log = open("fac_auto_test.txt","a+")
        self.stacknode = queue.LifoQueue()
        while(not self.stacknode.empty):  self.stacknode.get()
        GlobalVariable.log_data_buffer = ""
        self.find_new_tree_node = 0
        self.fac_test_to_main_trigger.emit(self.current_consolethread,"\r")
        time.sleep(2)
        self.tree = object
        self.tree = MultiTree('main menu',"")
        # root = TreeNode('root',"")
        # self.tree.add(root)
        #一直等待直到进入生产测试菜单
        while self.matchlog("生产测试菜单", GlobalVariable.log_data_buffer) != False: 
            print("进入生测测试菜单测试")
            #判断是否为主菜单 或 是否为单项测试
            if self.matchlog("主菜单",GlobalVariable.log_data_buffer) != False or self.matchlog("    单项测试",GlobalVariable.log_data_buffer) != False: 
                #如果是单项测试菜单下，则ctrl+z返回到上级菜单，即主菜单
                if self.matchlog("    单项测试",GlobalVariable.log_data_buffer) != False: 
                    print("找到单项测试菜单")
                    GlobalVariable.log_data_buffer = ""
                    self.fac_test_to_main_trigger.emit(self.current_consolethread, bytes([0x1a]))
                    time.sleep(3)
                
                #如果是主菜单下
                if self.matchlog("主菜单", GlobalVariable.log_data_buffer) != False:
                    # print("找到主菜单",GlobalVariable.log_data_buffer)

                    commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                    print("找到的命令和测试项:",commandlist,test_name_list)
                    if commandlist != False and test_name_list != False :
                        if len(commandlist) == len(test_name_list):
                            command_dictionary = GlobalVariable.mainwindow.two_list_convert_to_keyvalue_dict(test_name_list,commandlist)
                            print("找到的命令和测试项:",commandlist,test_name_list)
                            
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
                                self.test_menu.update({test_name_list[i]:commandlist[i]})
                            # print("测试是否找到：",self.tree.if_node_name_exist_recursion(self.tree.tree, "0. 产品信息检测", search=True))  #TODO 测试
                            # print("测试是否找到：",self.tree.if_node_name_exist_recursion(self.tree.tree, "0. 设置RTC时间", search=True))  #TODO 测试
                            # print("测试菜单：",self.test_menu)
                            # self.tree.show_tree()

                            #将树逆序放入堆栈
                            for i in range(len(commandlist)-1,-1,-1):
                                self.stacknode.put([commandlist[i],test_name_list[i]])
                            print("当前初始堆栈大小：",self.stacknode.qsize())

                            #开始正式测试循环
                            while not QThread.currentThread().isInterruptionRequested():
                                print("开始循环测试")
                                # while True:pass
                                GlobalVariable.log_data_buffer = ""
                                self.fac_test_to_main_trigger.emit(self.current_consolethread,"\r")
                                time.sleep(3)
                                #如果菜单不同，不存在树中，则加入tree，放入stack
                                if GlobalVariable.log_data_buffer != "":
                                    commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                                    print("commandlist and testnamelist:",commandlist,test_name_list)
                                    if commandlist != False and test_name_list != False :
                                        for i in range(len(test_name_list)):
                                            if list(self.test_menu.keys()).count(test_name_list[i]) == 0 :
                                            # print("是否找到旧节点：",test_name_list[i],self.tree.if_node_name_exist_recursion(self.tree.tree, test_name_list[i], search=True))
                                            # if self.tree.if_node_name_exist_recursion(self.tree.tree, test_name_list[i], search=True) == None:
                                                self.find_new_tree_node = 1  #找到新节点，说明菜单不同了
                                                print("找到新节点，说明有菜单")
                                        # if len(commandlist) == len(test_name_list):
                                            # sub_command_dictionary = GlobalVariable.mainwindow.two_list_convert_to_keyvalue_dict(test_name_list,commandlist)
                                            # print("sub_and_command_dictionary:",sub_command_dictionary,command_dictionary)
                                            # print("sub_and_command_dictionary_keys:",list(sub_command_dictionary.keys()),list(command_dictionary.keys()))
                                            # for i in test_name_list:
                                        if self.find_new_tree_node == 1:
                                            print("找到新菜单,开始添加新菜单")
                                            self.find_new_tree_node = 0
                                            # if list(sub_command_dictionary.keys()) != list(command_dictionary.keys()):
                                                #菜单不同则生成tree，放入stack.菜单是否不同需要通过查找树中是否有来判断。
                                            GlobalVariable.log_data_buffer = ""
                                            self.fac_test_to_main_trigger.emit(self.current_consolethread,"\r")
                                            time.sleep(3)
                                            if GlobalVariable.log_data_buffer != "":
                                                commandlist, test_name_list = self.search_test_item(GlobalVariable.log_data_buffer)
                                                if commandlist != False and test_name_list != False :
                                                    if len(commandlist) == len(test_name_list) :
                                                        sub_command_dictionary = GlobalVariable.mainwindow.two_list_convert_to_keyvalue_dict(test_name_list,commandlist)
                                                        print("找到的命令和测试项:",commandlist,test_name_list)
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
                                                            self.test_menu.update({test_name_list[i]:commandlist[i]})
                                                        #先将返回上层菜单ctrl+z放入堆栈
                                                        self.stacknode.put([bytes([0x1a]),". ctrlz"])
                                                        #将树逆序放入堆栈
                                                        for i in range(len(commandlist)-1,-1,-1):
                                                            self.stacknode.put([commandlist[i],test_name_list[i]])
                                                        print("当前堆栈大小：",self.stacknode.qsize())
                                                        command_dictionary = sub_command_dictionary
                                                        print("sub_and_command_dictionary_keys:",list(sub_command_dictionary.keys()),list(command_dictionary.keys()))
                                        #如果菜单相同，代表在同一级菜单下，则取stack开始测试
                                        else:
                                            if not self.stacknode.empty():
                                                waiting_send_command = self.stacknode.get()
                                                print("当前堆栈中取出发送的字符是：", waiting_send_command)
                                                for i in self.do_not_test:
                                                    if i == waiting_send_command[1]: #找到在不测列表中，则跳过不测
                                                        print("找到该测试项不测试",i,waiting_send_command[1])
                                                        do_not_test_flag = 1
                                                if do_not_test_flag == 1:
                                                    do_not_test_flag = 0
                                                    print("找到该测试项不测试开始跳出")
                                                    continue
                                                
                                                GlobalVariable.log_data_buffer = ""
                                                self.fac_test_to_main_trigger.emit(self.current_consolethread, waiting_send_command[0])
                                                self.fac_auto_test_overtime = False 
                                                self.fac_auto_test_timer.start(20*60*1000) #定时器是ms为单位，定时时间20分钟
                                                
                                                #从运行字典中查找是否有需要运行所需发送内容 #TODO:下面这个index没有了，需要从command中查找名字
                                                needed_send_command_key = self.find_dict_integrity_key(self.send_info, waiting_send_command[1])
                                                if needed_send_command_key != None:
                                                    needed_send_command = self.send_info[needed_send_command_key]
                                                    time.sleep(3)  #TODO 延时待定
                                                    print("needed_send_command",needed_send_command)
                                                    GlobalVariable.log_data_buffer = ""
                                                    self.fac_test_to_main_trigger.emit(self.current_consolethread, needed_send_command)
                                                
                                                #等待运行结束 或者超时20分钟未打印新字符
                                                print("等待命令运行结束")
                                                # print(self._judge_one_test_over(),self.fac_auto_test_overtime)
                                                while self._judge_one_test_over() != True and self.fac_auto_test_overtime == False:
                                                    print("等待运行结束...")
                                                    time.sleep(3)
                                                    #判断是否出现需要用户输入的[Yes/no]等字眼，如果是则自动输入
                                                    self.whether_press_yes()
                                                    self.whether_press_space_key()
                                                self.whether_reload_system()
                                                print("命令运行结束")

                                                
                                                #从check_info中查找是否有需要特别检查的信息
                                                check_info_key_list = waiting_send_command[1].split(". ")
                                                print("待check信息的key名：",check_info_key_list)
                                                check_info_key = self.find_dict_integrity_key(self.check_info, check_info_key_list[1])
                                                if check_info_key != None: #代表找到
                                                    if self.check_info[check_info_key]["longwaiting"] == 1:
                                                        GlobalVariable.log_data_buffer = ""
                                                        check_list = self.check_info[check_info_key]["check"]
                                                        while self.fac_auto_test_overtime == False:
                                                            print("等待重启完毕...")
                                                            time.sleep(5)
                                                            i = 0
                                                            for check in check_list:
                                                                if self.matchlog(check,GlobalVariable.log_data_buffer) != False:
                                                                    i+=1
                                                            if i == len(check_list):
                                                                print("找到所有需要匹配字符")
                                                                break
                                                        print("找到所有匹配的或者超时了",self.fac_auto_test_overtime)
                                                        while self._judge_one_test_over() != True and self.fac_auto_test_overtime == False:
                                                            print("等待运行结束...")

                                                            time.sleep(3)
                                                            #判断是否出现需要用户输入的[Yes/no]等字眼，如果是则自动输入
                                                            self.whether_press_yes()
                                                            self.whether_press_space_key()
                                                        print("重新进入了生测")
                                                        self.fac_test_to_main_trigger.emit(self.current_consolethread, "1")
                                                    else:
                                                        check_list = self.check_info[check_info_key]["check"]
                                                        while self.fac_auto_test_overtime == False:
                                                            time.sleep(2)
                                                            i = 0
                                                            for check in check_list:
                                                                if self.matchlog(check,GlobalVariable.log_data_buffer) != False:
                                                                    i+=1
                                                            if i == len(check_list):
                                                                print("找到所有需要匹配字符")
                                                                break
                                                        if self.check_info[check_info_key]["if"] != "":
                                                            while self.matchlog(self.check_info[check_info_key]["if"], GlobalVariable.log_data_buffer) == False and self.fac_auto_test_overtime == False:
                                                                time.sleep(2)  #没匹配到关键字且没超时则等待
                                                            self.fac_test_to_main_trigger.emit(self.current_consolethread,self.check_info[check_info_key]["send"])
                                            


                                                #判断测试是否pass
                                                if self._judge_pass_or_not(GlobalVariable.log_data_buffer) == False:
                                                    #保存失败的log数据
                                                    print("开始保存失败log信息...")
                                                    self.fac_auto_test_log.write("\r\n****************"+str(datetime.now())+"***************:\r\n")
                                                    self.fac_auto_test_log.write(GlobalVariable.log_data_buffer)
                                                
                                                #测试完单项，清空log缓存
                                                GlobalVariable.log_data_buffer = ""
                                                print("测试完单项，并清空log缓存")
                                                time.sleep(3)
                                                # command_dictionary = sub_command_dictionary
                                                # print("sub_and_command_dictionary_keys:",list(sub_command_dictionary.keys()),list(command_dictionary.keys()))

                                            else:
                                                break
            self.finished.emit() 
            QThread.currentThread().finished.emit()
            self.fac_auto_test_log.close()
            print("fac_auto_test_log已退出")
            return

    def whether_press_yes(self):
        #判断是否出现需要用户输入的[Yes/no]等字眼，如果是则自动输入
        for i in self.waiting_manu_press_yes_list:
            if self.matchlog(i,GlobalVariable.log_data_buffer) != False:
                GlobalVariable.log_data_buffer = ""
                #发送yes
                self.fac_test_to_main_trigger.emit(self.current_consolethread, "yes\r")
                self.whether_press_yes()

    def whether_press_space_key(self):
        #判断是否出现需要用户输入的按任意键等字眼，如果是则自动输入
        for i in self.waiting_manu_press_space_key_list:
            if self.matchlog(i,GlobalVariable.log_data_buffer) != False:
                GlobalVariable.log_data_buffer = ""
                #发送yes
                self.fac_test_to_main_trigger.emit(self.current_consolethread, "\r")
                self.whether_press_space_key()
    
    def whether_reload_system(self):
        for i in self.waiting_reload_list:
            if self.matchlog(i,GlobalVariable.log_data_buffer) != False:
                GlobalVariable.log_data_buffer = ""
                #发送yes
                self.fac_test_to_main_trigger.emit(self.current_consolethread, bytes([0x1a]))
                time.sleep(2)
                self.fac_test_to_main_trigger.emit(self.current_consolethread, bytes([0x1a]))
                time.sleep(1)
                #找全局复位字眼并发送命令
                key_name = self.find_dict_integrity_key(self.test_menu, "全局复位")
                if key_name != None:
                    self.fac_test_to_main_trigger.emit(self.current_consolethread, self.test_menu[key_name])
        self.fac_auto_test_timer.stop()
        self.fac_auto_test_timer.start(20*60*1000) #定时器是ms为单位，定时时间20分钟
        while self._judge_one_test_over() != True and self.fac_auto_test_overtime == False:
            print("等待重启完成...")
            time.sleep(3)
            #判断是否出现需要用户输入的[Yes/no]等字眼，如果是则自动输入
            self.whether_press_yes()
            self.whether_press_space_key()



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
        else: return False,False
        

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

    def find_dict_integrity_key(self,dictionary,findname):
        """
        找字典中是否存在该关键字的key名，找到则返回该完整key名
        没找到则返回none
        """
        print("待找的字典和key名：",dictionary,findname)
        key_list = list(dictionary.keys())
        for i in range(len(key_list)):
            # print("索引值",i)
            if re.findall(findname,key_list[i]) != []: 
                print("返回完整key值：",dictionary[list(dictionary.keys())[i]])
                return list(dictionary.keys())[i]
        # return False

    def find_dict_integrity_value(self,dictionary,findvalue):
        """
        找字典中是否存在该关键字的value，找到则返回该完整value名
        
        """
        print("待找的字典和value：",dictionary,findvalue)
        value_list = list(dictionary.values())
        for i in range(len(value_list)):
            # print("索引值",i)
            if re.findall(findvalue,value_list[i]) != []: 
                print("返回完整key值：",dictionary[list(dictionary.values())[i]])
                return list(dictionary.values())[i]
        # return False

