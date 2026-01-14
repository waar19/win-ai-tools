# Changelog

All notable changes to this project are documented here.

## [v1.3.0] - 2026-01-14

### ✨ New Features

- 🔍 **Change Monitor**: Detects when Windows Updates re-enable AI services and notifies the user
- 🔔 **Alert Banner**: Visual notification in the app when settings have been modified
- ↩️ **One-Click Restore**: Quickly restore your previous settings with a single button
- ✅ **Accept Changes**: Option to accept new state as baseline if desired
- 🤖 **Auto-Restore Mode**: New `--auto-restore` flag for completely automatic restoration:
  ```bash
  WinAIRemovalTool.exe --silent --auto-restore
  ```
- 📸 **State Snapshots**: Automatically saves your preferences to detect future changes

### 🔧 Improvements

- Silent mode now intelligently compares current state vs saved preferences
- System tray notifications when changes are detected
- Better logging of change detection and restoration events

---

## [v1.2.0] - 2026-01-14

### ✨ New Features

- 🎯 **Configuration Presets**: One-click presets for Privacy Mode, Balanced, and Gaming mode
- ⏰ **Scheduled Maintenance**: Automatically re-apply settings after Windows Updates
- 🚀 **Start with Windows**: Option to launch app at system startup
- 🔔 **System Tray**: Minimize to tray with quick access menu
- 📤 **Export/Import**: Share configurations between computers
- 🔄 **Auto-update checker**: Get notified when new versions are available

### 🚀 Performance Improvements

- ⚡ Asynchronous loading of services (no UI freeze)
- 🧵 Background thread for detection and actions
- 🎨 Smoother UI transitions

### 📦 Build & Distribution

- 🛠️ **NSIS Installer**: Professional Windows installer with Start Menu and Desktop shortcuts
- 📁 **Portable ZIP**: Standalone portable version
- 🤖 **GitHub Actions**: Automated builds include both installer and portable versions

### 🐛 Bug Fixes

- Fixed UI lag when switching between sections
- Improved error handling for registry operations

---

## [v1.1.0] - 2026-01-13

### ✨ New Features

- 🌍 **Multi-language support**: English, German (Deutsch), Spanish (Español)
- 🔄 **Language selector** in the top-right corner
- 🖥️ **Automatic system language detection**
- ⚡ **Real-time language switching** without restart

---

## [v1.0.0] - 2026-01-13

### 🎉 Initial Release

#### Features

- ✨ Modern dark-themed GUI (PyQt6)
- 🤖 Detection of 11 Windows 11 AI services:
  - Microsoft Copilot
  - Windows Recall
  - AI Explorer
  - Bing Search in Start Menu
  - Web Search in Taskbar
  - Windows Widgets (AI News)
  - Cortana (Legacy)
  - Edge Copilot Sidebar
  - AI Voice Typing
  - Suggested Actions
- ⚡ Enable/Disable services individually
- 🚫 One-click disable all services
- 💾 Backup system before modifications
- ↩️ Restore from backups
- 📋 Persistent activity log
- 🛡️ Automatic administrator privilege request
- 🌍 Multi-language support (English, German, Spanish)

#### Technical

- Standalone executable (.exe) - No Python required
- Registry modification to disable services
- Appx package removal when applicable
- Custom application icon
- GitHub Actions automated builds
