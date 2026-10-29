@echo off
title Leer SMART de los discos (administrador)
cd /d "%~dp0"

REM ---- Se auto-eleva: si no es administrador, se relanza pidiendo permisos ----
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo.
  echo   ============================================================
  echo     LECTURA SMART - necesita permisos de administrador
  echo   ============================================================
  echo.
  echo     Windows va a mostrar una ventana preguntando si permitir.
  echo     Pulse  "Si"  y la lectura arranca sola.
  echo.
  echo     (Solo LEE el estado de los discos. No borra ni cambia nada.)
  echo.
  timeout /t 3 >nul 2>&1
  powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

echo.
echo   ============================================================
echo     LEE EL ESTADO (SMART) DE TODOS LOS DISCOS
echo   ============================================================
echo.
echo     Esto NO borra ni cambia nada: solo LEE el estado del disco.
echo     Lo que hace es encender el registro SMART si estuviera apagado.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0leer-smart.ps1"

echo.
pause
