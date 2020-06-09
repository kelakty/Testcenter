


# def gendictdata(columnname,cellitem):
#     """
#     使用两个列表，生成一一对应的字典
#     columnname : 列名称的list
#     cellitem ： 列值的list
#     return一个列名称与列值一一对应的字典
#     如果列表不一样大，则返回空
#     """
#     dictdata={}
#     if len(columnname) != len(cellitem):
#         return
#     for i in range(len(columnname)):
#         dictdata.update(dict({columnname[i]:cellitem[i]}))
#     return dictdata

# columnname=["ID","address","L"]
# cellitem=[123,0x88,134]

# data= gendictdata(columnname,cellitem)
# # data=dict({columnname[0]:cellitem[0]})
# print(data)
consoledict = {"Name":"COM1", "consoleobj":"obj", "subwindow":"obj", "consolethread":123 }
console = []
console.append(consoledict)

print("consoledict:",consoledict)
print("console:",console)


def find_dictionarylist_keyvalue_index(dictionarylist, keyname, keyvalue):
    """
    从字典列表中查找 是否存在 某一个key 且对应的值正确 则返回字典所在列表的索引，否则返回False
    找到匹配的键值对 立马返回不再向下查找
    Args：
        dictionarylist: 一个字典列表
        keyname: 字典中的key名字
        keyvalue:字典中key名字对应的value值
    Return：
        index: 找到的键值对字典 所在列表的索引值
        False ： 没找到
    """
    for index in range(len(dictionarylist)):
        for key in dictionarylist[index]:
            print("%s--%s" % (key,dictionarylist[index][key]))
            if key == keyname:
                if dictionarylist[index][key] == keyvalue:
                    return index
    return False

print('查找到的字典列表',console[find_dictionarylist_keyvalue(console,"Name","COM1")])

def find_dictionary_keyvalue():
    """
    查找字典中是否存在 某一个key 且对应的值正确 则返回True

    """
