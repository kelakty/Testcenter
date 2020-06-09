from PyQt5.QtCore import QObject

class Console(QObject):
    """
    Console控制终端类，类中包含共用的保存log，收发，脚本执行，测试向导，工具--vlan配置，编辑--复制黏贴

    """
    def __init__(self, parent=None):
        """
        初始化，检查需要打开的控制端是否已经打开，没有打开则初始化
        """
        pass

    def checkconsoleexist(self):
        """
        应该去检查openedconsole字典是否存在

        串口：检查是否在GlobalVariable.opencomlist中
        Telnet：检查
        """
        pass

    def savelog(self):
        pass

    def runscript(self):
        pass

    def testnavigation(self):
        pass

    def testtools(self):
        pass

    def consoleedit(self):
        pass

    def setencoding(self):
        pass

    def quickcommand(self):   #也可以作为独立类，从console继承
        pass


