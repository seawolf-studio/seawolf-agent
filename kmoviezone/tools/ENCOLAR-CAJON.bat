@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title kmoviezone - ENCOLAR UN CAJON
color 0B

if not exist "cajones" (
  echo.
  echo   *** No existe la carpeta "cajones" ***
  echo   Avisa a Bellion.
  echo.
  pause
  exit /b
)

echo ==================================================
echo    ENCOLAR UN CAJON EN MIPONY
echo ==================================================
echo.
set /a n=0
for %%f in ("cajones\*.txt") do (
  set /a n+=1
  set "f!n!=%%~ff"
  echo    !n!.  %%~nxf
)
echo.
echo    0.  Cancelar
echo.
if %n%==0 (
  echo   La carpeta cajones esta vacia.
  echo.
  pause
  exit /b
)
set "opc="
set /p opc="  Numero del cajon a encolar: "
echo.
if "%opc%"=="" exit /b
if "%opc%"=="0" exit /b
set "ARCHIVO=!f%opc%!"
if "!ARCHIVO!"=="" (
  echo   *** Opcion invalida ***
  echo.
  pause
  exit /b
)
echo   Cajon elegido: !ARCHIVO!
echo.

echo   Verificando si MiPony esta abierto...
tasklist | find /i "mipony" >nul && (
  echo.
  echo   *** MIPONY ESTA ABIERTO ***
  echo   Cierrelo y vuelva a ejecutar este archivo.
  echo   ^(Si le escribimos con MiPony abierto, se PIERDEN los enlaces^)
  echo.
  pause
  exit /b
)

echo   MiPony cerrado. Encolando...
echo.
python mipony.py encolar "!ARCHIVO!"
echo.
echo ==================================================
echo   LISTO. Abra MiPony y vera los enlaces.
echo ==================================================
echo.
pause
