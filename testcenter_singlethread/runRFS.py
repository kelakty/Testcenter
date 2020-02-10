import subprocess
import os

def runCmd(cmd) :
        res = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        sout ,serr = res.communicate() #该方法和子进程交互，返回一个包含 输出和错误的元组，如果对应参数没有设置的，则无法返回
        return res.returncode, sout, serr, res.pid #可获得返回码、输出、错误、进程号；
res = runCmd('dir')
print res[0], res[1], res[2], res[3]  #从元组中获得对应数据