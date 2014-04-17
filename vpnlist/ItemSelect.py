''' 
    Select the row by the ip address we selected
'''

from ctypes import *
from pywinauto import win32structures, win32defines
import win32api
import win32gui
import win32con
import win32process
import commctrl
import sys
import GetIPList



'''
# get the index according to the IP address
def FindIndex(ipAddr, ipList):
    pass
'''

# select row according to the index supplied
def SelectItem(num, dblclick):
    KERNEL32 = windll.kernel32
    dwBufSize = 1024
    
    # find vpn list view handle
    try:
        hVpn = win32gui.FindWindow(None, "VPN Gate Academic Experimental Project Plugin for SoftEther VPN Client")
        hChild = win32gui.FindWindowEx(hVpn, 0, "SysListView32", None)
        hCon = win32gui.FindWindowEx(hVpn, 0, None, "&Connect to the VPN Server")
    except Exception as errFindHandle:
        print ("FindWindow failed, '{}'".format(errFindHandle))
    print ("hVpn: {},\thChild: {}\thCon: {}".format(hVpn, hChild, hCon))
    
    # inject process
    try:
        threadId, processId = win32process.GetWindowThreadProcessId(hChild)
        hProcess = KERNEL32.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, processId)
    except Exception as errCreateProcess:
        print ("Create process failed, '{}'".format(errCreateProcess))
    print ("threadId: {},\tprocessId: {}".format(threadId, processId))
    
    # Allocate memory
    try:    
        _lvi = KERNEL32.VirtualAllocEx(hProcess, 0, dwBufSize, win32con.MEM_RESERVE|win32con.MEM_COMMIT, win32con.PAGE_READWRITE)
    except Exception as errAllocEx:
        print ("Alloc memory failed, '{}'".format(errAllocEx))
        
         
    # declare lvitem
    lvitem = win32structures.LVITEMW()
    lvitem.mask = win32defines.LVIF_STATE
    lvitem.iItem = num
    lvitem.iSubItem = 0
    #lvitem.state = win32defineswin32defines.LVIS_SELECTED
    lvitem.stateMask = win32defines.LVIS_SELECTED
    lvitem.cchTextMax = 0


    # deselect all
    KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), 0)
    lvitem.stateMask = win32defines.LVIS_SELECTED
    #lvitem.state = 0
    win32api.SendMessage(hChild, commctrl.LVM_SETITEMSTATE, -1, _lvi)
    
    # select one
    lvitem.stateMask = win32defines.LVIS_SELECTED|win32defines.LVIS_FOCUSED
    lvitem.state = win32defines.LVIS_SELECTED|win32defines.LVIS_FOCUSED
    KERNEL32.WriteProcessMemory(hProcess, _lvi, addressof(lvitem), sizeof(lvitem), 0)
    #win32gui.SetWindowPos(hVpn, win32con.HWND_TOPMOST, 620, 283, 800, 600, \
    #                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| \
    #                      win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
    #win32gui.SetForegroundWindow(hChild)
    win32api.SendMessage(hChild, commctrl.LVM_SETITEMSTATE, num, _lvi)
    win32api.SendMessage(hChild, commctrl.LVM_ENSUREVISIBLE, num, _lvi)
    if dblclick == 1:
        win32gui.SetActiveWindow(hVpn)
        #win32api.SendMessage(hCon, win32con.BM_CLICK, 0, 0)
        win32api.SendMessage(hVpn, win32con.WM_COMMAND, \
                             win32api.MAKEWORD(win32con.IDOK, win32con.BN_CLICKED), hCon)
    '''
    try:
        win32gui.SetActiveWindow(hVpn)
        hIDOK = win32gui.FindWindowEx(hVpn, 0, None, "Select VPN Protocol to Connect")
        hChild_IDOK = win32gui.FindWindowEx(hVpn, 0, None, "&OK")
        win32api.SendMessage(hChild_IDOK, win32con.BM_CLICK, 0, 0)
    except Exception as errFindIDOKHandle:
        print ("FindWindow failed, '{}'".format(errFindIDOKHandle))
    print ("hIDOK: {},\thChild_IDOK: {}".format(hIDOK, hChild_IDOK))
   '''
    
    # clearing up
    KERNEL32.VirtualFreeEx(hProcess, _lvi, 0, win32con.MEM_RELEASE)
    KERNEL32.CloseHandle(hProcess)
    
# find the num in list of current selected ip
def ip2num(ip):
    ipList = GetIPList.gainIpList()
    num = ipList.get(ip)
    if num is None:
        return -1
    return num[0]



if __name__ == "__main__":
    SelectItem(int(sys.argv[1]), 0)

    