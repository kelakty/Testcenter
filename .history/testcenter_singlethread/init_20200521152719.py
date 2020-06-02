import os

class Init():

    def config_init(self):
    """
    加载初始化配置文件
    """ 
    if  not os.path.exists(GlobalVariable.configfilename): 
        read_line_configfile=open(GlobalVariable.configfilename, "w")
        read_line_configfile.close()
    else: 
        read_line_configfile= open(GlobalVariable.configfilename, "r")
        i=0
        find=0
        commandlist=[]
        for j in read_line_configfile:
            print("oneline:",j)
            print("onelinetype:",type(j))
            j=j.replace("\n","")
            if re.search("}quickcommand\d+",j) != None:
                find=0
                i=0
                GlobalVariable.quickcommand_setting_list.append(commandlist)
                commandlist=[]
            if find==1:   
                if i==0:  #第0行指令，为了提取标签名到list
                    GlobalVariable.quickcommand_namelist.append(j) 
                    i+=1  
                    continue 
                if i==1:
                    GlobalVariable.quickcommand_list.append(j) 
                    i+=1  
                    continue 
                j=j.replace(".mainwindow","")
                print(j)
                print(GlobalVariable.quickcommand_list)
                exec(j)
                commandlist.append(j)
            if re.search("quickcommand\d+:{",j) != None:
                find=1
                number=re.findall("(\d+)",j)
                if number != []:    
                    GlobalVariable.quickcommand_number=int(number[0])+1  #提取命令编号
                commandlist=[]
        #打印调试
        print("打印调试quickcommand_setting_list:",GlobalVariable.quickcommand_setting_list)
        
        print("打印调试quickcommand_list:",GlobalVariable.quickcommand_list)
        
        print("打印调试quickcommand_namelist:",GlobalVariable.quickcommand_namelist)
        read_line_configfile.close()   