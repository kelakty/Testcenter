import vt102
import pyte
from vt102 import debug
import  pandas  as pd
import binascii
import xlsxwriter

from datetime import datetime, timedelta
##stream = vt102.stream()
##screen = vt102.screen((24,50))
##screen.attach(stream)
##stream.process(u"\u001b7\u001b[?47h\u001b)0\u001b[H\u001b[2J\u001b[H" +
##               u"\u001b[2;1HNetHack, Copyright 1985-2003\r\u001b[3;1" +
##               u"H         By Stichting Mathematisch Centrum and M. " +
##               u"Stephenson.\r\u001b[4;1H         See license for de" +
##               u"tails.\r\u001b[5;1H\u001b[6;1H\u001b[7;1HShall I pi" +
##               u"ck a character's race, role, gender and alignment f" +
##               u"or you? [ynq] ")
##stream.process(u"\x1b[5B")
##print(screen)

####
##screen = pyte.HistoryScreen(24, 50)
##stream = pyte.Stream(screen)
##stream.attach(screen) 
####stream.feed(u"\u001b7\u001b[?47h\u001b)0\u001b[H\u001b[2J\u001b[H")  # Move the cursor down 5 rows.
##screen.draw("!")
##print(screen.display)       #screen.display returns only the characters. 
####print(stream.display)
####print()



#hex dump of data
#00000000  48 45 4c 4c 4f 20 54 48  49 53 20 49 53 20 54 48  |HELLO THIS IS TH|
#00000010  45 20 54 45 53 54 1b 5b  31 36 44 20 20 20 20 20  |E TEST.[16D     |
#00000020  20 20 20 20 20 20 20 20  20 20 20 1b 5b 31 36 44  |           .[16D|
#00000030  20 20                                             |  |
##data = 'HELLO THIS IS T TEST\x1b[16D                \x1b[16D  '
##data = 'HELLO THIS IS T TEST \r\n1234'

###Create a default sized screen that tracks changed lines
##screen = pyte.DiffScreen(24,80)
##screen.dirty.clear()
##stream = pyte.Stream(screen)
####stream = pyte.ByteStream()
####stream.attach(screen)
##stream.feed(data)
##
###Get index of last line containing text
##last = max(screen.dirty)
##
###Gather lines, stripping trailing whitespace
##lines = [screen.display[i].rstrip() for i in range(last + 1)]
##
##print('\n'.join(lines))
##
####print(screen.buffer[0])
####print(screen.buffer[1])    #buffer[1]中的数据是一个自定义的数据结构-字典
######{0: Char(data='1', fg='default', bg='default', bold=False, italics=False, underscore=False, strikethrough=False, reverse=False),
###### 1: Char(data='2', fg='default', bg='default', bold=False, italics=False, underscore=False, strikethrough=False, reverse=False),
###### 2: Char(data='3', fg='default', bg='default', bold=False, italics=False, underscore=False, strikethrough=False, reverse=False),
###### 3: Char(data='4', fg='default', bg='default', bold=False, italics=False, underscore=False, strikethrough=False, reverse=False)}
####for key in screen.buffer[1]:
####    screen.buffer[1][key] = screen.cursor.attrs   #用于把字典key对应的值设置为默认，data为空
####	
####print(screen.buffer[1])
##
##print(screen.dirty)   #{0, 1} 显示的好像是屏幕现有的行
##print(max(screen.dirty))    #类似最后的是哪一行 行从0开始
####screen.dirty.clear()
####print(screen.dirty)   #set()
##
####screen.erase_in_display(1)   #可以清空display的数据
###Get index of last line containing text
##last = max(screen.dirty)
##
###Gather lines, stripping trailing whitespace
##
##print(screen.display)  #直接display出来的数据结构如下：是一个列表，带有默认的字符
###['HELLO THIS IS T TEST    ', '1234                    ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ', '                        ']
##
##
##print(screen.display[0]+screen.display[1])
##
####screen.display
##
####from collections import namedtuple
####Animal= namedtuple("Animal",'name age type')
####perry= Animal(name='perry',age=31,type='cat')
####print(perry)  #output:Animal(name='perry', age=31, type='cat')
####print(perry.name)  #output:perry
##
##
####class Char(namedtuple("Savepoint", [
####    "cursor",
####    "g0_charset",
####    "g1_charset",
####    "charset",
####    "origin",
####    "wrap"
####])):
####    def __new__(cls,cursor,g0_charset=12,g1_charset=1,charset=123,origin=0,wrap=0):
####        pass
####

###打印每一条的信息，包含解释的调试信息
##data = 'HELLO THIS IS T TEST \r\n1234'
##stream = pyte.Stream(pyte.DebugScreen())
##stream.feed(data)

def convertToTitle(n):
        """
        :type n: int
        :rtype: str
        """
        chaDic = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J', 11:'K'
                , 12:'L', 13:'M', 14:'N', 15:'O', 16:'P', 17:'Q', 18:'R', 19:'S', 20:'T', 21:'U'
                , 22:'V', 23:'W', 24:'X', 25:'Y', 26:'Z'}      #注意，没有0对应的字母
        rStr = ""
        while n!=0:
            if n<=26:         #存在26对应的字母
                rStr = chaDic.get(n)+rStr
                n = 0
            else:
                res = n%26
                if res == 0:     #因为没有0对应的字母，所以如果余数为0的话需要自动提出26
                    res = 26
                    n -= 26
                rStr = chaDic.get(res)+rStr
                n = n//26
        return rStr

def convertToTitle2(n):
        """
        :type n: int
        :rtype: str
        """
        rStr = ""
        while n!=0:
            res = n%26
            if res == 0:
                res =26
                n -= 26
            rStr = chr(ord('A')+res-1) + rStr
            n = n//26
        return rStr


reg_data=[]
df=pd.read_excel('C:/Users/seeker/Desktop/M7810C-CM寄存器.xlsx',sheet_name='寄存器基线')
print("首次读取到的值：",df)
data=df.loc[:,'寄存器地址'].values #读所有行的title以及data列的值，这里需要嵌套列表
for i in range(len(data)):
    reg_data.append(data[i])
print(reg_data)
df['实际读出值']=reg_data

writer = pd.ExcelWriter('C:/Users/seeker/Desktop/M7810C-CM寄存器3.xlsx')
workbook=writer.book
#设置格式
fmt = workbook.add_format({"font_name": u"微软雅黑"})
border_format = workbook.add_format({'border': 1})
percent_fmt = workbook.add_format({'num_format': '0.00%'})
amt_fmt = workbook.add_format({'num_format': '#,##0'})
bold = workbook.add_format({'bold': True})
italic = workbook.add_format({'italic': True})
note_fmt = workbook.add_format(
        {'bold': True, 'font_name': u'微软雅黑', 'font_color': 'red', 'align': 'left', 'valign': 'vcenter'})
date_fmt = workbook.add_format({'bold': False, 'font_name': u'微软雅黑', 'num_format': 'yyyy-mm-dd'})
date_fmt1 = workbook.add_format(
        {'bold': True, 'font_size': 10, 'font_name': u'微软雅黑', 'num_format': 'yyyy-mm-dd', 'bg_color': '#9FC3D1',
         'valign': 'vcenter', 'align': 'center'})
highlight_fmt = workbook.add_format({'bg_color': '#FFD7E2', 'num_format': '0.00%'})
    
df.to_excel( writer,sheet_name='寄存器基线',index=False)
worksheet1 = writer.sheets[u'寄存器基线']
##for col_num, value in enumerate(df1.columns.values):
##        worksheet1.write(1, col_num, value, date_fmt1)
worksheet1.set_column('A:E', 15, fmt)
worksheet1.write_rich_string('G1','This is ',bold, 'bold',' and this is ',italic, 'italic')
##worksheet1.merge_range('A1:B1', u'测试情况统计表', note_fmt)
### 有条件设定表格格式：金额列
##    worksheet1.conditional_format('B3:E%d' % l_end, {'type': 'cell', 'criteria': '>=', 'value': 1, 'format': amt_fmt})
##    # 有条件设定表格格式：百分比
##    worksheet1.conditional_format('E3:E%d' % l_end,
##                                  {'type': 'cell', 'criteria': '<=', 'value': 0.1, 'format': percent_fmt})
##    # 有条件设定表格格式：高亮百分比
##    worksheet1.conditional_format('E3:E%d' % l_end,
##                                  {'type': 'cell', 'criteria': '>', 'value': 0.1, 'format': highlight_fmt})
##
##    
l_end = len(df.index) + 2
c_end=convertToTitle(len(df.columns))
print("l_end",l_end)
print("c_end",c_end)
worksheet1.conditional_format('A1:%s%d' % ( c_end , l_end) , {'type': 'no_blanks', 'format': border_format})

writer.save()
writer.close()




'''
reg_data=''
data=df.loc[:,'寄存器地址'].values #读所有行的title以及data列的值，这里需要嵌套列表
##print("读取指定行的数据：",data)
##print("len",len(data))
for i in range(len(data)):
    reg_data.append(data[i])
print(reg_data)
##
##print(df)
df['实际读出值']=reg_data
print("原始寄存器值：",reg_data[0])
print("原始寄存器值：",type(reg_data[0]))
##print("binascii转换：",binascii.a2b_base64(reg_data[0]))

str_to_hex=reg_data[0].replace('0x', '')
print("原始寄存器值：",str_to_hex)
##str_to_hex=str(int(hex(str_to_hex).upper(), 16))
for c in str_to_hex:
    print(c)
    print('{:4s}'.format(bin(int(c))))

##str_to_hex=''.join([bin(int(c)).replace('0x', '') for c in str_to_hex])
##print("str_to_hex:",str_to_hex)
##print(type(str_to_hex))

##str_to_bin=' '.join([bin(ord(c)).replace('0b', '') for c in reg_data[0]])
##print("str_to_bin:",str_to_bin)


##print(df)
##df["date"].reset_index(drop=True)   #重设索引列，丢弃原来的索引列
##df.set_index('寄存器名称')
date = datetime.now().date() # - timedelta(days=1)
time=datetime.now().time()
print("当前日期：",date)
print("当前时间：",time)
choosefilename="C:/Users/seeker/Desktop/M7810C-CM寄存器.xlsx"
choosefilename=choosefilename.replace('.xlsx', '')
filename=choosefilename+"_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
print(filename)

##filename=choosefilename.insert(index,"_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second))

##df.to_excel( "C:/Users/seeker/Desktop/M7810C-CM寄存器_%d%02d%02d_%d_%02d_%02d.xlsx"% (date.year, date.month, date.day,time.hour,time.minute,time.second),sheet_name='寄存器基线',index=False)
df.to_excel( filename,sheet_name='寄存器基线',index=False)
'''

