


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
consoledict1 = {"Name":"COM2", "consoleobj":"obj", "subwindow":"obj", "consolethread":153 }
consoledict2 = {"Name":"COM3", "consoleobj":"obj", "subwindow":"obj", "consolethread":143 }
console = []
console.append(consoledict)
console.append(consoledict1)
console.append(consoledict2)

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



def find_dictionary_keyvalue(dictionary, keyname, keyvalue):
    """
    查找字典中是否存在 某一个key 且对应的值正确 则返回True，否则返回False
    Args：
        dictionary: 一个字典
        keyname: 字典中的key名字
        keyvalue:字典中key名字对应的value值
    Return：
        True/False ： 找到/没找到
    """
    # print(list(dictionary.keys()).index(keyname))
    try:
        if list(dictionary.values())[list(dictionary.keys()).index(keyname)] == keyvalue:
            return True
        else: return False
    except Exception :
        return False

# print('查找到的字典列表',console[find_dictionarylist_keyvalue_index(console,"Name","COM1")])
# print('查找到的字典',find_dictionary_keyvalue(consoledict,"Name","COM1"))



a= (0 for i in console if list(i.values()).index("COM1"))
print(list(a))
# b=[1,2,3]
# a= (0 for i in b if i>1)
# print(list(a))