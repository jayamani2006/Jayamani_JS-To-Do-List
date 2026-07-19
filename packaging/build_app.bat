@echo off
:: Build the Python app using spec
python -m PyInstaller todo_app.spec

:: Copy the EXE to Desktop
copy /y "dist\todo_app.exe" "%USERPROFILE%\Desktop\JS-To-Do-List.exe"

:: Notify via VBScript
cscript //nologo notify.vbs

exit
