@echo off
title SEAWOLF TOOLS - servidor + tunel
setlocal
cd /d "%~dp0"

echo ================================================================
echo    SEAWOLF TOOLS  -  servidor local + tunel del dominio
echo ================================================================
echo.
echo    Local    :  http://localhost:8770
echo    Dominio  :  https://herramientas.sw-st.net
echo.
echo    Sin la clave de acceso NO se entra (ni local ni por dominio).
echo    Ver la clave:   python intel\seawolf-tools.py clave
echo.
echo ================================================================
echo.

REM ---- 1) El aplicativo (escaneo de discos, sin abrir navegador) ----
start "Seawolf Tools" /min cmd /c python "%~dp0intel\seawolf-tools.py" serve ALL --port 8770 --no-open

REM ---- 2) El tunel que publica el dominio ----
start "Seawolf Tunel" /min cmd /c "%~dp0tools\cloudflared.exe" tunnel --config "%USERPROFILE%\.cloudflared\seawolf-tools.yml" run seawolf-tools

echo  Ambos arrancados en segundo plano.
echo  (quedan 2 ventanas minimizadas: "Seawolf Tools" y "Seawolf Tunel")
echo.
echo  Esperando 8 segundos a que levanten...
ping -n 9 127.0.0.1 >nul
echo.
echo  LISTO. Abra:  https://herramientas.sw-st.net
echo.
