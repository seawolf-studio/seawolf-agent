@echo off
REM ============================================
REM  kmoviezone - ENCOLAR EN MIPONY
REM  Lee cola-enlaces.txt y mete los enlaces a MiPony.
REM  IMPORTANTE: cierra MiPony antes de usar esto.
REM ============================================
cd /d "%~dp0"
title kmoviezone - ENCOLAR A MIPONY
echo ============================================
echo  ENCOLAR ENLACES EN MIPONY
echo  Archivo de carga: cola-enlaces.txt
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
python mipony.py encolar
echo.
pause
