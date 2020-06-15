# from PyQt5.QtSerialPort import QSerialPortInfo, QSerialPort
# from PyQt5.QtWidgets import QWidget
# from PyQt5.QtWidgets import QMainWindow

import time
import re
from globalvariable import GlobalVariable



# from testcenter import encodingType  #无法传递
# import testcenter

class TestCommandSession():
    #属性
    

    def __init__(self, *args, **kwargs):
        pass


    def setMain(self, main_window):
        self.mainwindow = main_window

    def sendcommandlist(self,commandlist):
        #在这里处理发送的命令序列
        for index in range(len(commandlist)):
            if re.search(r"delay\(\d+\)",commandlist[index]) != None:
                t=re.findall(r"delay\((\d+)\)",commandlist[index])
                time.sleep(t[0])
            elif re.search(r"search\(.*\)",commandlist[index]) != None:
                pass  #在这里处理自动搜索匹配log
            elif re.search(r"findall\(.*\)",commandlist[index]) != None:
                pass  #在这里处理自动搜索匹配log
            elif  re.findall(r"@\d+@\d+@([ -~]+\r\n)",commandlist[index]) != None:
                waitedsendcommand = re.findall(r"@\d+@\d+@([ -~]+\r\n)",commandlist[index])
                print(waitedsendcommand)
                self.mainwindow._serial.write(waitedsendcommand[0].encode(GlobalVariable.encodingType))
                # self.mainwindow._serial.write("\r\n".encode(GlobalVariable.encodingType))
            else :
                print("未发现测试命令")
  
        
    def addcommandtolist(self,testcommand):
        #添加测试命令到测试命令序列
        pass
    
    def delsomecommand(self,index,num):
        #删除部分测试命令，索引以及数量
        pass

    def delallcommand(self):
        #删除所有测试命令
        pass

# #转换脚本为命令序列
# class ConvertToSessions(TestCommandSession):
#     pass


# def start_test(TestCommandSessions):
#     pass

# def start_autotest(TestCommandSessions):
#     pass