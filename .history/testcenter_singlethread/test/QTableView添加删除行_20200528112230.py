#QTableView组件的使用
from PyQt5.QtWidgets import  QAbstractItemView,QAction, QMenuBar,QTableView, QHeaderView, QFormLayout, QTableWidget,     QVBoxLayout,QWidget,QApplication ,QHBoxLayout, QPushButton,QMainWindow,QGridLayout,QLabel
import sys
from PyQt5.QtCore import  *
from PyQt5.QtGui import  QStandardItemModel,QStandardItem

class WindowClass(QMainWindow):
    #如果集成QMainWindow 则self.setLayout(self.layout) 替换成
    """
        widget=QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
    """
    #即可， 注意集成QWidget和集成QMainWindow时候区别

    def __init__(self,parent=None):
        super(WindowClass, self).__init__(parent)
        self.layout=QVBoxLayout()
        self.model=QStandardItemModel(4,4)#存储任意结构数据
        self.model.setHorizontalHeaderLabels(['序号','姓名','年龄','地址'])
        for row in range(4):
            for column in range(4):
                i=QStandardItem("  row %s,column %s"%(row,column))
                self.model.setItem(row,column,i)
        self.tableWidget=QTableWidget()
        # self.tableWidget.setModel(self.model)   #Table widgets provide standard table display facilities for applications. 
                                                #The items in a QTableWidget are provided by QTableWidgetItem.
                                                #If you want a table that uses your own data model you should use QTableView rather than this class.
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(4)
        self.header = QStringList()
        self.header"学号"  #<<"姓名"<<"性别"
        self.tableWidget.setHorizontalHeaderLabels(header)
        
        self.layout.addWidget(self.tableWidget)

        #继承QMainWidow使用下面三行代码
        widget=QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        #继承QWidget则使用下面这样代码
        #self.setLayout(self.layout)

        #设置表格充满这个布局QHeaderView
        #self.tableView.horizontalHeader().setStretchLastSection(True)#最后一列决定充满剩下的界面
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#所有列自动拉伸，充满界面

        #添加menu菜单栏,注意：QMainWindow 才可以有菜单栏，QWidget没有，因此上面只能采用继承QMainWIndow
        tool = self.addToolBar("File") #这里尝试使用QmenuBar，则此时会卡死，无法完成下面appedRow操作（猜测：可能是因为本身不允许menuBar完成这种操作）
        self.action= QAction("添加", self)
        self.action2=QAction("删除",self)
        tool.addAction(self.action)
        tool.addAction(self.action2)
        tool.actionTriggered[QAction].connect(self.processtrigger)

        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)#设置只能选中一行
        self.tableWidget.setEditTriggers(QTableView.NoEditTriggers)#不可编辑
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows);#设置只有行选中

    def processtrigger(self,action):
        if action.text()=="添加":
            self.model.appendRow([
                QStandardItem('row %s,column %s' % (11, 11)),
                QStandardItem('row %s,column %s' % (11, 11)),
                QStandardItem('row %s,column %s' % (11, 11)),
                QStandardItem('row %s,column %s' % (11, 11)),
            ])
            self.model.appendColumn([])
        if action.text()=="删除":

            r= self.tableWidget.selectionModel().selectedRows()#获取被选中行
            print(r)#被选中行的列表，每个元素是ModelIndex对象
            #indexs = self.tableView.selectionModel().selection().indexes()#返回结果是QModelIndex类对象，里面有row和column方法获取行列索引
            #print(indexs[0].row())
            if r:
                #下面删除时，选中多行中的最后一行，会被删掉；不选中，则默认第一行删掉
                index=self.tableWidget.currentIndex()
                print(index.row())
                self.model.removeRow(index.row())


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    sys.exit(app.exec_())
    