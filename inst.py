import os
import time
import winnt
import win32api
import win32con
import subprocess
import win32ui
import pywinauto
from pywinauto import * 
from pywinauto import Application
from pywinauto import Desktop
import win32ui
import pymysql
import socket
import platform
from pywinauto.keyboard import send_keys

info=socket.gethostname()
ip=socket.gethostbyname(info)
osv=platform.platform()
f=open('C:/AutoDlInstall/PY_Inst/bn.txt', 'r')
bn=f.read()
f.close()
ver=open('C:/AutoDlInstall/PY_Inst/bdt.txt', 'r')
bdt=ver.read().split('\n')[0]
ver.close()

print('Будет установлен',bdt)

conn=pymysql.connect(host='192.168.130.153',user='mysql', password='mysql', database='otis')
cur1=conn.cursor()
#cur1.execute("create table autoinstall (id INT AUTO_INCREMENT PRIMARY KEY, build VARCHAR(255), status VARCHAR(11))")
cur1.execute("insert into autoinstall (build, status, hostname, os, host_ip) VALUES (%s, 2, %s, %s, %s)", (bn, info, osv, ip))
conn.commit()
conn.close()



send_keys('{ESC 1}')

time.sleep(5)
prid=subprocess.Popen(["msiexec", "/i", r"C:\AutoDlInstall\PY_Inst\DallasLock8.0C.msi"], shell=True)
time.sleep(35)
app=Application().connect(title=bdt)
time.sleep(2)
top=app.top_window()
top.minimize()
top.restore()
p=app.process
print("PID =", p)
time.sleep(5)
os.chdir(r"C:\DLLOCK80\Files_x86")
os.remove("DlCredProv.dll")
f=open("newfile.txt", "w")
f.close()
os.rename("newfile.txt", "DlCredProv.dll")
os.chdir(r"C:\DLLOCK80\Files_x64")
os.remove("DlCredProv.dll")
g=open("newfile.txt", "w")
g.close()
os.rename("newfile.txt", "DlCredProv.dll")
dlg=app[bdt].NextButton.click_input()
time.sleep(1)
dlg1=app[bdt].Edit.type_keys("1-2160-1519")
dlg11=app[bdt].Edit2.type_keys("25774927-865")
if len(bn)<6:
    dlg12=app[bdt].Button2.click_input()
else:
    dlg12=app[bdt].Button1.click_input()
time.sleep(2)
dlg2=app[bdt].ComboBox.type_keys('{DOWN 3}')
time.sleep(1)
dlg21=app[bdt].Edit3.type_keys("^a{BACKSPACE}")
time.sleep(1)
cfg="C:\AutoDlInstall\cfg\\fortest.dlc"
print(cfg)
dlg21=app[bdt].Edit3.set_text(cfg)
if len(bn)<6:
    dlg22=app[bdt].Button2.click_input()
else:
    dlg22=app[bdt].Button1.click_input()
time.sleep(2)
time.sleep(35)
dlg4=app[bdt].Button1.click_input()
if len(bn)<6:
    print('Готово')
else:
    reboot=app[bdt].Button1.click_input()
f=open('c:\\AutoDlInstall\\usr.txt', 'r')
user=f.read()
f.close()
hKey, flag = win32api.RegCreateKeyEx(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Provider Filters\{06BEC7B3-65ED-4DAD-A5C5-48C81928D2B2}', win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY, Options=winnt.REG_OPTION_VOLATILE)
win32api.RegSetValueEx(hKey, 'Disabled', 0, winnt.REG_DWORD, 1)
hKey, flag = win32api.RegCreateKeyEx(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon', win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY, Options=winnt.REG_OPTION_VOLATILE)
win32api.RegSetValueEx(hKey, 'DefaultPassword', 0, winnt.REG_SZ, 'Password!')
hKey, flag = win32api.RegCreateKeyEx(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon', win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY, Options=winnt.REG_OPTION_VOLATILE)
win32api.RegSetValueEx(hKey, 'DefaultUserName', 0, winnt.REG_SZ, user)
hKey, flag = win32api.RegCreateKeyEx(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon', win32con.KEY_ALL_ACCESS | win32con.KEY_WOW64_64KEY, Options=winnt.REG_OPTION_VOLATILE)
win32api.RegSetValueEx(hKey, 'AutoAdminLogon', 0, winnt.REG_SZ, '1')
print("Dallas Lock установлен!")