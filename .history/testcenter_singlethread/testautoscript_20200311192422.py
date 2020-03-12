

from AutomationScript import CRT
from PyQt5.QtWidgets import QMessageBox
from globalvariable import GlobalVariable
CRT=CRT()
print("开始运行testautoscript脚本")

a=2
b=2

CRT.MessageBox("warning","警告","这是一个警告")


if a<b:
    CRT.Send("abc\r\n")
    pass
elif a==b:
    results=CRT.SendAndWaitString("sh ver\r\n",1,"aBc",CompileFlag="IGNORECASE",EmptyBuffer=1)
    print("运行结果为：",results)
    results=CRT.SendAndWaitString("sh ver detail\r\n",1,"1.00",CompileFlag="IGNORECASE",EmptyBuffer=1)
    print("运行结果为：",results)
    results=CRT.SendAndWaitString("sh in st\r\n",1,"geg",CompileFlag="IGNORECASE",EmptyBuffer=1)
    print("运行结果为：",results)
    results=CRT.SendAndWaitString("sh pow\r\n",1,"sh pow",CompileFlag="IGNORECASE",EmptyBuffer=1)
    print("运行结果为：",results)
    results=CRT.SendAndWaitString("sh pow\r\n",1,"sh pow",CompileFlag="IGNORECASE",EmptyBuffer=1)
    print("运行结果为：",results)
else :
    # CRT.MessageBox("critical","警告","这是一个警告")
    pass
CRT.InputCheckDialog()
# print(CRT.WaitForString("ABC",CompileFlag="IGNORECASE"))
print("结束运行testautoscript脚本")
    