import os

if __name__ == "__main__":
    cmd = "ping 192.168.0.1 -n 20"
    shell = os.popen(cmd)#调用os模块进行ping操作
    s = shell.text()
    print(s)