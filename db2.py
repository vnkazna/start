import pymysql
import time
from pywinauto import Application
import subprocess
from pywinauto import Desktop
import socket
import shutil

fsb=open('C:/AutoDlInstall/PY_Inst/bdt.txt', 'r')
v=fsb.read().split('\n')[0]
fsb.close()
b=v.split('-C')
d=u' Сервер безопасности Демо-версия.'
b.insert(1, d)
bdt="".join(b)
prid=subprocess.Popen(["msiexec", "/i", r"C:\AutoDlInstall\PY_Inst\DL80.SecServerDemo10.msi"], shell=True)
time.sleep(5)
app=Application().connect(title=bdt)
p=app.process
time.sleep(2)
dlg1=app[bdt].NextButton.click_input()
time.sleep(1)
dlg2=app[bdt].Button2.click_input()
time.sleep(1)
dlg3=app[bdt].Button2.click_input()
time.sleep(1)
dlg4=app[bdt].Button2.click_input()
time.sleep(4)
dlg5=app[bdt].Button.click_input()