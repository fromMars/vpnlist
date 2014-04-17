''' This Script is used to get the IP list from VPN Gate Client Plugin,
    and ping a specified IP address(eg: www.google.com) to determing the
    lowest legacy VPN server.
'''

from ctypes import *
from pywinauto import win32structures, win32defines
import win32api
import win32gui
import win32con
import win32process
import commctrl


# write log file
def wrtFile(path, stri):
    wf = open(path, 'a')
    wf.write(stri)
    wf.close()

# get the {ip:region} dictionary
def gainIpList():
    ipList = {}
    KERNEL32 = windll.kernel32
    dwBufSize = 64
    
    # find vpn list view handle
    try:
        hVpn = win32gui.FindWindow(None, "VPN Gate Academic Experimental Project Plugin for SoftEther VPN Client")
        # hVpn = win32gui.FindWindow(None, "Downloads - WinRAR (evaluation copy)")
        # hVpn = win32gui.FindWindow(None, "SoftEther VPN Client Manager")
        hChild = win32gui.FindWindowEx(hVpn, 0, "SysListView32", None)
    except Exception as errFindHandle:
        print ("FindWindow failed, '{}'".format(errFindHandle))
    print ("hVpn: {},\thChile: {}".format(hVpn, hChild))
    
    # inject process
    try:
        threadId, processId = win32process.GetWindowThreadProcessId(hChild)
        hProcess = KERNEL32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, processId)
    except Exception as errCreateProcess:
        print ("Create process failed, '{}'".format(errCreateProcess))
    print ("threadId: {},\tprocessId: {}".format(threadId, processId))
    
    # Allocate memory
    try:    
        dll_address = KERNEL32.VirtualAllocEx(hProcess, 0, dwBufSize, win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
        _lvi = KERNEL32.VirtualAllocEx(hProcess, 0, dwBufSize, win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    except Exception as errAllocEx:
        print ("Alloc memory failed, '{}'".format(errAllocEx))
        
    # create local buffer
    target_buff = create_string_buffer(dwBufSize)
        
    # declare lvitem
    lvitem = win32structures.LVITEMW()
    lvitem.mask = win32defines.LVIF_TEXT
    lvitem.iItem = 0
    lvitem.cchTextMax = dwBufSize
    lvitem.pszText = _lvi
    lvitem.nLen = 1280
    
    
    # Get item text
    listCount = win32api.SendMessage(hChild, commctrl.LVM_GETITEMCOUNT)
    #KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)

    for i in range(listCount):
        lvitem.iItem = i
        # get IP Address (Hostname)
        lvitem.iSubItem = 1
        KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)
        win32api.SendMessage(hChild, commctrl.LVM_GETITEMTEXT, i, _lvi)
        KERNEL32.ReadProcessMemory(hProcess, _lvi, target_buff, dwBufSize, None)
        ipAddr = target_buff.value
            # cut off useless strings
        brkPos = ipAddr.find('(')
        if brkPos != -1:
            ipAddr = ipAddr[:brkPos]
        # get Region
        lvitem.iSubItem = 2
        KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)
        win32api.SendMessage(hChild, commctrl.LVM_GETITEMTEXT, i, _lvi)
        KERNEL32.ReadProcessMemory(hProcess, _lvi, target_buff, dwBufSize, None)
        region = target_buff.value
        #ipList[ipAddr: no, region, VPNSession,...]
        ipList[ipAddr] = [i, region]
        # get VPNSession
        lvitem.iSubItem = 4
        KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)
        win32api.SendMessage(hChild, commctrl.LVM_GETITEMTEXT, i, _lvi)
        KERNEL32.ReadProcessMemory(hProcess, _lvi, target_buff, dwBufSize, None)
        sessCount = target_buff.value
        ipList[ipAddr].append(sessCount)
        # get Speed
        lvitem.iSubItem = 5
        KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)
        win32api.SendMessage(hChild, commctrl.LVM_GETITEMTEXT, i, _lvi)
        KERNEL32.ReadProcessMemory(hProcess, _lvi, target_buff, dwBufSize, None)
        linkSpeed = target_buff.value
        ipList[ipAddr].append(linkSpeed)
        # get g_ping
        lvitem.iSubItem = 6
        KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)
        win32api.SendMessage(hChild, commctrl.LVM_GETITEMTEXT, i, _lvi)
        KERNEL32.ReadProcessMemory(hProcess, _lvi, target_buff, dwBufSize, None)
        googlePing = target_buff.value
        ipList[ipAddr].append(googlePing)
        # get opened ports
        lvitem.iSubItem = 7
        KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), None)
        win32api.SendMessage(hChild, commctrl.LVM_GETITEMTEXT, i, _lvi)
        KERNEL32.ReadProcessMemory(hProcess, _lvi, target_buff, dwBufSize, None)
        opened_ports = target_buff.value
        ipList[ipAddr].append(opened_ports)
    
    # clearing up
    KERNEL32.VirtualFreeEx(hProcess, dll_address, 0, win32con.MEM_RELEASE)
    KERNEL32.VirtualFreeEx(hProcess, _lvi, 0, win32con.MEM_RELEASE)
    KERNEL32.CloseHandle(hProcess)
    
    return ipList


if __name__ == "__main__":
    li = gainIpList()
    print li
    i = 0
    for key in li:
        i = i + 1
        
    print i
    