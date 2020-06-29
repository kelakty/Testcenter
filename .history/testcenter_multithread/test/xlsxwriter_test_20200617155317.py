import xlsxwriter
import pandas as pd
from datetime import datetime
# from xlsxpandasformatter import FormatedWorksheet
import seaborn
import win32com.client as wc

path = r"C:\Users\seeker\Desktop\TES10T117-生产用软件checklist模板 20200601更新.xlsx"

class Xlsx_Write():
    def test(self):
        #读入Excel文件
        self.report_df = pd.read_excel(path, sheet_name = '机框式交换机生测checklist')
        print(self.report_df)
        self.report_name = path + "_%d%02d%02d_%d_%02d_%02d"% (datetime.now().year, datetime.now().month, datetime.now().day,datetime.now().hour,datetime.now().minute,datetime.now().second)+".xlsx"
        #创建xlsxwriter格式Writer文件
        self.report_writer = pd.ExcelWriter(self.report_name, engine='xlsxwriter')
        
        #将dataframe数据写入创建的Writer文件
        self.report_df.to_excel(self.report_writer, sheet_name='机框式交换机生测checklist',index=False)
        workbook  = self.report_writer.book
        worksheet = self.report_writer.sheets['机框式交换机生测checklist']
        wrap_format = workbook.add_format({'text_wrap': True, 'border': 4,"valign":"center","align":"center"})
        bold_format = workbook.add_format({'text_wrap': True, 'border': 1,"valign":"vcenter","align":"center",'bold': True,'fg_color': '#D7E4BC'})
        border_format = workbook.add_format({"border":1,"valign":"vcenter","align":"center",'text_wrap': True})
        test_spe_format = workbook.add_format({'text_wrap': True, 'border': 1,"valign":"center","align":"center",'bg_color':'#C5D9F1'})
        worksheet.set_column('A1:A', 15,bold_format)  #设置第一列"测试项"格式
        worksheet.set_column('B1:B', 60, test_spe_format)#设置第二列“测试判断”格式
        worksheet.set_column('C1:C', 8, bold_format)
        worksheet.set_column('D1:D', 8, border_format)
        worksheet.set_column('E1:E', 8, border_format)
        worksheet.set_row(0,20)
        header_format = workbook.add_format({
                                                'bold': True,
                                                'text_wrap': True,
                                                'valign': 'top',
                                                "align":"center",
                                                'fg_color': '#CAE6F4',
                                                'border': 1})
        fail_format = workbook.add_format({'bold': True,'bg_color':'red','font_color': "black"})
        pass_format = workbook.add_format({'bold': True,'bg_color':'green','font_color': "black"})
        na_format = workbook.add_format({'bold': True,'bg_color':'#D9D9D9','font_color': "black"})
        empty_format = workbook.add_format({'bold': True,'bg_color':'yellow'})
        
        worksheet.conditional_format('C1:C54', {'type':'cell',
                                        'criteria': 'equal to',
                                        'value':'"fail"',
                                        'format':   fail_format})
        worksheet.conditional_format('C1:C54', {'type':'cell',
                                        'criteria': 'equal to',
                                        'value':'"pass"',
                                        'format':   pass_format})
        worksheet.conditional_format('C1:C54', {'type':'cell',
                                        'criteria': 'equal to',
                                        'value':'"na"',
                                        'format':   na_format})
        worksheet.conditional_format('C1:C54', {'type':'cell',
                                        'criteria': 'equal to',
                                        'value':'"不适用"',
                                        'format':   na_format})
        worksheet.conditional_format('C1:C54', {'type':'cell',
                                        'criteria': 'equal to',
                                        'value':'""',
                                        'format':   empty_format})

        # worksheet.autofilter(C1,C54,wrap_format)
        #报告部分
        #合并header单元格
        merge_header_format = workbook.add_format({'text_wrap': True,'border': 1,"valign":"vcenter","align":"center",'bold': True,'bg_color': 'yellow',"font_size":20})
        worksheet.merge_range('G1:J1',"测试报告", merge_header_format)
        worksheet.write("F1","")
        report_cell_format = workbook.add_format({'text_wrap': True,"valign":"vcenter","font_color":"blue",'border': 1})
        # report_cell_format.set_border()
        worksheet.conditional_format("G1:J7",{ 'type' : 'no_blanks','format':report_cell_format})
        # worksheet.set_row(0,18,cell_format)
        # worksheet.set_column('B:B', None, header_format)
        text = 'A simple textbox with some text'
        worksheet.insert_textbox(2, 3, text,{'width': 60,'height': 60})
        imgfile = r"C:\Users\seeker\Desktop\ASCII编码.jpg"
        worksheet.insert_image('D5', imgfile,{'x_scale': 0.1, 'y_scale': 0.1, 'positioning': 3})

        #保存文件
        self.report_writer.save()


        #启动Excel应用
        excel = wc.Dispatch('Excel.Application')
        excel.Visible = True
        #连接excel
        workbook = excel.Workbooks.Open(self.report_name )
        worksheet = workbook.Worksheets('机框式交换机生测checklist')
        #关闭并保存
        # shape = xlSheet.Shapes.AddOLEObject(ClassType='Paint.Picture',Filename="D:\union.jpeg", Link=False)  #插图片附件
        Embedded_object = worksheet.OLEObjects()
        file_loction = r"C:\Users\seeker\Desktop\123.txt"
        # shapeleft = worksheet.Cells(1,3).Left
        # shapetop = worksheet.Cells(1,3).Top
        Embedded_object.Add(ClassType=None, Filename=file_loction, Link=False, DisplayAsIcon=True,
                Left=1, Top=3, Width=50, Height=50)
        # shape.Left = xlSheet.Cells(2,2).Left  #把定位附件到指定单元格 单位:磅
        # shape.Top = xlSheet.Cells(2,2).Top
        workbook.Save() 


# shape.Left = xlSheet.Cells(2,2).Left  #把定位附件到指定单元格 单位:磅
# shape.Top = xlSheet.Cells(2,2).Top
# xlSheet.Rows(2).RowHeight  = shape.Height    #行高
# xlSheet.Columns(2).ColumnWidth = shape.Width  #列宽
# book.SaveAs(filename)

        # workbook.SaveAs('newexcel.xlsx')
        # excel_app.Application.Quit()



test = Xlsx_Write()
test.test()

