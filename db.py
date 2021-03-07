import pymysql
import datetime
import time
import os
from pywinauto import Application
from subprocess import Popen
from pywinauto import Desktop
import socket
import urllib.request
import platform
import ssl
from pywinauto.keyboard import send_keys
import shutil

info=socket.gethostname()
print(info)
ip=socket.gethostbyname(info)
if os.path.exists('//192.168.0.162/Soft/TestIPS/auto/ip.txt'):
    os.remove('//192.168.0.162/Soft/TestIPS/auto/ip.txt')
    ipf=open('//192.168.0.162/Soft/TestIPS/auto/ip.txt', 'w+')
else:
    ipf=open('//192.168.0.162/Soft/TestIPS/auto/ip.txt', 'w+')
ipf.write(ip)
ipf.close()
if os.path.exists('//192.168.0.162/Soft/TestIPS/auto/usr.txt'):
    os.remove('//192.168.0.162/Soft/TestIPS/auto/usr.txt')
    shutil.copyfile('C:/AutoDlInstall/usr.txt', '//192.168.0.162/Soft/TestIPS/auto/usr.txt')
else:
    shutil.copyfile('C:/AutoDlInstall/usr.txt', '//192.168.0.162/Soft/TestIPS/auto/usr.txt')
osv=platform.platform()
f=open('C:/AutoDlInstall/PY_Inst/bn.txt', 'r')
bn=f.read()
f.close()
print('Сборка №',bn)

response=None
"""try:
    print("Checking Internet access...")
    url = "http://www.nalog.ru"
    context=ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context, timeout=10).read().decode('utf-8')
except (ValueError, RuntimeError, TypeError, NameError) as error:
    print('Data not retrieved because' , error, url)
except socket.timeout as err:
    print('Data not retrieved because', err, url)"""
    
    
MAX_RETRY = 5
print("Checking Internet access...")
def get_html(html_url, timeout=10, decode='utf-8'):
    html_url = "http://www.nalog.ru"
    for tries in range(MAX_RETRY):
        try:
            with urllib.request.urlopen(html_url, timeout=timeout) as response:
                return response.read().decode(decode)
        except Exception as e:
            logging.warning(str(e) + ',html_url:{0}'.format(html_url))
            if tries < (MAX_RETRY - 1):
                continue
            else:
                print('Has tried {0} times to access url {1}, all failed!'.format(MAX_RETRY, html_url))
                return None

conn=pymysql.connect(host='192.168.130.153',user='mysql', password='', database='otis')
cur1=conn.cursor()
#cur1.execute("create table autoinstall (id INT AUTO_INCREMENT PRIMARY KEY, build VARCHAR(255), status VARCHAR(11))")
cur1.execute("UPDATE autoinstall SET status= '1' WHERE status='2' AND hostname=%s", info)
conn.commit()
conn.close()
    
send_keys('{ESC 1}')   
app = Application().start("C:\DLLOCK80\TestProg.exe")
p=app.process
print("PID =", p)
time.sleep(5)
dlg=app["СЗИ НСД Dallas Lock 8.0-C. Автоматическое тестирование функций СЗИ"].NextButton.click_input()
time.sleep(10)
app1 = Application().start("C:\DLLOCK80\AdmShell.exe")
p=app1.process
print("PID =", p)   


if response is not None:
    ts = time.time()
    timestamp1 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    conn=pymysql.connect(host='192.168.130.153',user='mysql', password='mysql', database='otis')
    x = conn.cursor()
    timestamp2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    x.execute("INSERT into autotests (testname, build, timestart, timefinish, status, hostname, host_ip, os) VALUES ('InternetAccess', %s, %s, %s, 1, %s, %s, %s)",(bn,timestamp1,timestamp2, info, ip, osv))
    conn.commit()
    conn.close()
else:
    ts = time.time()
    timestamp1 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    conn=pymysql.connect(host='192.168.130.153',user='mysql', password='mysql', database='otis')
    x = conn.cursor()
    timestamp2 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    x.execute("INSERT into autotests (testname, build, timestart, timefinish, status, hostname, host_ip, os) VALUES ('InternetAccess', %s, %s, %s, 0, %s, %s, %s)",(bn,timestamp1,timestamp2, info, ip, osv))
    conn.commit()
    conn.close()
try:
    shutil.copyfile('//192.168.0.162/Soft/TestIPS/auto/usr.txt', 'C:/AutoDlInstall/usr.txt')
except Exception as e:
    print('OK')
os.system('C:/AutoDlInstall/start_pySB.bat')
"""time.sleep(5)
dlg1=app["Уведомление"].NextButton.click_input()
time.sleep(5)
dlg11=app["Уведомление"].NextButton.click_input()"""
