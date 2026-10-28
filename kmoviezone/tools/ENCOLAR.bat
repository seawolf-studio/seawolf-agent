@echo off
REM ============================================
REM  kmoviezone - ENCOLAR EN MIPONY
REM  Uso:  ENCOLAR.bat               -> usa cola-enlaces.txt
REM        ENCOLAR.bat otro.txt      -> usa ese archivo
REM        o ARRASTRE un .txt sobre este .bat
REM  IMPORTANTE: cierre MiPony antes de usar esto.
REM ============================================
cd /d "%~dp0"
title kmoviezone - ENCOLAR A MIPONY
set "ARCHIVO=%~1"
if "%ARCHIVO%"=="" set "ARCHIVO=cola-enlaces.txt"
echo ============================================
echo  ENCOLAR ENLACES EN MIPONY
echo  Archivo de carga: %ARCHIVO%
echo ============================================
echo.
echo  Verificando si MiPony esta abierto...
tasklist | find /i "mipony" >nul && (
  echo.
  echo  *** MIPONY ESTA ABIERTO ***
  echo  Cierralo y vuelve a ejecutar este archivo.
  echo.
  pause
  exit /b
)
echo  MiPony cerrado. Encolando...
echo.
python mipony.py encolar "%ARCHIVO%"
echo.
pause
