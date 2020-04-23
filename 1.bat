set PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python37\;%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;%SYSTEMROOT%\System32\WindowsPowerShell\v1.0\
rmdir C:\AutoDlInstall /S /Q
net use \\192.168.0.162\Soft\TestIPS\auto\Auto_Install /user:isc\kvn 5745Ayc
xcopy "\\192.168.0.162\Soft\TestIPS\auto\Auto_Install\*" "C:\AutoDlInstall\" /e
xcopy "C:\AutoDlInstall\db.py" "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\" /Y
net use \\192.168.0.162\Soft\TestIPS\auto\Auto_Install /delete
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" goto 64BIT
echo 32-bit OS
if not exist "%USERPROFILE%\AppData\Local\Programs\Python\Python37\python.exe" C:\AutoDlInstall\python-3.7.5.exe /quiet PrependPath=1
C:\AutoDlInstall\get-pip.py
%USERPROFILE%\AppData\Local\Programs\Python\Python37-32\Scripts\pip.exe install pywinauto
%USERPROFILE%\AppData\Local\Programs\Python\Python37-32\Scripts\pip.exe install pymysql
goto END
:64BIT
echo 64-bit OS
if not exist "%USERPROFILE%\AppData\Local\Programs\Python\Python37\python.exe" C:\AutoDlInstall\python-3.7.5-amd64.exe /quiet PrependPath=1
C:\AutoDlInstall\get-pip.py
%USERPROFILE%\AppData\Local\Programs\Python\Python37\Scripts\pip.exe install pywinauto
%USERPROFILE%\AppData\Local\Programs\Python\Python37\Scripts\pip.exe install pymysql
:END
cd C:\AutoDlInstall
C:\AutoDlInstall\PY_Inst\2.py
C:\AutoDlInstall\start_py.bat