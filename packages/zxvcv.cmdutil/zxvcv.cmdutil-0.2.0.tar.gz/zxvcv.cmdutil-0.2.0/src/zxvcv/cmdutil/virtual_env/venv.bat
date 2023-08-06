set VenvsDir=C:\PythonVenv

:: Create python virtual env
DOSKEY venvi=zxvcv.venvi $*

:: Remove python virtual env by name
DOSKEY venvr=zxvcv.venvr $*

:: List python virtual envs in VenvsDir
DOSKEY venvl=zxvcv.venvl $*

:: Activate python virtual env
DOSKEY venva=%VenvsDir%\$1\Scripts\activate.bat

:: Deactivate python virtual env
DOSKEY venvd=deactivate
