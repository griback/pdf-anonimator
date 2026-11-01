@echo off
setlocal
cd /d "%~dp0"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm --clean --onefile --windowed --name AnonimizadorPDF_v3 anonimizador_pdf.py
if exist "dist\AnonimizadorPDF_v3.exe" (
 echo.
 echo OK: dist\AnonimizadorPDF_v3.exe
) else (
 echo ERRO: o executavel nao foi criado.
)
pause
