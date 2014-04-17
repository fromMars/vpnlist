from DB.models import VPNserver, ServStats
import GetIPList
import re


def AddIP(ip, ip_list):
    ip_info = ip_list[ip]
    p = re.compile('\d+')
    ip_info[2] = p.findall(ip_info[2])
    p = VPNserver.objects.create(ip_addr=ip, 
                                 region=ip_info[1])
    ServStats.objects.create(port=ip_info[5], 
                             ping=int(ip_info[0]), 
                             session_count=int(ip_info[2][0]),
                             link_speed=ip_info[3], 
                             ping_ex=ip_info[4], 
                             vpn_server=p)
    print '%20s added.' % ip
    
    
def UpdateIP(ip, ip_list):
    ip_info = ip_list[ip]
    p = re.compile('\d+')
    ip_info[2] = p.findall(ip_info[2])
    p_serv = VPNserver.objects.get(ip_addr=ip)
    ServStats.objects.create(port=ip_info[5], 
                  ping=int(ip_info[0]), 
                  session_count=int(ip_info[2][0]),
                  link_speed=ip_info[3], 
                  ping_ex=ip_info[4], 
                  vpn_server=p_serv)
    print '%20s updated.' % ip
    
    
def AddorUpdate(ip, ip_list):
    try:
        VPNserver.objects.get(ip_addr=ip)
    except Exception:
        print ("Adding new vpn server information ...")
        AddIP(ip, ip_list)
        return 1
    UpdateIP(ip, ip_list)
    return 2


def UpdateHistory(ip_list):
    for ip in ip_list:
        AddorUpdate(ip, ip_list)


def GetAllList():
    try:
        server_list = VPNserver.objects.all().iterator()
    except Exception as serv_list_err:
        print "get server_list error:%s" % serv_list_err
        return -1
    
    serv_list = []
    for ip in server_list:
        serv_list.append([ip.ip_addr, ip.region])
    
    return serv_list


def GetPingHistory(ip):
    print "ip is:", ip
    try:
        vpn_serv = VPNserver.objects.all().get(ip_addr = ip)
    except Exception as ping_vpnserv_err:
        print "get vpn_serv error:%s" % ping_vpnserv_err
        return -1
        
    try:
        ping_history_list = ServStats.objects.all().filter(vpn_server = vpn_serv).order_by('update_time')
    except Exception as his_list_err:
        print "get ping history list error:%s" % his_list_err
        return -1
    
    return ping_history_list[0]
    

if __name__ == "__main__":
    ip_list = GetIPList.gainIpList()
    #print AddorUpdate('106.1.89.7', ip_list)
    UpdateHistory(ip_list)