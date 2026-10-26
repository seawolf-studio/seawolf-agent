@echo off
REM ============================================
REM  kmoviezone - DESCUBRIR (herramienta de operador)
REM  Doble clic -> abre el navegador en localhost
REM  Busca por titulo o por año y agrega al catalogo.
REM ============================================
cd /d "%~dp0"
title kmoviezone - DESCUBRIR (cierra esta ventana para detener)
python descubrir.py
pause
