
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow,QAction
from PyQt5.QtGui import QIcon
from ui_mainwindow import Ui_MainWindow
import qdarkstyle

class MyUi_MainWindow(object):
    def setupUi2(self, MainWindow):
        self.mainWindow=MainWindow
#        self.treeWidget.topLevelItem(0).child(0).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(1).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(2).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(3).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(4).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(5).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(6).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(7).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(8).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(9).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(10).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(11).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(12).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(13).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(14).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(14).child(0).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(14).child(1).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(14).child(2).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(14).child(3).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(15).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(16).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(17).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(18).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(19).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(20).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(21).setCheckState(0, Qt.Unchecked)
#        self.treeWidget.topLevelItem(0).child(22).setCheckState(0, Qt.Unchecked)
        
#        self.dockWidget.setAllowedAreas(QtCore.Qt.RightDockWidgetArea | QtCore.Qt.LeftDockWidgetArea)#设置dockWidget只停靠在左边栏
        
        #self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea or QtCore.Qt.RightDockWidgetArea)设置dockWidget只停靠在左边栏
        #self.dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)#设置不可移动关闭等
        #self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetMovable)#设置QDockWidget只可移动
        
        #print(QMainWindow.dockWidgetArea(Ui_MainWindow.dockWidget))
        #print(Qt.DockWidgetAreas)
        
        #增加一个protocalSetting
        # self.page_3 = QtWidgets.QWidget()
        # self.page_3.setGeometry(QtCore.QRect(0, 0, 160, 519))
        # self.page_3.setObjectName("page_3")
        # self.protocalSetting.addTab(self.page_3, "")

        #self.page_2.setStyleSheet("color: rgb(0, 255, 0)")  #设置protocalSetting中的page_2内的文字颜色。直接指向对象名使用
        #self.protocalSetting.setStyleSheet("self.protocalSetting.page_3{border: none; background: rgb(68, 69, 73); color: rgb(0, 160, 230);}")
        #self.send_button.setStyleSheet:hover("color: rgb(0, 255, 0)")
        
        #使用.qss文件的方式进行qss
        #with open('D:/testcenter20190102备份/testcenter/testcenter_pyqt5/QSS.qss', 'r') as f:   #导入qss样式
        #    self.send_button_style = f.read()
        #self.send_button.setStyleSheet(self.send_button_style)
        
        send_button_style='''QPushButton#send_button:hover { background: green;border-radius: 5px;}'''
        self.send_button.setStyleSheet(send_button_style)
        
        self.splitter.setStretchFactor(0, 8)
        self.splitter.setStretchFactor(1, 2)
        # MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar_quickcommand)
        #使用现成的黑色样式
        #self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        # # 为本窗口添加一个toolbar的状态
        #添加一个快速命令工具栏
        # self.toolBar_quickcommand = QtWidgets.QToolBar(MainWindow)
        # self.toolBar_quickcommand.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        # self.toolBar_quickcommand.setObjectName("toolBar_quickcommand")
        # MainWindow.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar_quickcommand) #TopToolBarArea

        # toolBar = self.mainWindow.addToolBar("TestToolBar")
        # # 添加打开tool 在pyqt5里面是一个action
        # newTestCommand  = QAction(QIcon("./images/AddTest.jpg"), "添加测试命令", self)
        # toolBar.addAction(newTestCommand)
        # # 添加第二个action  参数分别是 图片， 名字(可以理解给这个action起个名字)，上下文
        # delayTime = QAction(QIcon("./images/Delay.jpg"), "设置延时", self)
        # toolBar.addAction(delayTime)

        # logRecognition = QAction(QIcon("./images/ScanText.jpg"), "设置log识别内容", self)
        # toolBar.addAction(logRecognition)
        # specialTest = QAction(QIcon("./images/SpecialTest.png"), "添加特殊测试", self)
        # toolBar.addAction(specialTest)
        # expertScan = QAction(QIcon("./images/ExpertScan.jpg"), "高级log识别", self)
        # toolBar.addAction(expertScan)
        # deleteTest = QAction(QIcon("./images/delete.png"), "删除选中测试", self)
        # toolBar.addAction(deleteTest)
        # # action一般是用这个作为绑定的点击事件 注意方括号里面的QAction
        # toolBar.actionTriggered[QAction].connect(self.toolbtnpressed)
        # #self.setLayout(layout)


        #####调整右侧sequencer的dockwidget控件内嵌tree widget
        # self.dockWidgetContents_3 = QtWidgets.QWidget()
        # # self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        # self.treeWidget_sequencer = QtWidgets.QTreeWidget()  #self.dockWidgetContents_3
        # self.treeWidget_sequencer.setGeometry(QtCore.QRect(0, 0, 291, 431))
        # self.treeWidget_sequencer.setObjectName("treeWidget_sequencer")
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_sequencer)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_sequencer)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_sequencer)
        # item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget_sequencer)
        # self.Sequencer.setWidget(self.treeWidget_sequencer) #self.dockWidgetContents_3
        #####调整右侧sequencer的dockwidget控件内嵌tree widget###结束#######

        #设置sequencer dockwidget中的treewidget控件的边缘间隙为0#######
        # self.verticalLayout.setContentsMargins(0,0,0,0)
        


        self.retranslateUi2(MainWindow)
        
    # def toolbtnpressed(self, a):
    #     print("pressed tool button is ", a.text())
        


    def retranslateUi2(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        #self.protocalSetting.setTabText(self.protocalSetting.indexOf(self.page_3), _translate("MainWindow", "SIT测试"))
        self.toolBar_quickcommand.setWindowTitle(_translate("MainWindow", "快速命令工具栏"))  #设置快速命令工具栏显示名字
        # #######添加treewidget 控件中的信息
        # self.treeWidget_sequencer.headerItem().setText(0, _translate("MainWindow", "命令"))
        # self.treeWidget_sequencer.headerItem().setText(1, _translate("MainWindow", "说明"))
        # self.treeWidget_sequencer.headerItem().setText(2, _translate("MainWindow", "备注"))
        # __sortingEnabled = self.treeWidget_sequencer.isSortingEnabled()
        # self.treeWidget_sequencer.setSortingEnabled(False)
        # self.treeWidget_sequencer.topLevelItem(0).setText(0, _translate("MainWindow", "sh ver "))
        # self.treeWidget_sequencer.topLevelItem(0).setText(1, _translate("MainWindow", "show信息"))
        # self.treeWidget_sequencer.topLevelItem(0).setText(2, _translate("MainWindow", "客户端 dut1主"))
        # self.treeWidget_sequencer.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "scan"))
        # self.treeWidget_sequencer.topLevelItem(0).child(0).setText(1, _translate("MainWindow", "识别对应信息是否正确"))
        # self.treeWidget_sequencer.topLevelItem(1).setText(0, _translate("MainWindow", "sh pow "))
        # self.treeWidget_sequencer.topLevelItem(1).setText(1, _translate("MainWindow", "show电源信息"))
        # self.treeWidget_sequencer.topLevelItem(1).setText(2, _translate("MainWindow", "客户端 duit1 从"))
        # self.treeWidget_sequencer.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "scan"))
        # self.treeWidget_sequencer.topLevelItem(1).child(0).setText(1, _translate("MainWindow", "识别对应信息是否正确"))
        # self.treeWidget_sequencer.topLevelItem(2).setText(0, _translate("MainWindow", "XXX"))
        # self.treeWidget_sequencer.topLevelItem(2).setText(1, _translate("MainWindow", "发包机打流"))
        # self.treeWidget_sequencer.topLevelItem(2).setText(2, _translate("MainWindow", "客户端 发包机"))
        # self.treeWidget_sequencer.topLevelItem(3).setText(0, _translate("MainWindow", "XXX"))
        # self.treeWidget_sequencer.topLevelItem(3).setText(1, _translate("MainWindow", "自动上下电"))
        # self.treeWidget_sequencer.topLevelItem(3).setText(2, _translate("MainWindow", "客户端 串口自动上下电工具"))
        # self.treeWidget_sequencer.setSortingEnabled(__sortingEnabled)
        # #######添加treewidget 控件中的信息#####结束###########
    
        
        
