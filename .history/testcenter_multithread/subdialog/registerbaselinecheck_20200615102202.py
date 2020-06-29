# -*- coding: utf-8 -*-

"""
Module implementing RegisterBaseLineCheck.
"""
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot,QDir,QCoreApplication,QStandardPaths,QByteArray 
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
import pandas as pd

import re
import time
from .Ui_registerbaselinecheck import Ui_RegisterBaseLineCheck
from globalvariable import GlobalVariable

from datetime import datetime, timedelta

encodingType=GlobalVariable.defaultEncodingType
class RegisterBaseLineCheck(QWidget, Ui_RegisterBaseLineCheck):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(RegisterBaseLineCheck, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Dialog)  #重要！让窗口置顶显示

        self.setupUi(self)
        self.getdata=[]
        GlobalVariable.openreceivebuffer = True   #开启接收 log缓存

    def setMain(self, main_window):
        self.mainwindow=main_window

    def closeEvent(self, event):
        
        GlobalVariable.openreceivebuffer = False  #关闭串口是关闭 接收log缓存
        super(self).closeEvent(parent)
        
    def brosebaselinedir(self):
        # fileName, path = QFileDialog.getOpenFileName(self, "Open File",QCoreApplication.applicationDirPath())
        # print(QStandardPaths.standardLocations(0))
        # print(QStandardPaths.standardLocations(0)[0])

        #选择单个待测Baseline的excel文件。如果使用的是QFileDialog.getOpenFileNames则可以同时选择多个文件
        choosefilename, _ = QFileDialog.getOpenFileName(self, "选取文件",QStandardPaths.standardLocations(0)[0],
                            "Excel Files (*.xlsx *.xls);;All Files (*)")
        # print(choosefilename)
        if choosefilename:
            self.lineEdit_register_base_line_dir.setText(choosefilename) 
        self.gen_filename=self.lineEdit_register_base_line_dir.text()
            
    def baselinetest(self):
        index = self.mainwindow.find_dictionarylist_keyvalue_index(GlobalVariable.Console, "subwindowobj", self.mainwindow.mdiArea.currentSubWindow())
        
        self.choosefilename = self.lineEdit_register_base_line_dir.text()
        self.gen_filename=self.choosefilename
        print(self.choosefilename)
        # self.mainwindow._serial.write("insmod /sbin/dram_hwtest.ko\r\n".encode(encodingType))
        GlobalVariable.Console[index]["consolethread"].send_trigger.emit("insmod /sbin/dram_hwtest.ko\r\n".encode(GlobalVariable.Console[index]["encodingtype"]))
        self.registerbaseline = pd.read_excel(self.choosefilename, sheet_name = '寄存器基线')
        
        self.all_register_address = self.registerbaseline.loc[:,'寄存器地址'].values
        # print("读取指定行的数据：",self.all_register_address)
        GlobalVariable.receivebuffer = b""   #测试前先将接收buffer清空
        
        for i in range(len(self.all_register_address)):
            registeraddress_command="hw_test.bin reg_rd64 "+self.all_register_address[i]+"\r\n"
            # print("准备发送的数据：",registeraddress_command)
            # self.mainwindow._serial.write(str(registeraddress_command).encode(encodingType)) 
            GlobalVariable.Console[index]["consolethread"].send_trigger.emit(str(registeraddress_command).encode(GlobalVariable.Console[index]["encodingtype"]))
        """
        #单个地址的测试，已废弃
        x=0
        y=1
        self.registeraddress=registerbaseline.ix[x,y]#读取第一行第二列的值，这里不需要嵌套列表
        print("读取指定行的数据：",self.registeraddress)
        print("读取指定行的数据类型：",type(self.registeraddress))

        registeraddress_command="hw_test.bin reg_rd64 "+self.registeraddress+"\r\n"
        print("待读取寄存器指令：",registeraddress_command)

        print("测试前buffer数据",GlobalVariable.receivebuffer)
        GlobalVariable.receivebuffer=b""   #先将接收buffer清空
        print("清空后buffer数据",GlobalVariable.receivebuffer)

        self.mainwindow._serial.write(str(registeraddress_command).encode(encodingType)) 
        #发送完指令后，读取信息应该放在外面处理，否则串口未接收到数据
        # registerdata=QByteArray(GlobalVariable.receivebuffer).data().decode(encodingType)          #.data().decode(encodingType)
        # print("测试后buffer数据",GlobalVariable.receivebuffer)
        # GlobalVariable.receivebuffer=b""   #接收buffer清空
        # print("串口终端返回的寄存器信息：",registerdata)

        # registeraddress=str(registeraddress)
        # reg_search=registeraddress[5:]+": 0x(\w{16})"
        # getdata=re.findall(reg_search,registerdata)
        # print(getdata)
        """
    
    def gen_bit_compare_list(self,one_column_list):
        """
        输入一个寄存器基线表格的“寄存器位组成”的列，一维列表
        返回一个寄存器按位组成的二维列表
        """
        # self.registerbaseline.loc[:,'寄存器位组成'].values
        two_dimension_list=[]
        registerbaseline = pd.read_excel("C:/Users/seeker/Desktop/M7810C-CM寄存器.xlsx", sheet_name = '寄存器基线')
        one_column_list=registerbaseline.loc[:,'寄存器位组成'].values

        # two_dimension_list=two_dimension_list.append(bit_compare_list[i].split('\r\n')  for i in range(len(bit_compare_list)))
        # # a.split(' ')[0]
        # print(two_dimension_list)

        for i in range(len(one_column_list)):
            string_list=re.split(" |\r\n|\n|/|<|>",one_column_list[i])
            while '' in string_list:
                string_list.remove('')
            two_dimension_list.append(string_list) 
        print(two_dimension_list)

        for i in range(len(two_dimension_list)):
            num_list=[]
            for j in range(len(two_dimension_list[i])):
                # print(type(two_dimension_list[i][j]))
                print(two_dimension_list[i][j])
                if two_dimension_list[i][j].find("~") != -1 or two_dimension_list[i][j].find(":") !=-1:
                    # print("开始处理字符串",i,j)
                    v=re.split("~|:",two_dimension_list[i][j])
                    a1=int(v[0])
                    a2=int(v[1])
                    step = 1 if a1 <= a2 else -1
                    num_list.extend(list(range(a1,a2+step,step)))
                    # two_dimension_list[i][j]=num_list
                    # print(two_dimension_list[i][j])
                else:
                    num_list.append(int(two_dimension_list[i][j]))
                    # two_dimension_list[i][j]=num_list
                    # print(two_dimension_list[i][j])
            two_dimension_list[i]=num_list
        #     print(two_dimension_list[i][j])
        # print("最终输出字符串:",two_dimension_list)
        return two_dimension_list

    def gen_bit_compare_list(self,one_column_list):
        """
        输入一个寄存器基线表格的“寄存器位组成”的列，一维列表
        返回一个寄存器按位组成的二维列表
        """
        # self.registerbaseline.loc[:,'寄存器位组成'].values
        two_dimension_list=[]
        # registerbaseline = pd.read_excel("C:/Users/seeker/Desktop/M7810C-CM寄存器.xlsx", sheet_name = '寄存器基线')
        # one_column_list=registerbaseline.loc[:,'寄存器位组成'].values

        # two_dimension_list=two_dimension_list.append(bit_compare_list[i].split('\r\n')  for i in range(len(bit_compare_list)))
        # # a.split(' ')[0]
        # print(two_dimension_list)

        for i in range(len(one_column_list)):
            # print(type(one_column_list[i]))
            string_list=re.split(" |\r\n|\n|/",str(one_column_list[i]))
            while '' in string_list:
                string_list.remove('')
            two_dimension_list.append(string_list) 
            # print("分割字符串：",string_list)
        # print(two_dimension_list)

        for i in range(len(two_dimension_list)):
            num_list=[]
            for j in range(len(two_dimension_list[i])):
                # print(type(two_dimension_list[i][j]))
                # print(two_dimension_list[i][j])
                if two_dimension_list[i][j].find("~") != -1 or two_dimension_list[i][j].find(":") !=-1:
                    # print("开始处理字符串",i,j)
                    v=re.split("~|:",two_dimension_list[i][j])
                    a1=int(v[0])
                    a2=int(v[1])
                    step = 1 if a1 <= a2 else -1
                    num_list.extend(list(range(a1,a2+step,step)))
                    # two_dimension_list[i][j]=num_list
                    # print(two_dimension_list[i][j])
                else:
                    num_list.append(int(two_dimension_list[i][j]))
                    # two_dimension_list[i][j]=num_list
                    # print(two_dimension_list[i][j])
            two_dimension_list[i]=num_list
        #     print(two_dimension_list[i][j])
        # print("最终输出字符串:",two_dimension_list)
        return two_dimension_list

    def fillarray_to_64bit(self,one_list):
        if len(one_list) <64:
            # print("into extend:",len(one_list))
            one_list.extend("0"*(64-len(one_list)))
        # print(one_list)
        return one_list

    def two_dimension_list_setzeros(self,two_D_list):
        zeroslist=[]
        def foo(x):
            x=x if x==0 else 0
            return x
        for i in range(len(two_D_list)):
            zeroslist.append(list(map(foo,two_D_list[i])))
        return zeroslist

    def bit_compare(self,baselinedata_list,getdata_list,two_dimension_positionbybit_list):
        # registerbaseline = pd.read_excel("C:/Users/seeker/Desktop/M7810C-CM寄存器.xlsx", sheet_name = '寄存器基线')
        # getdata_list=registerbaseline.loc[:,'寄存器值'].values
        # one_column_list=registerbaseline.loc[:,'寄存器位组成'].values
        # getdata_list2=['0x0000000000000001','0x0000060A000A000A','0x00000020A1FF1200', '0x013FFC2082249041', '0x00000020A1FF1400']
        # data=str(0x0001180000002000)
        error_bit_list=[[] for _ in range(len(two_dimension_positionbybit_list))] 
        print("error_bit_list",error_bit_list)
        # print("two_dimension_positionbybit_list",two_dimension_positionbybit_list)
        #先判断下基线列表与实际读出寄存器值列表大小是否相等
        if len(baselinedata_list) == len(getdata_list):
            for i in range(len(baselinedata_list)):
                print("基线值：",baselinedata_list[i])
                baselinebit_data=list(bin(int(baselinedata_list[i], 16))[2:].zfill(8))
                baselinebit_data.reverse()
                print("基线二进制值：",baselinebit_data)
                getbit_data=list(bin(int(getdata_list[i], 16))[2:].zfill(8))
                getbit_data.reverse()
                print("实际读出二进制值：",getbit_data)
                #填充序列到64bit：
                baselinebit_data=self.fillarray_to_64bit(baselinebit_data)
                getbit_data=self.fillarray_to_64bit(getbit_data)

                # for j in range(len(two_dimension_positionbybit_list[i])):
                errorbit=[]
                for j in two_dimension_positionbybit_list[i]:
                    if getbit_data[j] == baselinebit_data[j]:
                        pass
                    else:
                        #将对应位标记处理
                        errorbit.append(j)
                        
                error_bit_list[i].extend(errorbit)
                # print("errorbit:",errorbit)
                # print("errobitlist:",error_bit_list)   
        else:
            
            QMessageBox.information('警告','寄存器基线值行数与实际读出值行数不同，请修改',QMessageBox.Ok) 
        return error_bit_list

    def generate_baselinereport(self):
        
        registerbaseline = pd.read_excel(self.gen_filename, sheet_name = '寄存器基线')
        
        getdata_list=registerbaseline.loc[:,'实际读出值'].values
        baselinedata_list=registerbaseline.loc[:,'寄存器值'].values
        # print("getdata:",getdata_list)
        one_column_list=registerbaseline.loc[:,'寄存器位组成'].values   
        # print("onecolumn:",one_column_list)
        two_dimension_positionbybit_list=self.gen_bit_compare_list(one_column_list)
        error_bit_list=self.bit_compare(baselinedata_list,getdata_list,two_dimension_positionbybit_list)
        print(error_bit_list)
        registerbaseline.loc[:,'错误寄存器位']=error_bit_list

        #生成excel处理
        writer = pd.ExcelWriter(self.gen_filename)
        self.excel_workbook_format(writer,registerbaseline)  #workbook格式处理
        writer.save()

    def generate_baselineexcel(self):
        self.getdata=[]
        registerdata=QByteArray(GlobalVariable.receivebuffer).data().decode(encodingType)          #.data().decode(encodingType)
        # print("测试后buffer数据",GlobalVariable.receivebuffer)
        GlobalVariable.receivebuffer=b""   #接收buffer清空
        print("串口终端返回的寄存器信息：",registerdata)
        print("所有寄存器地址：",self.all_register_address)
        for i in range(len(self.all_register_address)):
            registeraddress=str(self.all_register_address[i])
            reg_search=registeraddress[5:]+": 0x(\w{16})"
            pattern=re.compile(reg_search,re.I)
            # reg_search="reg_rd64 "+registeraddress  #临时测试
            # print("getdata:",self.getdata)
            # print("finddata",re.findall(reg_search,registerdata))
            searchdata=pattern.findall(registerdata)
            if searchdata==[]:
                self.getdata.append("Error")
            else:
                self.getdata.append(searchdata[0])
            print("找到的寄存器值：",self.getdata)
        # print(self.registerbaseline)
        self.registerbaseline.loc[:,'实际读出值']=self.getdata
        #比较寄存器基线值，并设定颜色
        # bin(int(self.getdata[0], scale))[2:].zfill(num_of_bits)


        #写入excel
        date = datetime.now().date()   #- timedelta(days=1)
        time=datetime.now().time()
        choosefilename=self.choosefilename.replace('.xlsx', '')
        print("临时变量choosefilename",choosefilename)
        print("self变量choosefilename",self.choosefilename)
        self.gen_filename=choosefilename+"_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
        self.registerbaseline.to_excel(self.gen_filename,sheet_name='寄存器基线',index=False)

    #########excel处理相关#########
    def convertToTitle(self,n):
            """
            将数字转换为Excel表格列中的ABCD
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

    def convertToTitle2(self,n):
            """
            将数字转换为Excel表格列中的ABCD
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

    #对excel的workbook设置格式
    def excel_workbook_format(self,writer,registerbaseline):

        # writer = pd.ExcelWriter('C:/Users/seeker/Desktop/M7810C-CM寄存器3.xlsx')
        workbook=writer.book
        #设置格式
        fmt = workbook.add_format({"font_name": u"微软雅黑"})  #设置字体
        # border_format = workbook.add_format({'border': 1})  #设置边框
        # red_fmt = workbook.add_format({'color': 'red'})
        # blue_fmt=workbook.add_format({'color':'blue'})
        # navy_fmt=workbook.add_format({'color':'navy'}) # 'brown''cyan''gray' 'green' 'lime' 'magenta''navy''orange' 'pink''purple''red' 'silver''white''yellow'
        bluegreen_fmt=workbook.add_format({'bg_color':'#5DB78E'})
        red_bg_fmt=workbook.add_format({'bg_color':'#FF0000'})
        # percent_fmt = workbook.add_format({'num_format': '0.00%'})  #设置数字格式
        # amt_fmt = workbook.add_format({'num_format': '#,##0'})#设置数字格式
        # note_fmt = workbook.add_format(
        #         {'bold': True, 'font_name': u'微软雅黑', 'font_color': 'red', 'align': 'left', 'valign': 'vcenter'})
        # date_fmt = workbook.add_format({'bold': False, 'font_name': u'微软雅黑', 'num_format': 'yyyy-mm-dd'})
        # date_fmt1 = workbook.add_format(
        #         {'bold': True, 'font_size': 10, 'font_name': u'微软雅黑', 'num_format': 'yyyy-mm-dd', 'bg_color': '#9FC3D1',
        #         'valign': 'vcenter', 'align': 'center'})
        # highlight_fmt = workbook.add_format({'bg_color': '#FFD7E2', 'num_format': '0.00%'})
        highlight_lightblue_fmt = workbook.add_format({'bg_color': '#B5E9E1'}) #设置背景色
        normal_fmt=workbook.add_format({"font_name": u"微软雅黑",'align': 'left','valign': 'vcenter','border': 1})
        
        registerbaseline.to_excel( writer,sheet_name='寄存器基线',index=False)
        worksheet1 = writer.sheets[u'寄存器基线']

        r_end = len(registerbaseline.index) + 2
        # print("转换得到：",convertToTitle2(5))
        c_end=self.convertToTitle(len(registerbaseline.columns))
        # print("l_end",r_end)
        # print("c_end",c_end)
        worksheet1.set_column('A:F' , 20)   #设置列宽和格式
        worksheet1.set_column('N:N' , 15)   #设置列宽和格式
        # worksheet1.set_column('A:%s' % c_end , 15, normal_fmt) #设置列宽和格式
        worksheet1.set_column('M:M' , 21,fmt) 
        worksheet1.conditional_format('A1:%s%d' % ( c_end , r_end) , {'type': 'no_blanks', 'format': normal_fmt}) #type只对非空单元格设置格式
        # worksheet1.add_sparkline('N2', {'high_color': True})
        # worksheet1.write_rich_string('%s%d' % ( c_end , l_end) ,red_fmt,"this is")
        worksheet1.set_column('G:L' , None ,None,{'hidden':True }  )  #将G-L列隐藏
        worksheet1.conditional_format('M1:M%d' %  r_end , {'type': 'no_blanks', 'format': highlight_lightblue_fmt})

        #处理错误位标记为红色，正确的标记为绿色
        errorbit_list=registerbaseline.loc[:,'错误寄存器位'].values
        for i in range(len(errorbit_list)):
            if errorbit_list[i] == []:
                worksheet1.conditional_format('N%d' %  int(i+2) , {'type': 'no_blanks', 'format': bluegreen_fmt})
            else:
                worksheet1.conditional_format('N%d' %  int(i+2) , {'type': 'no_blanks', 'format': red_bg_fmt})

    @pyqtSlot()
    def on_pushButton_browse_RBL_dir_clicked(self):
        """
        Slot documentation goes here.
        """
        self.brosebaselinedir()
    
    @pyqtSlot()
    def on_startRegisterBaseLine_Test_clicked(self):
        """
        点击寄存器基线测试对话框的“开始测试”
        """
        # try:
        self.baselinetest()
        QMessageBox.information(self, '提示','已发送指令到控制台，请查看控制台收发是否正确',QMessageBox.Ok)
        # except Exception as result:
        #     print("未知错误%s" % result)
        #     QMessageBox.critical(self, '警告','未知错误，请检查表格格式一致后重试。表格sheet页名必须为“寄存器基线”',QMessageBox.Yes)
        
    @pyqtSlot()
    def on_generateRegisterBaseLineExcel_clicked(self):
        """
        点击寄存器基线测试对话框的“生成表格”
        """
        try:
            reply=QMessageBox.question(self, '注意','测试前是否已关闭待测试的寄存器基线文档？未关闭会报错',QMessageBox.Yes | QMessageBox.Cancel,QMessageBox.Cancel)
            # print("接收到的reply：",reply)
            if reply==QMessageBox.Yes:
                # print("开始测试")
                self.generate_baselineexcel()
                QMessageBox.information(self, '提示','已自动提取寄存器值存入到基线文档，请查看基线文档中寄存器值是否正确',QMessageBox.Yes)
        except Exception as result:
            print("未知错误%s" % result)
            QMessageBox.critical(self, '警告','未知错误，请检查是否关闭表格后重试',QMessageBox.Yes)

    @pyqtSlot()
    def on_generateRegisterBaseLineReport_clicked(self):
        """
        点击寄存器基线测试对话框的“使用表格生成报告”.
        """
        try:
            self.generate_baselinereport()
        except Exception as result:
            print("未知错误%s" % result)
            QMessageBox.critical(self, '警告','表格异常，请检查寄存器位组成（位组成没有出现异常字符，没有出现14~128等异常位组成）、寄存器值、实际读出值是否有空单元格(有空单元格需要补充或者删除整列)，检查是否有隐藏的行列，修改后重试',QMessageBox.Yes)

