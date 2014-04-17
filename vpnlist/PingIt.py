''' 
     Ping ip, return legacy
'''

import subprocess
import re
import threading
import GetIPList


# create thread class
class PingIt(threading.Thread):
    def __init__(self, ipAddr):
        self.ipAddr = ipAddr
        self.pingTime = 0
        self.done = False
        self.cond = threading.Condition()
        threading.Thread.__init__(self)
        
    def run(self):
        self.cond.acquire()
        cmd = ['ping', '-n', '2', self.ipAddr]
        try:
            result = subprocess.check_output(cmd)
        except Exception as err1:
            result = -1
        if result != -1:
            p = re.compile('\d+ms')
            self.pingTime = p.findall(result)[-1:]
            p = re.compile('\d+')
            try:
                # get int ping value without 'ms' mark
                self.pingTime = int(p.findall(self.pingTime[0])[0])
            except Exception as pingTimeGetErr:
                print 'get pingTime error: {}'.format(pingTimeGetErr)
            #self.pingTime = self.pingTime[-1:]
        else:
            self.pingTime = result
        self.cond.notify()
        self.done = True
        self.cond.release()
    
    # return legacy value  
    def getLegacy(self):
        self.cond.acquire()
        while not self.done:
            self.cond.wait()
        self.cond.release()
        # return -1 or legacy value like [160ms]
        if type(self.pingTime) == list:
            try:
                return self.pingTime[0]
            except Exception as errRtn:
                print("error return self.pingTime[0]: {}".format(errRtn))
                print("ip: {}, pingTime: {}".format(self.ipAddr, self.pingTime))
                return self.pingTime
        return self.pingTime
        



if __name__ == "__main__":
    ipList = GetIPList.gainIpList()
    a = []
    for ip in ipList:
        p = PingIt(ip)
        p.start()
        p.getLegacy()
        #print pit.getLegacy()
    '''
    m = a[0]
    n = a[1]
    o = a[2]
    p = a[3]
    q = a[4]
    
    pit = PingIt(m)
    pit1 = PingIt(n)
    pit2 = PingIt(p)
    pit3 = PingIt(p)
    pit4 = PingIt(q)
    
    pit.start()
    pit1.start()
    pit2.start()
    pit3.start()
    pit4.start()
    
    print pit.getLegacy()
    print pit1.getLegacy()
    print pit2.getLegacy()
    print pit3.getLegacy()
    print pit4.getLegacy()
    '''
    '''
    for ip in ipList:
        pit = PingIt(ip)
        pit.start()
        #print pit.pingTime
        print pit.getLegacy()
    '''