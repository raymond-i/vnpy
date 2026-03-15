@ECHO OFF
REM Day 1 使用项目 .venv 启动 Trader（无需连接 CTP）
SET VNPY_ROOT=%~dp0..\..
SET VENV_PY=%VNPY_ROOT%\.venv\Scripts\python.exe
if not exist "%VENV_PY%" (
    echo .venv not found at %VNPY_ROOT%\.venv
    echo Please create it: python -m venv .venv then install vnpy.
    pause
    exit /b 1
)
cd /d "%~dp0"
"%VENV_PY%" run_day1.py
pause
