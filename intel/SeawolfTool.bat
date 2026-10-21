@echo off
REM Seawolf Tools - Optimizacion de disco (lanzador)
REM Lee TODOS los discos accesibles (ALL). Doble clic y listo.
setlocal
set JAVA_HOME=D:\jdk21\jdk-21.0.12.1+1
set GHIDRA_INSTALL_DIR=D:\ghidra\ghidra_12.1.4_PUBLIC
echo ============================================
echo   SEAWOLF TOOLS - Optimizacion de disco
echo   Escaneando TODOS los discos accesibles...
echo ============================================
python "%~dp0seawolf-tools.py" serve ALL --port 8770
pause
