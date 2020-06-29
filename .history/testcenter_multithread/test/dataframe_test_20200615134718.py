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
        choosefilename, _ = QFileDialog.getOpenFileName(self, "选取文件",QStandardPaths.standardLocations(0)[0],
                                    "Excel Files (*.xlsx *.xls);;All Files (*)")
        report = pd.read_excel(choosefilename, sheet_name = '机框式交换机生测checklist')
        print(report)
        print(report.iloc[5,4])

        print("df: ", self.df)
        print("df A: ", self.df.A)
        print("df head: ", self.df.head())
        print("df head2: ", self.df.head(2))
        print("df tail: ", self.df.tail(2))
        print("df 12", self.df.iloc[[1,2,3]].values)
        print("df ab", df.loc[[1,2],['A','B']].values)
        # print("本次测试结果为：",report[5:])
        # print("C行值",report.loc[:,1])
        

        # report = choosefilename +"_%d%02d%02d_%d_%02d_%02d"% (datetime.year, date.month, date.day,time.hour,time.minute,time.second)+".xlsx"
        # report.to_excel(report,sheet_name='机框式交换机生测checklist',index=False)


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    testCenter = MainWindow()
    testCenter.show()
    sys.exit(app.exec_())