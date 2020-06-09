

from PyQt5.QtCore import  QByteArray
from datetime import datetime
serialreaddata = b'Ruijie#\r\nSystem description : Ruijie Gibabit Ethernet Switch(S1920-8GT2SFP) By Ruijie Networks\r\r\nSystem start time'
serialreaddata2 = b'12:12:21\r\r\nRuijie#\r\n'

def log_joint_and_decode(residue_data, logdata, encodingtype):
    """
    数据处理后存入log，将有找到\r\n或者\r\r\n的进行回车处理，分行显示
    Args
        residue_data:传入上一次处理剩余的数据
        logdata：待处理的log数据
    Return
        datalist：处理后的log数据列表
        residue_data：处理后剩余的数据
    """
    data = logdata.decode(encodingtype)
    data_list=[]
    new_data=''
    i=0
    for x in data:
        
        if x=='\r':
            print(r"找到\r")
            i+=1
            # if i==2:
            print(i)
            continue 
        elif x=='\n' and (i > 0):
            print(r"找到\n")  #只有找到\r\n或者\r\r\n才能进行打印操作，否则
            data_list.append(new_data)
            i=0
            new_data=""
            continue 
        else:
            i=0
            new_data+=x
    if new_data != "":
        data_list.append(new_data)
    return data_list
    

data_list = loginfo_handle(serialreaddata,"gb2312")

for x in data_list:
    print("最终打印：",datetime.now(), x)