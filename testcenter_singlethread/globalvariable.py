#全局变量存放
import os
class GlobalVariable():
    defaultEncodingType='utf-8'    #配置默认控制台发送编码方式
    encodingType='utf-8'
    testcommandlist = []
    commandlist_num=0
    case_num=0
    receivebuffer=b''
    serialreaddata=b''

    #quickcommand
    quickcommand_number=0
    quickcommand_setting_list=[]     #快速命令的配置生成信息
    quickcommand_list=[]    
    quickcommand_namelist=[]
    configfilename=os.getcwd()+r"\config.ini"  #保存配置文件的路径
    hoverd_action=""
    