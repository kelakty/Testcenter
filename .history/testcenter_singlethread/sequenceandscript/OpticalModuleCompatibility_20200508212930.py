from AutomationScript import CRT
from PyQt5.QtWidgets import QMessageBox
from globalvariable import GlobalVariable
from PyQt5.QtCore import QThread
import threading
CRT=CRT()
CRT.Info("开始运行脚本")

CRT.MessageBox("information","提示","是否现在开始测试")
CRT.MessageBox("information","提示","请按照测试指南搭建好打流模型")
count_flag=1
while count_flag==1:
    CRT.SendAndWaitString("show int te0/1 transceiver\r\n",1,"sh in te0/25 transceiver",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("show int te0/1 transceiver alarm\r\n",1,"show int te0/1 transceiver alarm",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("show int te0/1 transceiver manu\r\n",1,"show int te0/1 transceiver manu",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("show int te0/1 transceiver diagnosis\r\n",1,"show int te0/1 transceiver diagnosis",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.MessageBox("information","提示","查看端口LED是否点灯？")
    CRT.MessageBox("information","提示","现在开始切换测试")
    CRT.SendAndWaitString("con\r\n",1,"ruijie",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("int r te0/1-2\r\n",1,"ruijie",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("speed 1000\r\n",1,"speed 1000",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("sh in sta\r\n",1,"sh in sta",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.MessageBox("information","提示","查看端口LED是否点灯？")
    CRT.SendAndWaitString("speed 10g\r\n",1,"speed",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.SendAndWaitString("sh in sta\r\n",1,"speed",CompileFlag="IGNORECASE",EmptyBuffer=1)
    CRT.MessageBox("information","提示","查看端口LED是否点灯？")

    count_flag=CRT.MessageBox("information","提示","是否继续下一轮测试？")
CRT.MessageBox("information","提示","现在开始自协商测试")
CRT.SendAndWaitString("con\r\n",1,"ruijie",CompileFlag="IGNORECASE",EmptyBuffer=1)
CRT.SendAndWaitString("int r te0/1-2\r\n",1,"ruijie",CompileFlag="IGNORECASE",EmptyBuffer=1)
CRT.SendAndWaitString("speed 1000\r\n",1,"speed 1000",CompileFlag="IGNORECASE",EmptyBuffer=1)
CRT.SendAndWaitString("sh in sta\r\n",1,"sh in sta",CompileFlag="IGNORECASE",EmptyBuffer=1)

CRT.InputCheckDialog()
# print(CRT.WaitForString("ABC",CompileFlag="IGNORECASE"))

print("结束运行脚本")
