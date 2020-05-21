#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author Rongzhong Xu 2016-08-25 wechat: pythontesting
"""
Name: telnet_demo.py

Tesed in python3.5
"""
from telnetlib import Telnet
import telnetlib
import sys
HOST = "192.168.193.23"
PORT = 23
#user = "seeker"
#password = "qwer1234"

"""
def command(con, str_=""):
    data = con.read_very_eager()
    print(data.decode(errors='ignore'))
    con.write(str_.encode() + b"\r\n")
    return data

tn = Telnet(HOST,PORT)
#tn.open(HOST,1000)
#command(tn, "login: ", user)
#if password:
#    command(tn, "Password: ", password)
# command(tn, "ls")
# command(tn, " exit")
# command(tn, "")
print("连接成功")
tn.write(b'\r\n')
tn.write(b'\r\r\n')
tn.write(b'sh ver\r\n')
print(tn.read_all())

# if 1:
#     getstring()
    
tn.close()
"""

# with Telnet('192.168.193.106', 23) as tn:
#     tn.interact()  
if sys.platform == "win32":
    print("这是一个win32平台")

with Telnet('192.168.193.106', 2002) as tn:
    tn.mt_interact()  


    # def interact(self):
    #     """Interaction function, emulates a very dumb telnet client."""
    #     if sys.platform == "win32":
    #         self.mt_interact()
    #         return
    #     with _TelnetSelector() as selector:
    #         selector.register(self, selectors.EVENT_READ)
    #         selector.register(sys.stdin, selectors.EVENT_READ)

    #         while True:
    #             for key, events in selector.select():
    #                 if key.fileobj is self:
    #                     try:
    #                         text = self.read_eager()
    #                     except EOFError:
    #                         print('*** Connection closed by remote host ***')
    #                         return
    #                     if text:
    #                         sys.stdout.write(text.decode('ascii'))
    #                         sys.stdout.flush()
    #                 elif key.fileobj is sys.stdin:
    #                     line = sys.stdin.readline().encode('ascii')
    #                     if not line:
    #                         return
    #                     self.write(line)


    #     while 1:
    #         line = sys.stdin.readline()
    #         if not line:
    #             break
    #         line=line+"\r\n"   #添加一行回车 适配八爪鱼 
    #         self.write(line.encode('ascii'))
