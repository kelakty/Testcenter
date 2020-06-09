

from PyQt5.QtCore import  QByteArray
from datetime import datetime
serialreaddata=b'System description : Ruijie Gibabit Ethernet Switch(S1920-8GT2SFP) By Ruijie Networks\r\r\nSystem start time'
i=0
new_serialdata=''

def loginfo_handle(serialreaddata):
    """
    数据处理后存入log，将有找到\r\n或者\r\r\n的进行回车处理，分行显示
    Args
        data：待处理的log数据
    Return
        datalist：处理后的log数据列表
    """
    serialdata_list=[]
    for x in serialreaddata.decode('gb2312'):
        
        if x=='\r':
            print(r"找到\r")
            i+=1
            # if i==2:
            print(i)
            continue 
        elif x=='\n' and (i==2 or i==1):
            print(r"找到\n")  #只有找到\r\n或者\r\r\n才能进行打印操作，否则
            serialdata_list.append(new_serialdata)
            i=0
            new_serialdata=""
            continue 
        else:
            i=0
            new_serialdata+=x
    if new_serialdata != "":
        serialdata_list.append(new_serialdata)

    for x in serialdata_list:
        print("最终打印：",datetime.now().date,datetime.now().time, x)
