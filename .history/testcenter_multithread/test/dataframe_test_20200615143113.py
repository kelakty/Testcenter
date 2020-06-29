from PyQt5.QtCore import QThread,pyqtSignal,QStandardPaths
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
import pandas as pd
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import xlwt

class Ui_MainWindow(object):
    """
    自动生成的代码, 请不要修改
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 357)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 10, 341, 341))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 10, 81, 31))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.choosefilename)
        d={'A':1,'B':pd.Timestamp('20130301'),'C':range(4),'D':np.arange(4)}
        self.df=pd.DataFrame(d)

    def choosefilename(self):
        self.ExportExcel()
        choosefilename, _ = QFileDialog.getOpenFileName(self, "选取文件",QStandardPaths.standardLocations(0)[0],
                                    "Excel Files (*.xlsx *.xls);;All Files (*)")
        report = pd.read_excel(choosefilename, sheet_name = '机框式交换机生测checklist')
        print(report)
        # print(report.iloc[5,4])
        
        print("df: ", self.df)
        print("df A: ", self.df.A)
        print("df head: ", self.df.head())
        print("df head2: ", self.df.head(2))
        print("df tail: ", self.df.tail(2))
        print("输出行号列表",self.df.index.values)
        print("输出列标题",self.df.columns.values)
        print("输出行号列表",report.index.values)
        print("输出列标题",report.columns.values)
        print("df 12", self.df.iloc[[1,2,3]].values)
        print("df ab", self.df.loc[[1,2],['A','B']].values)
        # print("本次测试结果为：",report[5:])
        # print("C行值",report.loc[:,1])
        

        # report = choosefilename +"_%d%02d%02d_%d_%02d_%02d"% (datetime.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
        # report.to_excel(report,sheet_name='机框式交换机生测checklist',index=False)

    def ExportExcel(self):
        f = xlwt.Workbook() 
        #设置表格样式 
        style = xlwt.easyxf('font: name Arial Black, colour_index black, bold on; align: wrap on, vert centre, horiz center;border:left thin, right thin, top thin, bottom thin') 
        #创建sheet1 
        sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) 
        # 创建复杂表头 
        #write_merge(x, x + m, y, y + n, string, sytle) x表示行，y表示列，m表示跨行个数，n表示跨列个数，
        # string表示要写入的单元格内容，style表示单元格样式。 
        # 其中，x, y, m, n，都是以0开始计算的。 
        sheet1.write_merge(0,1,0,0,u'商圈', style) 
        sheet1.write_merge(0,1,1,1,u'销售流水', style) 
        sheet1.write_merge(0,1,2,2,u'流水占比', style) 
        sheet1.write_merge(0,1,3,3,u'流水差距', style) 
        sheet1.write_merge(0,0,4,6,u'流水份额', style) 
        sheet1.write_merge(1,1,4,4,u'饿了么', style) 
        sheet1.write_merge(1,1,5,5,u'美团', style) 
        sheet1.write_merge(1,1,6,6,u'大众点评', style) 
        sheet1.write_merge(0,1,7,7,u'全网门店数', style) 
        sheet1.write_merge(0,0,8,10,u'门店覆盖率', style) 
        sheet1.write_merge(1,1,8,8,u'饿了么', style) 
        sheet1.write_merge(1,1,9,9,u'美团', style) 
        sheet1.write_merge(1,1,10,10,u'大众点评', style) 
        print( '#############') 
        f.save('D:\demo.xls')



if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    testCenter = MainWindow()
    testCenter.show()
    sys.exit(app.exec_())