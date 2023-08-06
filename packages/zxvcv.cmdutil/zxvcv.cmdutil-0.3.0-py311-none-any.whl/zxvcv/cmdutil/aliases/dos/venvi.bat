@echo off
SETLOCAL

IF "%1"=="--help" (
    echo Initialize python virtual env
    echo usage venvi [--help] pyver args
    echo.
    echo arguments:
    echo   --help      show brief help message
    echo   pyver       python version which should beused to create virtual environment
    echo   args        arguments for python script what will create virtual environment
    goto end_fun
)

set PYTHON_NUMBER=%1
set STRIPPEDPARAMS=
shift
:strip_params
if "%1"=="" goto main_fun
set STRIPPEDPARAMS=%STRIPPEDPARAMS% %1
shift
goto strip_params

:main_fun
py -%PYTHON_NUMBER% -m zxvcv.cmdutil.pvenv.initialize %STRIPPEDPARAMS%

:end_fun
