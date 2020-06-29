from PyQt5.QtCore import QThread,pyqtSignal,QStandardPaths
from PyQt5.QtWidgets import QWidget,QFileDialog,QMessageBox
import pandas as pd
import numpy as np
from datetime import datetime

d={'A':1,'B':pd.Timestamp('20130301'),'C':range(4),'D':np.arange(4)}
df=pd.DataFrame(d)

choosefilename, _ = QFileDialog.getOpenFileName("选取文件",QStandardPaths.standardLocations(0)[0],
                            "Excel Files (*.xlsx *.xls);;All Files (*)")
report = pd.read_excel(choosefilename, sheet_name = '机框式交换机生测checklist')
print(report)
print("C行值",report.loc[:, "C" ])
print("本次测试结果为：",report[5:"D"])

report = choosefilename +"_%d%02d%02d_%d_%02d_%02d"% (datetime.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
report.to_excel(report,sheet_name='机框式交换机生测checklist',index=False)

