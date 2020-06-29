import xlsxwriter
import pandas as pd
from datetime import datetime
# from xlsxpandasformatter import FormatedWorksheet
import seaborn

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
        wrap_format = workbook.add_format({'text_wrap': True})

        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 60)
        worksheet.set_column('B:B', None, wrap_format)
        header_format = workbook.add_format({
                                                'bold': True,
                                                'text_wrap': True,
                                                'valign': 'top',
                                                'fg_color': '#D7E4BC',
                                                'border': 1})
        # worksheet.set_column('B:B', None, header_format)

        #保存文件
        self.report_writer.save()
test = Xlsx_Write()
test.test()

