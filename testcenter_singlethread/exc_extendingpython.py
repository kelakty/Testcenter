import os
import subprocess
import sys
from subprocess import Popen, PIPE
from AutomationScript import CRT
import re
from re import RegexFlag
from PyQt5.QtCore import QByteArray

# dir=r"D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\sequenceandscript\testautoscript.py"
# command = "python "+dir
# print("文件名：",command)
"""
crt=CRT()
print("crt对象为：",crt)
crt_str=str(crt)
print("crt对象string为：",crt_str)
num1=100
num2="AutomationScript.CRT object at 0x0000000003F5FEB8"
# results=os.system(r'python D:\testcenter20190116备份（增加qtextedit中进行发送命令）\testcenter20190102备份\testcenter\testcenter_pyqt5\testautoscript.py %s %d' % (num1,num2))
# print("1运行结果：",results)

get_filename="D:/testcenter20190116备份（增加qtextedit中进行发送命令）/testcenter20190102备份/testcenter/testcenter_pyqt5/testautoscript.py"
command="python "+get_filename+" "+"%s"+" "+"%s"
print('待测python文件命令为：',command)
results=os.system(command % (num1,num2))
print("1运行结果：",results)

result5=os.system('python "{}" {} {}'.format(get_filename,num1,num2))
print("5运行结果：",result5)

command2="python "+get_filename
process =Popen([sys.executable, command2,str(num1) ,str(num2)  ], stdout=PIPE, stderr=PIPE,shell=True)  #['python ', "C:\\Users\\seeker\\Desktop\\testautoscript.py"]
stdout, stderr = process.communicate()
print("6运行结果stdout：", stdout.decode('utf-8'))
print("6运行结果process：", process)
# result2=os.system(command)
# print("2运行结果：",result2)

# result3=os.system("python C:\\Users\\seeker\\Desktop\\testautoscript.py num1 num2")
# print("3运行结果：",result3)


# command2="C:/Users/seeker/Desktop/testautoscript.py"
# command3=command2.replace('/','\\')
# print(command3)

# with open("C:/Users/seeker/Desktop/vlan_gen.txt","rb") as file:
#     data = file.read()     #decode('gb18030', 'ignore')
# print(data)

# exec(open("C:/Users/seeker/Desktop/testautoscript.py","rb").read())
"""


"""
receivebuffer=b'tartedabcdsef\r\r'
def WaitForString( waitstring ,**kwargs):
    if kwargs['CompileFlag'] !='':
        print(kwargs['CompileFlag'])
        if kwargs['CompileFlag'] == "IGNORECASE":
            compileflag=re.IGNORECASE
        if kwargs['CompileFlag'] == "DOTALL":
            compileflag=re.DOTALL
        if kwargs['CompileFlag'] == "LOCALE":
            compileflag=re.LOCALE
        if kwargs['CompileFlag'] == "MULTILINE":
            compileflag=re.MULTILINE
        if kwargs['CompileFlag'] == "VERBOSE":
            compileflag= re.VERBOSE

        return re.findall(waitstring,receivebuffer.decode('gb2312') ,compileflag)
        # re.findall(waitstring,receivebuffer.decode('gb2312') ) 
print(WaitForString("abc" , CompileFlag="IGNORECASE"))
"""

# def WaitForString( waitstring ,**kwargs):
#     print(waitstring)
#     print(kwargs['CompileFlag'])
# WaitForString("abc" , CompileFlag="re.I")



# get_filename="D:/testcenter20190116备份（增加qtextedit中进行发送命令）/testcenter20190102备份/testcenter/testcenter_pyqt5/testautoscript.py"
# exec(open(get_filename,"rb").read())

receivebuffer=QByteArray(b'abc\r\r\n')
waitstring='AbC'
compileflag=re.IGNORECASE
matchingdata=re.findall(waitstring,receivebuffer.data().decode('gb2312') ,compileflag)
print("matchingdata is ",matchingdata)



