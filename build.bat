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
    
    REM Chequear si makensis (NSIS) esta disponible
    where makensis >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Compilando instalador NSIS...
        makensis installer.nsi
        if %ERRORLEVEL% EQU 0 (
            echo INSTALADOR CREADO EXITOSAMENTE: Setup_WinAIRemovalTool_v1.2.0.exe
        ) else (
            echo Error al compilar el instalador.
        )
    ) else (
        echo.
        echo Nota: NSIS no encontrado en PATH. No se genero el instalador.
        echo Para generar el setup, instale NSIS y agreguelo al PATH.
    )

    echo Este archivo solicitara permisos de
    echo administrador automaticamente al ejecutar.
) else (
    echo BUILD FALLIDO
    echo Revise los errores anteriores.
)
echo ========================================
pause
