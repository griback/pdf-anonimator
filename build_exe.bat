@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
if errorlevel 1 goto erro
".venv\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto erro
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto erro
".venv\Scripts\python.exe" build.py
if errorlevel 1 goto erro
pause
exit /b 0
:erro
echo ERRO: a geracao foi interrompida. Verifique a mensagem acima.
pause
exit /b 1
