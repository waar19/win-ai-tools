@echo off
echo ========================================
echo  Windows AI Removal Tool - Build Script
echo ========================================
echo.

REM Verificar si PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Instalando PyInstaller...
    pip install pyinstaller
)

echo.
echo Compilando ejecutable...
echo.

pyinstaller --clean app.spec

echo.
echo ========================================
if exist "dist\WinAIRemovalTool.exe" (
    echo BUILD EXITOSO!
    echo.
    echo El ejecutable se encuentra en:
    echo   dist\WinAIRemovalTool.exe
    echo.
    echo Este archivo solicitara permisos de
    echo administrador automaticamente al ejecutar.
) else (
    echo BUILD FALLIDO
    echo Revise los errores anteriores.
)
echo ========================================
pause
