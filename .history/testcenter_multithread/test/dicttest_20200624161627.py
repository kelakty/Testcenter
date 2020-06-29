import threading
from datetime import datetime
import re

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
# consoledict = {"Name":"COM1", "consoleobj":"obj", "subwindow":"obj", "consolethread":123 }
# consoledict1 = {"Name":"COM2", "consoleobj":"obj", "subwindow":"obj", "consolethread":153 }
# consoledict2 = {"Name":"COM3", "consoleobj":"obj", "subwindow":"obj", "consolethread":143 }
# console = []
# console.append(consoledict)
# console.append(consoledict1)
# console.append(consoledict2)

# print("consoledict:",consoledict)
# print("console:",console)


# def find_dictionarylist_keyvalue_index(dictionarylist, keyname, keyvalue):
#     """
#     从字典列表中查找 是否存在 某一个key 且对应的值正确 则返回字典所在列表的索引，否则返回False
#     找到匹配的键值对 立马返回不再向下查找
#     Args：
#         dictionarylist: 一个字典列表
#         keyname: 字典中的key名字
#         keyvalue:字典中key名字对应的value值
#     Return：
#         index: 找到的键值对字典 所在列表的索引值
#         False ： 没找到
#     """
#     for index in range(len(dictionarylist)):
#         for key in dictionarylist[index]:
#             print("%s--%s" % (key,dictionarylist[index][key]))
#             if key == keyname:
#                 if dictionarylist[index][key] == keyvalue:
#                     return index
#     return False



# def find_dictionary_keyvalue(dictionary, keyname, keyvalue):
#     """
#     查找字典中是否存在 某一个key 且对应的值正确 则返回True，否则返回False
#     Args：
#         dictionary: 一个字典
#         keyname: 字典中的key名字
#         keyvalue:字典中key名字对应的value值
#     Return：
#         True/False ： 找到/没找到
#     """
#     # print(list(dictionary.keys()).index(keyname))
#     try:
#         if list(dictionary.values())[list(dictionary.keys()).index(keyname)] == keyvalue:
#             return True
#         else: return False
#     except Exception :
#         return False

# # print('查找到的字典列表',console[find_dictionarylist_keyvalue_index(console,"Name","COM1")])
# # print('查找到的字典',find_dictionary_keyvalue(consoledict,"Name","COM1"))



# # try:
# #     print("字典值列表",list(consoledict.values()).index("COM1"))  #如果错误则ValueError: 'COM' is not in list
# # except ValueError:
# #     print("can not find member index")

# # # a= (0 for i in console if list(i.values()).index("COM1") )
# # # print(list(a))
# # # b=[1,2,3]
# # # a= (i for i in b if i>1)
# # # print(list(a))

# # for i in console:
# #     print(i)
# #     print(i.values())
# #     print(list(i.values()).index("COM1"))
# #     print(list(i.values()).count("COM1"))
# #     if list(i.values()).count("COM1") >= 1:
# #         print("找到")

# print("dictionary is :",consoledict["Name"])
# console.remove(console[0])
# print("delete",console)

# # console[0].remove()
# # print("delete",console)
# a = -1
# if a < 0:
#     print("找到")

# waiting_to_send={}
# waiting_to_send.update({str(threading.current_thread().ident) : {"senddata":[123], "residue":""}})

# print(waiting_to_send)
# print(waiting_to_send[str(threading.current_thread().ident)]["senddata"])

# quickcommand_list = []
# print(quickcommand_list[len(quickcommand_list)-1])


# command = 'sh ver\\r\\n'
# print(command.replace("\\r\\n", "\r\n"))   #会报错，原因未知. SyntaxError: EOL while scanning string literal

# command = 0
# command2 = False
# print(int(command) == True)
# print(int(command2) == False)

# with open("fac_auto_test.txt","a+") as file:
#     data = file.read()
# print(data)

# command_name = "RTC时间"
# send_info = {"0. 设置RTC时间":"2020 12 31 23:59:59","abc":123}
# # needed_send_command_menu = list(send_info.keys())[list(send_info.keys()).index(command_name)] #不存在会出错
# # needed_send_command = send_info[needed_send_command_menu]
# # print(needed_send_command)
# # print(needed_send_command)

# send_info_key_list = list(send_info.keys())
# for i in range(len(send_info_key_list)):
#     if re.findall(command_name,send_info_key_list[i]) != []: 
#         print(send_info[list(send_info.keys())[i]])
#         # return list(send_info.keys())[i]

# from datetime import datetime 
# fac_auto_test_log = open("fac_auto_test.txt","a+")

# #保存失败的log数据
# print("开始保存失败log信息...")
# fac_auto_test_log.write(str(datetime.now())+":\r\n")
# fac_auto_test_log.write("2365df6")

# a= ["123","456"]
# b = ["123","456"]
# print(a==b)


# import queue
# stacknode = queue.LifoQueue()
# stacknode.put("1")
# stacknode.put("2")
# print(stacknode.qsize())

import re
def matchlog(need_match_text, log_data_buffer):
    #匹配log
    # print("log缓存区：", log_data_buffer)
    matchdatalist = []
    matchdatalist = re.findall(need_match_text, log_data_buffer)
    if matchdatalist != []:
        return matchdatalist
    else:
        return False

def search_test_item(log_data):
    #找当前菜单下有多少个测试项
    #找到则返回序数列表，否则返回false
    need_match_text = "    (\w). "
    need_match_name = "    (\w. .*)\r\n"
    match_num_list = matchlog(need_match_text, log_data)
    match_name_list = matchlog(need_match_name, log_data)
    if match_num_list != False:
        return match_num_list, match_name_list
    else: return False,False

log_data_buffer = "1"
if log_data_buffer != "":
    # print(search_test_item(log_data_buffer))
    commandlist, test_name_list = search_test_item(log_data_buffer)

    if commandlist != [] and test_name_list != [] and len(commandlist)==len(test_name_list):
        print("pass")
