chcp 1251 >NUL
set /p usr=<C:\AutoDlInstall\1.txt
chcp 866 >NUL
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" goto 64BIT
cd %usr%\AppData\Local\Programs\Python\Python37-32\
start C:\AutoDlInstall\bin\1.exe cmd.exe "/k python.exe C:\AutoDlInstall\db2.py"
goto END
:64BIT
cd %usr%\AppData\Local\Programs\Python\Python37\
start C:\AutoDlInstall\bin\1_x64.exe cmd.exe "/k python.exe C:\AutoDlInstall\db2.py"
:END