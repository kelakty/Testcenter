
# from mainwindow import MainWindow
from globalvariable import GlobalVariable
import time
import re
from re import RegexFlag
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QByteArray

encodingType=GlobalVariable.defaultEncodingType

class CRT():
    """
    脚本常用函数
    """
    global encodingType
    def __init__(self): #,  parent=None
        pass
        # super(CRT, self).__init__(parent)

    # def setMain(self, main_window):
    #     self.mainwindow=main_window

    def Send(self,sendstring):
        print("send命令发送的字符串",sendstring)
        
        # GlobalVariable.mainwindow.serial.write(chars.encode(encodingType))
        GlobalVariable.mainwindow.newthread.send_trigger.emit(sendstring.encode(encodingType))
        

    def SendAndWaitString(self,sendstring, waittime,waitstring, **kwargs):
        # GlobalVariable.mainwindow.serial.write(sendstring.encode(encodingType))
        GlobalVariable.mainwindow.newthread.send_trigger.emit(sendstring.encode(encodingType))
        self.Sleep(waittime)
        return self.WaitForString(waitstring,**kwargs)

    def SendKeys(self,sendkey):
        # GlobalVariable.mainwindow.serial.write(sendkey.encode(encodingType))
        GlobalVariable.mainwindow.newthread.send_trigger.emit(sendkey.encode(encodingType))

    def Sleep(self,waittime):
        time.sleep(waittime)

    def WaitForString(self,waitstring, **kwargs):
        compileflag=''
        matchingdata=[]
        if kwargs['CompileFlag'] !='':
            print(kwargs['CompileFlag'])
            if kwargs['CompileFlag'] == "IGNORECASE":
                compileflag=re.I
            if kwargs['CompileFlag'] == "DOTALL":
                compileflag=re.DOTALL
            if kwargs['CompileFlag'] == "LOCALE":
                compileflag=re.LOCALE
            if kwargs['CompileFlag'] == "MULTILINE":
                compileflag=re.MULTILINE
            if kwargs['CompileFlag'] == "VERBOSE":
                compileflag= re.VERBOSE
            if compileflag !="" and GlobalVariable.receivebuffer !=QByteArray(b'') :

                matchingdata=re.findall(waitstring,GlobalVariable.receivebuffer.data().decode('gb2312') ,compileflag) #注意这里使用需要先import RegexFlag
                print("compileflag is ",compileflag)
                print("matchingdata is ",matchingdata)
        elif GlobalVariable.receivebuffer != "" :
            matchingdata = re.findall(waitstring,GlobalVariable.receivebuffer.data().decode('gb2312'))
        if kwargs['EmptyBuffer'] == True:
            GlobalVariable.receivebuffer=QByteArray(b'')
        print("matchingdata is :",matchingdata)
        return matchingdata

    def SpyForString(self):
        pass

    def MessageBox(self,boxtype,title,statement):
        print("运行messagebox方法")
        command="QMessageBox."+(str(boxtype))+"(GlobalVariable.mainwindow, \""+str(title)+"\",\""+str(statement)+"\")"
        # QMessageBox.critical(self, 'title','说明')
        print("command is :",command)
        exec(command)

    def InputCheckDialog(self):
        pass

    def OpenFileCheck(self):
        pass





