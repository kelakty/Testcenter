

from PyQt5.QtCore import  QByteArray
from datetime import datetime
serialreaddata=b'System description : Ruijie Gibabit Ethernet Switch(S1920-8GT2SFP) By Ruijie Networks\r\r\nSystem start time'
i=0
new_serialdata=''
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

print(serialdata_list)

for x in serialdata_list:
    print(x)

date = datetime.now().date()   #- timedelta(days=1)
time=datetime.now().time()
print("data is :",date)
print("time is :",time)

print(date.year, date.month, date.day,time.hour,time.minute,time.second)
print(datetime.now().date(),datetime.now().time())
print(datetime.now())
