@echo off
REM Seawolf Tools - Optimizacion de disco (lanzador)
REM Doble clic para abrir el aplicativo en el navegador.
setlocal
set JAVA_HOME=D:\jdk21\jdk-21.0.12.1+1
set GHIDRA_INSTALL_DIR=D:\ghidra\ghidra_12.1.4_PUBLIC
echo ============================================
echo   SEAWOLF TOOLS - Optimizacion de disco
echo   Abriendo aplicativo en el navegador...
echo ============================================
python "%~dp0seawolf-tools.py" serve "C:\Users\Admin" --port 8770
pause
