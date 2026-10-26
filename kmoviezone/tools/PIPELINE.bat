@echo off
REM ==========================================================
REM  kmoviezone - PIPELINE (menu unico del operador)
REM  Todo el proceso desde un solo lugar.
REM ==========================================================
cd /d "%~dp0"
title kmoviezone - PIPELINE

:MENU
cls
echo ============================================================
echo   KMOVIEZONE - PIPELINE DEL OPERADOR
echo ============================================================
echo.
echo   [1] ENCOLAR enlaces      (lee cola-enlaces.txt - MiPony debe estar CERRADO)
echo   [2] Ver estado de la cola de MiPony
echo   [3] Exportar los detenidos para reintentar
echo.
echo   [4] COSECHAR enlaces  - VER    (no escribe nada)
echo   [5] COSECHAR enlaces  - AGREGAR al catalogo
echo.
echo   [6] Publicar  - regenerar datos.json
echo   [7] Publicar  - subir la web por FTP
echo.
echo   [8] Ver el PROCESO COMPLETO (paso a paso)
echo   [0] Salir
echo.
set /p OP=  Elija una opcion y pulse Enter: 

if "%OP%"=="1" goto ENCOLAR
if "%OP%"=="2" goto ESTADO
if "%OP%"=="3" goto PENDIENTES
if "%OP%"=="4" goto COSECHAR_VER
if "%OP%"=="5" goto COSECHAR_ADD
if "%OP%"=="6" goto REGENERAR
if "%OP%"=="7" goto SUBIR
if "%OP%"=="8" goto LEER
if "%OP%"=="0" exit /b
goto MENU

:ENCOLAR
cls
echo --- ENCOLAR EN MIPONY ---
echo.
tasklist | find /i "mipony" >nul && (
  echo *** MIPONY ESTA ABIERTO *** Cierrelo y vuelva a intentar.
  echo.
  pause
  goto MENU
)
python mipony.py encolar
echo.
pause
goto MENU

:ESTADO
cls
echo --- ESTADO DE LA COLA ---
echo.
python mipony.py estado
echo.
pause
goto MENU

:PENDIENTES
cls
echo --- EXPORTAR DETENIDOS ---
echo.
python mipony.py pendientes
echo.
echo   Re-encolados con la opcion [1] usando reintentar.txt
echo.
pause
goto MENU

:COSECHAR_VER
cls
echo --- COSECHAR (VER) ---
echo.
set /p TIT=  Titulo exacto: 
set /p TIP=  Tipo (pelicula/serie/anime/comics) [anime]: 
if "%TIP%"=="" set TIP=anime
set /p FIL=  Filtro (palabra que solo aparezca en esta tanda): 
echo.
python cosechar.py "%TIT%" --tipo %TIP% --filtro "%FIL%"
echo.
pause
goto MENU

:COSECHAR_ADD
cls
echo --- COSECHAR (AGREGAR A catalogo.csv) ---
echo.
set /p TIT=  Titulo exacto: 
set /p TIP=  Tipo (pelicula/serie/anime/comics) [anime]: 
if "%TIP%"=="" set TIP=anime
set /p FIL=  Filtro (palabra que solo aparezca en esta tanda): 
echo.
python cosechar.py "%TIT%" --tipo %TIP% --filtro "%FIL%" --csv
echo.
pause
goto MENU

:REGENERAR
cls
echo --- REGENERAR datos.json ---
echo.
python build.py
echo.
pause
goto MENU

:SUBIR
cls
echo --- SUBIR LA WEB POR FTP ---
echo.
call SUBIR_WEB.bat
goto MENU

:LEER
cls
echo Abriendo el proceso completo...
start "" PROCESO-COMPLETO.md
echo.
pause
goto MENU