# Changelog

All notable changes to this project are documented here.

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
