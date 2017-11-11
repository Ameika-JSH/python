@echo off
setx test c:\test\;c:\test2\;c:\test3\; /m
if '%errorlevel%' NEQ '0' (
  echo get admin...
  goto UACPrompt
) else ( goto gotAdmin )
:UACPrompt
  echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
  set params = %*:"=""
  echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

  "%temp%\getadmin.vbs"
  rem del "%temp%\getadmin.vbs"
:gotAdmin
  exit
