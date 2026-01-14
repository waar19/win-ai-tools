; Windows AI Removal Tool Installer Script
; Requires NSIS (Nullsoft Scriptable Install System)

;--------------------------------
;General

  ;Name and file
  Name "Windows AI Removal Tool"
  OutFile "WinAIRemovalTool_v1.3.0_win_x64_Setup.exe"
  Unicode True

  ;Default installation folder
  InstallDir "$PROGRAMFILES64\Windows AI Removal Tool"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKLM "Software\Windows AI Removal Tool" "Install_Dir"

  ;Request application privileges for Windows Vista+
  RequestExecutionLevel admin

  ;Icon
  Icon "app.ico"

;--------------------------------
;Interface Settings

  !include "MUI2.nsh"
  !include "LogicLib.nsh"

  !define MUI_ABORTWARNING
  !define MUI_ICON "app.ico"
  !define MUI_UNICON "app.ico"

  ;Pages
  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "LICENSE"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

  ;Languages
  !insertmacro MUI_LANGUAGE "English"
  !insertmacro MUI_LANGUAGE "Spanish"
  !insertmacro MUI_LANGUAGE "German"

;--------------------------------
;Installer Sections

Section "Windows AI Removal Tool (Required)" SecCore

  SectionIn RO
  
  ;Set output path to the installation directory.
  SetOutPath "$INSTDIR"
  
  ;Put file there
  File "dist\WinAIRemovalTool.exe"
  File "app.ico"
  File "README.md"
  File "LICENSE"
  
  ;Write the installation path into the registry
  WriteRegStr HKLM "SOFTWARE\Windows AI Removal Tool" "Install_Dir" "$INSTDIR"
  
  ;Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "DisplayName" "Windows AI Removal Tool"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "DisplayIcon" '"$INSTDIR\app.ico"'
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "Publisher" "WinAI Community"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "DisplayVersion" "1.3.0"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool" "NoRepair" 1
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\uninstall.exe"
  
SectionEnd

Section "Start Menu Shortcuts" SecStartMenu

  CreateDirectory "$SMPROGRAMS\Windows AI Removal Tool"
  CreateShortcut "$SMPROGRAMS\Windows AI Removal Tool\Windows AI Removal Tool.lnk" "$INSTDIR\WinAIRemovalTool.exe" "" "$INSTDIR\app.ico" 0
  CreateShortcut "$SMPROGRAMS\Windows AI Removal Tool\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  
SectionEnd

Section "Desktop Shortcut" SecDesktop

  CreateShortcut "$DESKTOP\Windows AI Removal Tool.lnk" "$INSTDIR\WinAIRemovalTool.exe" "" "$INSTDIR\app.ico" 0
  
SectionEnd

Section "Always Run as Administrator" SecRunAdmin
  
  ; Set compatibility flag to always run as administrator for current user
  WriteRegStr HKCU "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers" "$INSTDIR\WinAIRemovalTool.exe" "~ RUNASADMIN"
  
SectionEnd


;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecCore ${LANG_ENGLISH} "Core application files."
  LangString DESC_SecStartMenu ${LANG_ENGLISH} "Create shortcuts in Start Menu."
  LangString DESC_SecDesktop ${LANG_ENGLISH} "Create shortcut on Desktop."
  LangString DESC_SecRunAdmin ${LANG_ENGLISH} "Configure application to always run with Administrator privileges (recommended)."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} $(DESC_SecCore)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecRunAdmin} $(DESC_SecRunAdmin)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;Remove Registry Keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\WindowsAIRemovalTool"
  DeleteRegKey HKLM "SOFTWARE\Windows AI Removal Tool"

  ;Remove Files and Uninstaller
  Delete "$INSTDIR\WinAIRemovalTool.exe"
  Delete "$INSTDIR\app.ico"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\LICENSE"
  Delete "$INSTDIR\uninstall.exe"

  ;Remove Shortcuts
  Delete "$SMPROGRAMS\Windows AI Removal Tool\Windows AI Removal Tool.lnk"
  Delete "$SMPROGRAMS\Windows AI Removal Tool\Uninstall.lnk"
  RMDir "$SMPROGRAMS\Windows AI Removal Tool"
  Delete "$DESKTOP\Windows AI Removal Tool.lnk"
  
  ;Remove directories used
  RMDir "$INSTDIR"
  
SectionEnd
