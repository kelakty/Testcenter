


def gendictdata(columnname,cellitem):
        """
        使用两个列表，生成一一对应的字典
        columnname : 列名称的list
        cellitem ： 列值的list
        return一个列名称与列值一一对应的字典
        如果列表不一样大，则返回空
        """
        dictdata={}
        if len(columnname) != len(cellitem):
            return
        for i in range(len(columnname)):
            dictdata.update(dict(columnname[i]=cellitem[i]))
        return dictdata

columnname=["ID","address","L"]
cellitem=[123,0x88,134]

data= gendictdata(columnname,cellitem)
print(data)

