@echo off
SETLOCAL

@REM set PythonRoot=%~dp0..\..\..\..\..\..\python.exe
@REM set PythonRoot=C:\Python311\python.exe
py -m zxvcv.cmdutil.pvenv.list %*
