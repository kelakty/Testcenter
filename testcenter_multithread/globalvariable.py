#全局变量存放
import os
from PyQt5.QtCore import QByteArray
class GlobalVariable():
    defaultEncodingType='utf-8'    #配置默认控制台发送编码方式
    encodingType='utf-8'
    testcommandlist = []
    commandlist_num=0
    case_num=0
    receivebuffer = QByteArray(b'')
    openreceivebuffer = False
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
    
    # #存储打开的MdiSubWindow
    # mdisubwindow_objlist=[]
    # #存储打开的串口列表
    # opencomlist=[]   #文本显示的串口列表
    # opencom_objlist=[]   #串口对象列表

    #存储打开的Telnet列表
    opentelnetlist=[]

    # #串口线程计数
    # comThreadCounter=0
    
    #当前激活的窗口
    activedTerminal=0

    #新建串口对象列表
    serial=[]

    #全局console字典列表
    Console=[]

    #待保存log处理的中间变量
    waiting_to_send = {}
    waiting_to_receive = {}

    #用于log识别的log缓存
    log_data_buffer = ""

    #测试序列的用例表格字典列表
    table_dict_list = []
    #表示sequencer线程是否在执行
    sequencer_working = False
    fac_auto_quick_test_working = False

    #sequencer等待main运行结束再执行下面的程序
    sequencer_waiting_for_main = False
    sequencer_choosefilename = ""

    #消极的词汇
    negative_vocabulary = ["fail","故障","失败","不在位","N/A","NA"]

    