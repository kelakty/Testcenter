from AutomationScript import CRT
from PyQt5.QtWidgets import QMessageBox
from globalvariable import GlobalVariable
from PyQt5.QtCore import QThread
import threading
CRT=CRT()
print("开始运行脚本")

CRT.MessageBox("information","提示","是否现在开始测试")
CRT.Send("aBc\r\n")

results=CRT.SendAndWaitString("sh ver\r\n",1,"aBc",CompileFlag="IGNORECASE",EmptyBuffer=1)
print("运行结果为：",results)
results=CRT.SendAndWaitString("sh ver detail\r\n",1,"description",CompileFlag="IGNORECASE",EmptyBuffer=1)
print("运行结果为：",results)
results=CRT.SendAndWaitString("sh in st\r\n",1,"duplex",CompileFlag="IGNORECASE",EmptyBuffer=1)
print("运行结果为：",results)
results=CRT.SendAndWaitString("sh pow\r\n",1,"Invalid",CompileFlag="IGNORECASE",EmptyBuffer=1)
print("运行结果为：",results)
results=CRT.SendAndWaitString("sh manu\r\n",1,"Location",CompileFlag="IGNORECASE",EmptyBuffer=1)
print("运行结果为：",results)

CRT.InputCheckDialog()
# print(CRT.WaitForString("ABC",CompileFlag="IGNORECASE"))

print("结束运行脚本")