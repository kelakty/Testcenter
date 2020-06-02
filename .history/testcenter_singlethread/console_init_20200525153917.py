
from Console import Console

class ConsoleInit(Console):
    """
    用于在新建console前进行窗口等的初始化新建MDIarea的sub窗口操作
    """
    def __init__(self, parent=None):
        
        super(self).__init__(parent)
        
    def checkconsoleexist():
        """
        应该去检查openedconsole字典是否存在

        串口：检查是否在GlobalVariable.opencomlist中
        Telnet：检查
        """
        pass

    def new_
