import pandas as pd
from PyQt5.QtCore import QObject
from PyQt5.QtCore import QThread,pyqtSignal,QStandardPaths
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
from globalvariable import GlobalVariable
import threading
import time
import re
import pandas as pd


d={'A':1,'B':pd.Timestamp('20130301'),'C':range(4),'D':np.arange(4)}
df=pd.DataFrame(d)
choosefilename, _ = QFileDialog.getOpenFileName(self, "选取文件",QStandardPaths.standardLocations(0)[0],
                            "Excel Files (*.xlsx *.xls);;All Files (*)")
self.report = pd.read_excel(choosefilename, sheet_name = '机框式交换机生测checklist')
print(self.report)
print("C行值",self.report.loc[:, "C" ])
print("本次测试结果为：",self.report[5:"D"])
self.report = choosefilename +"_%d%02d%02d_%d_%02d_%02d"% (date.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
self.report.to_excel(self.report,sheet_name='机框式交换机生测checklist',index=False)

