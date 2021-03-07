## -*- coding: utf-8 -*-
import os
import shutil
import sys
import socket
import time
import pymysql
import platform
from PyQt5.QtNetwork import QTcpServer, QHostAddress
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWinExtras import *
from PyQt5.Qt import *
from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
from vmwc import VMWareClient


class MyThread(QThread):
    def  __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow
    def run(self):
        #ComboBoxDemo.printInbox(self, 'Вычисление номера ожидаемой сборки...695')
        #ComboBoxDemo.get_selected_leaves(self)
        file_path=''
        while not os.path.exists(file_path):
            time.sleep(60)

        if os.path.isfile(file_path):
            print('OK')
        else:
            raise ValueError("%s isn't a file!" % file_path)
class ComboBoxDemo(QMainWindow, QTreeWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("DL80autoInstaller_v 1.1")
        self.setFixedSize(640,480)
        self.checknewver = QCheckBox(self)
        self.checknewver.setGeometry(540, 80, 25, 25)
        self.label = QLabel("Включить отслеживание новой сборки DL:", self)
        self.label.setGeometry(310, 80, 230, 25)
        self.bnChange = QComboBox(self)
        self.bnChange.setGeometry(310, 40, 250, 30)
        bnlist=self.bnList()
        self.bnChange.addItems(bnlist)
        self.label1 = QLabel("Выберите сборку DL:", self)
        self.label1.setGeometry(310, 1, 110, 50)
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setGeometry(50, 300, 550, 170)
        self.pbar = QProgressBar(self)  
        self.pbar.setGeometry(50, 269, 550, 30)
        self.percentage = 0
        self.pbar.setTextVisible(self.percentage)
        self.pbar.setValue(self.percentage)
        self.btn = QPushButton('Установить Dallas Lock', self)
        self.btn.setStyleSheet("background-color: blue; color: white")
        self.btn.setGeometry(355, 235, 130, 30)
        self.setWindowIcon(QIcon('ips.ico'))
        self.taskbar_button = QWinTaskbarButton()
        self.taskbar_button.setWindow(self.windowHandle())
        self.taskbar_button.setOverlayIcon(QIcon('ips.ico'))
        self.treeConstructor()
        self.show()
        self.printInbox("Подключение к хосту 192.168.13.138 выполнено")
        self.btn.clicked.connect(self.get_selected_leaves)    
    def treeConstructor(self):
        self.tree = QTreeWidget(self)
        self.tree.setGeometry(50, 15, 250, 250)
        self.tree.setHeaderLabels(("Версия ОС:",))
        parent0 = QTreeWidgetItem(self.tree)
        self.p0=parent0
        parent0.setText(0, "All Windows")
        parent0.setFlags(parent0.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        osv=self.esxi()
        typeWinList=['Vista', '7', ' 8', '10', '2008', '2012','2016', '2019' ]
        for i in typeWinList:
            parent = QTreeWidgetItem(parent0)
            parent.setText(0, "Windows{}".format(i))
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            for x in osv:
                if i in x:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setText(0, "{}".format(x))
                    child.setCheckState(0, Qt.Unchecked)
    def get_selected_leaves(self):
        self.btn.setDisabled(True)
        checked_items = []
        def recurse(p0):
            for i in range(p0.childCount()):
                child = p0.child(i)
                grand_children = child.childCount()
                if grand_children > 0:
                    recurse(child)
                else: 
                    if child.checkState(0) == Qt.Checked:
                        checked_items.append(child.text(0))
        recurse(self.tree.invisibleRootItem())
        self.osvm=checked_items
        if self.checknewver.isChecked():
            self.printInbox('Включено отслеживание и установка новой сборки')
            MyThread.run(self)
        else:
            self.install()
        #return checked_items
    def waiting_build(self):

        file_path=''
        while not os.path.exists(file_path):
            time.sleep(60)

        if os.path.isfile(file_path):
            print('OK')
        else:
            raise ValueError("%s isn't a file!" % file_path)
                #choices = {'a': 1, 'b': 2}
                #result = choices.get(key, 'default')   
    def clear(self, froot):
        for subfolder in os.listdir(froot):
            f_path = os.path.join(froot, subfolder)
            del_f=shutil.rmtree(f_path)
    def printInbox(self, string): 
        self.textBrowser.append(string)
        QApplication.processEvents()
    def bnList(self):
        bnlist=[]
        sroot = r'\\192.168.0.162\czi-share\! DallasLock\DL80'
        os.chdir(sroot)
        for item in os.listdir(sroot):
             if os.path.isdir(item):
                if 'DL80' in item:
                    bnlist.append(item)
        bnlist=bnlist[::-1]
        return bnlist
    def esxi(self):
        connect = SmartConnectNoSSL(host='192.168.13.138', user='kvn', pwd='5745Ayc')
        content = connect.content
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        osv=[]
        pfx='Deploy'
        vm_list=container.view
        for vm in vm_list:
            if pfx in vm.name:
                osv.append(vm.name)
        Disconnect(connect)
        return osv
    def autorization(self, vm_name, lang):
        connect = SmartConnectNoSSL(host='192.168.13.138', user='kvn', pwd='5745Ayc')
        content = connect.content
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        vm_list=container.view
        for i in vm_list:
            if i.name == vm_name:
                vm=i
        if lang == 'RU':
            langchange=['0xe1']
            keyevent1=vim.UsbScanCodeSpecKeyEvent()
            hidCodeHexToInt1 = int(langchange[0], 16)
            hidCodeValue1 = (hidCodeHexToInt1 << 16) | 7
            keyevent1.usbHidCode = hidCodeValue1
            keyevent1.modifiers = vim.UsbScanCodeSpecModifierType()
            #keyevent1.modifiers.leftControl = True
            keyevent1.modifiers.leftAlt = True
            sp1 = vim.UsbScanCodeSpec()
            eventlist1=[keyevent1]
            sp1.keyEvents = eventlist1
            r1 = vm.PutUsbScanCodes(sp1)

        passw=['0x13', '0x04', '0x16', '0x16', '0x1a', '0x12', '0x15', '0x07', '0x1e', '0x28']
        for item in passw:
            keyevent2=vim.UsbScanCodeSpecKeyEvent()
            hidCodeHexToInt2 = int(item, 16)
            hidCodeValue2 = (hidCodeHexToInt2 << 16) | 7
            keyevent2.usbHidCode = hidCodeValue2
            keyevent2.modifiers = vim.UsbScanCodeSpecModifierType()
            if passw.index(item) == 0 or passw.index(item) == 8:
                keyevent2.modifiers.leftShift = True
                sp2 = vim.UsbScanCodeSpec()
                sp2.keyEvents = [keyevent2]
                r2 = vm.PutUsbScanCodes(sp2)
                keyevent2.modifiers.leftShift = False
            else:
                sp2 = vim.UsbScanCodeSpec()
                sp2.keyEvents = [keyevent2]
                r2 = vm.PutUsbScanCodes(sp2)
    def install(self):
        self.mythread_instance = MyThread(mainwindow=self)
        self.mythread_instance.start()
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.printInbox('Программа автоустановки Dallas Lock запущена!...')
        QThread.msleep(2000)
        bn = self.bnChange.currentText()
        try:
            os.remove('//192.168.0.162/Soft/TestIPS/auto/ip.txt')
            os.remove('//192.168.0.162/Soft/TestIPS/auto/usr.txt')
        except Exception as e:
            self.printInbox("Удаление файлов предыдущей установки")
        sroot = r'\\192.168.0.162\czi-share\! DallasLock\DL80'
        self.ProgressBar()
        szi=r'DallasLock8.0C.msi'
        sb=r'DL80.SecServerDemo10.msi'
        os.chdir(sroot)
        os.chdir(bn)
        shutil.copy('DallasLock8.0C.msi', '//192.168.0.162/Soft/TestIPS/auto/Auto_Install/PY_Inst/DallasLock8.0C.msi')
        shutil.copy('DL80.SecServerDemo10.msi', '//192.168.0.162/Soft/TestIPS/auto/Auto_Install/PY_Inst/DL80.SecServerDemo10.msi')
        self.printInbox(bn)
        self.printInbox('Идет копирование файлов установки...')
        QThread.msleep(2000)
        self.printInbox('Установка будет быполнена на следующие машины:')
        host = '192.168.13.138'
        username = 'kvn'
        password = '5745Ayc'
        snapshot_name = 'install'
        
        with VMWareClient(host, username, password) as client:
            for vm in client.get_virtual_machines():
                for v in self.osvm:
                    if vm.name == v:
                        for snapshot in vm.get_snapshots():
                            if snapshot.name == snapshot_name:
                                self.printInbox(vm.name)
                                vm_tofix=vm.name
                                snapshot.revert()
                                QThread.msleep(3000)
                                self.fix_reboot_stuck(vm_tofix)
                                self.printInbox("Загрузка виртуальной машины...")
        QThread.msleep(10000)
        if len(bn) > 24:
            bn=bn[:24]
            if bn[-3]==' ':
                bn=bn[-4::-1]
                bn=bn[::-1]
        elif len(bn) < 24:
            l=len(bn)
            bn=bn[:l]
        time.sleep(2)
        if bn.find('.') == 8:
            if bn.find(' ') == 10:
                bn1=bn[5:10]
            else:
                bn1=bn[5:11]
        else:
            bn1=bn[5:8]
        
        b = open('//192.168.0.162/Soft/TestIPS/auto/Auto_Install/PY_Inst/bn.txt', 'w')
        b.write(bn1)
        b.close()
        self.ProgressBar()
        QThread.msleep(300000)
        for vm_name in self.osvm:
            if vm_name == 'Deploy2016':
                self.autorization(vm_name, 'RU')
            else:
                self.autorization(vm_name, 'EN')
        self.printInbox('Вход в систему выполнен успешно')                  
    def finished(self):
        while not os.path.exists('//192.168.0.162/Soft/TestIPS/Auto/ip.txt'):
            self.ProgressBar()
            QThread.msleep(5000)
        i=open('//192.168.0.162/Soft/TestIPS/Auto/ip.txt', 'r')
        ip=i.read()
        i.close()
        QThread.msleep(3000)
        self.ProgressBar()
        u=open('//192.168.0.162/Soft/TestIPS/Auto/usr.txt', 'r')
        usr=u.read()
        u.close()
        os.remove('//192.168.0.162/Soft/TestIPS/auto/ip.txt')
        os.remove('//192.168.0.162/Soft/TestIPS/auto/usr.txt')
        self.ProgressBar()
        os.chdir('C:/')
        psw="Password!"
        #command0="cmdkey /generic:'{0}' /user:'{1}' /pass:'{2}'".format(ip, usr, psw)
        text_rdp=("IP адрес: " + ip + "\nЛогин: " + usr + "\nПароль: " + psw)
        self.printInbox(text_rdp)
        command1=("mstsc /v:%s" % ip)
        #os.system(command0)
        QThread.msleep(1000)
        os.system(command1)
        self.printInbox("Готово!")
        sys.exit()
        print('OK')
    def connect(self):
        s = socket.socket()
        port = 12345
        s.bind(('', port))
        s.listen(5)
        os.chdir('C:/')
        ip="10.10.101.213"
        path="cmd /c c:\1\1.py"
        cmd="wmic /node:'{0}' /user:kvn2019\Admin /password:Password! process call create '{1}'".format (ip, path)
        os.system(cmd)
        c, addr = s.accept()
        print ("Socket Up and running with a connection from", addr)
        while True:
            rcvdData = c.recv(1024).decode()
            print ("S:", rcvdData)
            sendData = input("Введите сообщение: ")
            c.send(sendData.encode())
            if(sendData == "Bye" or sendData == "bye"):
                break
        c.close()
    def ProgressBar(self):
        self.pbar.setValue(self.percentage)
        self.pbar.setTextVisible(self.percentage)
        while self.percentage >= 100:
            self.timer.stop() 
            #self.percentage = 0
        else: self.percentage += 2
    def fix_reboot_stuck(self, vm_name):
        connect = SmartConnectNoSSL(host='192.168.13.138', user='kvn', pwd='5745Ayc')
        content = connect.content
        container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
        vm_list=container.view
        for vm in vm_list:
            if vm_name == vm.name:
                vm.PowerOff()
                time.sleep(2)
                spec = vim.vm.ConfigSpec()
                opt = vim.option.OptionValue()
                spec.extraConfig = []
                opt.key = 'monitor_control.enable_softResetClearTSC'
                opt.value = 'TRUE'
                spec.extraConfig.append(opt)
                opt = vim.option.OptionValue()
                task = vm.ReconfigVM_Task(spec)
                time.sleep(2)
                vm.PowerOn()
        Disconnect(connect)
app = QApplication(sys.argv)
demo = ComboBoxDemo()
demo.show()
sys.exit(app.exec_())      