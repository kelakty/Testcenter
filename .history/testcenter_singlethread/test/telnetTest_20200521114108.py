#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author Rongzhong Xu 2016-08-25 wechat: pythontesting
"""
Name: telnet_demo.py

Tesed in python3.5
"""
from telnetlib import Telnet
import telnetlib

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

with Telnet('192.168.193.106', 2002) as tn:
    tn.mt_interact()  

