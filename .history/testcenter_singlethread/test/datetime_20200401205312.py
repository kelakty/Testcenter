# import logging
# from logging import handlers
# from datetime import datetime

# logger= logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# # handler= logging.FileHandler("log.txt")

# handler= logging.handlers.TimedRotatingFileHandler('.\\log\\all.log',when='midnight',interval=1,backupCount=30)
# handler.setLevel(logging.DEBUG)
# handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s ： %(message)s'))

# error_handler=logging.FileHandler('.\\log\\error.log')
# error_handler.setLevel(logging.ERROR)
# error_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s - %(filename)s[:%(lineno)d] - %(message)s'))

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s ： %(message)s'))

# logger.addHandler(handler)
# logger.addHandler(error_handler)
# logger.addHandler(console)



# logger.debug("this is a debug log")
# logger.info("this is a info log")
# logger.warning("this is a warning log")
# logger.error("this is a error log")
# logger.critical("this is a critical log")
# logger.info("this is a info log")


import socket
import time
import re

def service_client(new_socket,request):
    # 1.接收浏览器发送过来的请求，即http请求
    #request=new_socket.recv(1024).decode("utf-8")

    request_lines= request.splitlines()
    file_name=""
    ret=re.match(r"[^/]+(/[^ ]*)", request_lines[0])
    if ret:
        file_name = ret.group(1)
        if file_name == "/":
            file_name = "/index.html"
    # 2.返回http格式的数据，给浏览器
    try:
        f=open("./html" + file_name, "rb")
    except:
        response = "HTTP/1.1 404 NOT FOUND\r\n"
        response += "\r\n"
        response += "---file not found"
        new_socket.send(response.encode("utf-8"))
    else:
        html_content = f.read()
        f.close()
        response_body = html_content

        # 2 准备发送给浏览器的数据   header
        response_header = "HTTP/1.1 200 OK\r\n"
        response_header +="Content-Length:%d\r\n" % len(response_body)
        response_header +="\r\n"

        response = response_header.encode("utf-8") + response_body
        new_socket.send(response)

    #关闭套接字
    # new_socket.close()
    
def main():
    # 1.创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server_socket.setblocking(socket.SOL_SOCKET , socket.SO_REUSEADDR,1)
    # 2.绑定
    tcp_server_socket.bind(("",7890))
    # 3.变为监听套接字
    tcp_server_socket.listen(128)
    tcp_server_socket.setblocking(False)
    
    client_socket_list=list()
    while True:
        # 4.等待新客户端的链接
        try:
            new_socket, client_addr = tcp_server_socket.accept()
        except Exception as ret:
            print("没有新的客户端到来")
        else:
            print("只要没有异常，意味着来了一个新的客户端")
            new_socket.setblocking(False)
            client_socket_list.append(new_socket)
        for client_socket in client_socket_list:
            try:
                recv_data=client_socket.recv(1024)
            except Exception as ret:
                print(ret)
                print("这个客户端没有发送过来数据")
            else:
                if recv_data:
                    #print("客户端发送过来了数据")
                    service_client(client_socket ,recv_data)
                else:
                    client_socket.close()
                    client_socket_list.remove(client_socket)
    # 关闭监听套接字
    tcp_server_socket.close()

