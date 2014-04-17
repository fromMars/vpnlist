from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from django.utils import simplejson
from ChooseIP import *
from ItemSelect import *
import IPHistory

import threading
import PingIt
import datetime
import time
import os


# homepage
def homepage(request):
    p_homepage = get_template('home.html')
    server_file = 'softether-vpnserver-v4.06-9432-beta-2014.03.20-linux-x64-64bit.tar.gz'
    client_file = 'vpngate-client-2014.03.22-build-9433.129212.zip'
    server_list = IPHistory.GetAllList()
    lp = IPHistory.GetPingHistory("183.101.156.243")
    if lp == -1:
        last_ping = ["ERROR", "ERROR", "ERROR", "ERROR", "ERROR"]
    else:
        last_ping = [lp.update_time, lp.ping, lp.port, lp.ping_ex, lp.link_speed]
    html = p_homepage.render(Context({'server_file': server_file, 
                                      'client_file': client_file,
                                      'server_list': server_list,
                                      'last_ping': last_ping}))
    
    return HttpResponse(html)


# file download
def dl_file(request, file_name):
    c = open("C:\Users\ZMB\Downloads\%s"%file_name, 'rb').read()
    response = StreamingHttpResponse(FileWrapper(c), mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name
    
    return HttpResponse(c)


# get ajax ping value
def ping_ip(request, ip):
    p = PingIt.PingIt(ip)
    p.start()
    pingValue = p.getLegacy()
    
    return HttpResponse(pingValue)


# get ip list
def ip_list(request):
    allList = []
    ipList = GetIPList.gainIpList()
    GetAll(ipList, allList)
    # wait all threads to finish
    for t in threads:
        t.join()
        
    # auto DB backup
    t_db = threading.Thread(target=IPHistory.UpdateHistory, args=(ipList,))
    t_db.start()
    
    if allList is None:
        raise Http404()
    
    p_list = get_template('iplist.html')
    al = sorted(allList, cmp=lambda x,y:cmp(x[3],y[3]))
    html = p_list.render(Context({'all_list': al}))
    
    return HttpResponse(html)
    

# retrive newest server information
def get_serv_info(request, ip):
    lp = IPHistory.GetPingHistory(ip)
    if lp == -1:
        last_ping = ["ERROR", "ERROR", "ERROR", "ERROR", "ERROR"]
    else:
        last_ping = {'update_time': lp.update_time.strftime('%Y-%m-%d %H:%M:%S'), 
                     'ping': lp.ping, 
                     'port': lp.port, 
                     'ping_ex': lp.ping_ex, 
                     'link_speed': lp.link_speed}

    return HttpResponse(simplejson.dumps(last_ping, ensure_ascii=False))

    
# select ip
def item_select(request, ip, enter_it):
    rowid = ip2num(ip)
    html = 'Selected'
    if rowid == -1:
        html = 'Not Found'
    SelectItem(int(rowid), int(enter_it))
    return HttpResponse(html)


# select server
def serv_select(request, ip):
    pass
    