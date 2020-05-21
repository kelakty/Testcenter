#全局变量存放
import os
from PyQt5.QtCore import QByteArray
class GlobalVariable():
    defaultEncodingType='utf-8'    #配置默认控制台发送编码方式
    encodingType='utf-8'
    testcommandlist = []
    commandlist_num=0
    case_num=0
    receivebuffer=QByteArray(b'')
    serialreaddata=QByteArray(b'')
    mainwindow=object()

    #quickcommand
    quickcommand_number=0
    quickcommand_setting_list=[]     #快速命令的配置生成信息
    quickcommand_list=[]    
    quickcommand_namelist=[]
    configfilename=os.getcwd()+r"\config.ini"  #保存配置文件的路径
    hoverd_action=""
    
    #串口相关设置变量：
    #当前选中串口对象地址等信息
    ComINFO={}
    SelectCom=""
    setting_stop_bit=""
    setting_data_bits=""
    setting_checksum_bits=""
    setting_baud_rate_option=""

    #存储可用串口列表
    comports_available=[]
    
    #存储打开的MdiSubWindow
    mdisubwindow_objlist=[]
    #存储打开的串口列表
    opencomlist=[]   #文本显示的串口列表
    opencom_objlist=[]   #串口对象列表

    #存储打开的Telnet列表
    opentelnetlist=[]

    #串口线程计数
    comThreadCounter=0
    
    #当前激活的窗口
    activedTerminal=0