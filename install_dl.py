# -*- coding: utf-8 -*-
import os
import shutil
import sys
import time

try:
    os.remove('//192.168.0.162/Soft/TestIPS/auto/ip.txt')
    os.remove('//192.168.0.162/Soft/TestIPS/auto/usr.txt')
except Exception as e:
     print ("")   
bn=str(input('Введите номер сборки Dallas Lock (например, 630): '))
osv=str(input('Введите версию Windows (например, 2016, 10 и т.д.): '))

sroot = r'\\192.168.0.162\czi-share\! DallasLock\DL80'
droot = r'\\192.168.0.162\czi-share\ОТиС\Казначеев\DL'
froot = droot + "\\" + osv
szi=r'DallasLock8.0C.msi'
sb=r'DL80.SecServerDemo10.msi'
os.chdir(sroot)
for item in os.listdir(sroot):
    if os.path.isdir(item):
        if bn in item:
            os.chdir(item)
            shutil.copyfile(sb, '//192.168.0.162/Soft/TestIPS/auto/Auto_Install/PY_Inst/DL80.SecServerDemo10.msi')
            dst=os.path.join(froot , item)
            if not os.path.exists(dst):
                os.mkdir(dst)
            dt=dst + ("\\" + szi)
            shutil.copyfile(szi, dt)
            print('Идет копирование файлов установки...')
            time.sleep(2)
print('Запущен процеcc установки сборки', bn, 'на Windows', osv, '...\nКогда установка завершится, появится окно авторизации RDP.' )
time.sleep(3)
while not os.path.exists('//192.168.0.162/Soft/TestIPS/Auto/ip.txt'):
    time.sleep(10)
    
i=open('//192.168.0.162/Soft/TestIPS/Auto/ip.txt', 'r')
ip=i.read()
i.close()
time.sleep(3)
u=open('//192.168.0.162/Soft/TestIPS/Auto/usr.txt', 'r')
usr=u.read()
u.close()
os.remove('//192.168.0.162/Soft/TestIPS/auto/ip.txt')
os.remove('//192.168.0.162/Soft/TestIPS/auto/usr.txt')
os.chdir('C:/')
psw="Password!"
command0="cmdkey /generic:'{0}' /user:'{1}' /pass:'{2}'".format(ip, usr, psw)
print("IP адрес:", ip, "\nЛогин:", usr, "\nПароль:", psw)
command1=("mstsc /v:%s" % ip)
os.system(command0)
time.sleep(1)
os.system(command1)
