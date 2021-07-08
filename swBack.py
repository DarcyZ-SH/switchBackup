import sys
import os
import telnetlib
import time
import threading
import datetime
now = datetime.datetime.now()
#Use for loop to telnet into each routers and execute commands
class Bakconf(threading.Thread):
    def __init__(self,host):
        threading.Thread.__init__(self)
        s=host.split()
        self.host=s[0]
        self.USERNAME=s[1]
        self.PASSWORD=s[2]
    def run(self):
        print('host:'+self.host+' user:'+self.USERNAME+' password:'+self.PASSWORD)
        try:
            
            tn = telnetlib.Telnet(self.host,port=23,timeout=5)
            tn.set_debuglevel(5)
            tn.read_until(b"Username:", timeout=2)
            tn.write(bytes(self.USERNAME,"utf8") +b"\n")
            tn.read_until(b"Password:", timeout=2)
            tn.write(bytes(self.PASSWORD,'utf8') +b"\n")
            tn.write(b"\n")
            time.sleep(2)
            tn.write(b"system-view"+b"\n")
            tn.write(b"user-interface vty 0 4"+b"\n")
            tn.write(b"screen-length 0"+b"\n")    #设置华为交换机命令不分布显示 cisco用terminal length 0
            tn.write(b"quit"+b"\n")
            tn.write(b"quit"+b"\n")
            #######executive command in the txt file########
            for COMMANDS in open(sys.path[0]+r'/command.txt').readlines():
                COMMAND = COMMANDS.strip('\n')
                tn.write(b"\n"+ bytes(COMMAND,'utf8'))
            #######executive command in the txt file########
            time.sleep(10)   #设置延时，使下面命令有足够时间获取返回值，调整到适当时长
            output = tn.read_very_eager()      #获取返回值
            tn.write(b"quit"+b"\n")
            filename = sys.path[0]+"/log/%s_%i-%.2i-%.2i_%.2i:%.2i:%.2i.log" % (self.host,now.year,now.month,now.day,now.hour,now.minute,now.second)    #格式化文件名
            time.sleep(10)
            fp = open(filename,"w")
            fp.write(bytes.decode(output))
            fp.close()
            
        except Exception as e:
            print ("Can't connection %s" %self.host)
            return

def main():
    for host in open(sys.path[0]+r'/swList.txt').readlines():
        dsthost = host.strip('\n')
        print(dsthost)
        bakconf=Bakconf(dsthost)
        bakconf.start()
if __name__=="__main__":
    main()