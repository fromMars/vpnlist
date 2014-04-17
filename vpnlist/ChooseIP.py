import PingIt
import GetIPList
# import ItemSelect
import threading



ipList = []
mlock = threading.RLock()
logfile = 'vpnlegacy_log.txt'
open(logfile, 'w').close()
allList = []
threads = []


def GetLegacy(ip, ipList, alLst):
    p = PingIt.PingIt(ip)
    p.start()
    pingValue = p.getLegacy()
    idxNum = ipList[ip][0]
    region = ipList[ip][1]
    ipInfo = ipList[ip][2:]
    if pingValue != -1:
        mlock.acquire()
        alLst.append([idxNum, ip, region, pingValue, ipInfo[0], ipInfo[1], ipInfo[2], ipInfo[3]])
        mlock.release()

def GetAll(ipList, alst):
    for ip in ipList:
        t = threading.Thread(target=GetLegacy, args=(ip, ipList, alst, ), name='thread-'+ip)
        t.start()
        threads.append(t)
        


if __name__ == "__main__":
    ipList = GetIPList.gainIpList()
    GetAll(ipList, allList)
    # wait all threads to finish
    for t in threads:
        t.join()
    
    for i in sorted(allList, cmp=lambda x,y:cmp(x[3],y[3])):
        print "%5s%20s%25s%10sms%20s%10s%10s%25s" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])
        GetIPList.wrtFile(logfile, "%5s%20s%25s%10sms%20s%10s%10s%25s" % \
                          (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
    