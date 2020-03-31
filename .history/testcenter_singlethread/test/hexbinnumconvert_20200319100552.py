"""
df['实际读出值']=reg_data
print("原始寄存器值：",reg_data[0])
print("原始寄存器值：",type(reg_data[0]))
##print("binascii转换：",binascii.a2b_base64(reg_data[0]))

str_to_hex=reg_data[0].replace('0x', '')
print("原始寄存器值：",str_to_hex)
##str_to_hex=str(int(hex(str_to_hex).upper(), 16))
for c in str_to_hex:
    print(c)
    print('{:4s}'.format(bin(int(c))))

##str_to_hex=''.join([bin(int(c)).replace('0x', '') for c in str_to_hex])
##print("str_to_hex:",str_to_hex)
##print(type(str_to_hex))

##str_to_bin=' '.join([bin(ord(c)).replace('0b', '') for c in reg_data[0]])
##print("str_to_bin:",str_to_bin)
"""

"""
str1="hw_test.bin i2c_rd 12 0x58 "
str2=0x81
str3=" 0 12"
for i in range(10):
    addr = '0x%02X' % str2
    str2+=1
    str4=str1+addr+str3
    print(str4)
"""


# def print_bytes_hex(data):
#     lin = ['%02X' % i for i in data]
#     print(" ".join(lin))

# # 测试字节列表，这也是网络传输收到的原始类型
# arr = [0x4B, 0x43, 0x09, 0xA1, 0x01, 0x02, 0xAB, 0x4A, 0x43]
# print_bytes_hex(arr)

"""
counter=1

console_terminal_threadpool=["abc"]
# if console_terminal_threadpool == []:
#     console_terminal_threadpool.append(None)
#     print(console_terminal_threadpool)
#     print("is none")
# else:
try:
    if console_terminal_threadpool[counter] != None:
        print("%s,is not none" % console_terminal_threadpool[counter])
        counter+=1
except Exception:
    console_terminal_threadpool.append(None)
    print("%s,is none" % console_terminal_threadpool)
console_terminal_threadpool[counter]="345"
print("%s" % console_terminal_threadpool)
print("end")
"""
a=1
b=2
if tryopencom() == True:
    print("pass")
else:
    print("false")

def tryopencom(self):
    if a>b:
        return False
    else:
        return True