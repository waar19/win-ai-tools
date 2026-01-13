# Windows AI Removal Tool

<p align="center">
  <img src="app.ico" alt="Windows AI Removal Tool" width="128" height="128">
</p>

A desktop application to manage and remove AI services from Windows 11. Take control of your privacy by disabling Copilot, Recall, and other AI integrations.

## ✨ Features

- 🤖 **Detect AI Services** - Automatically scans for 11 different AI integrations
- ⚡ **Enable/Disable** - Toggle individual services on or off
- 🚫 **Disable All** - One-click to disable all AI services
- 💾 **Backup & Restore** - Create backups before making changes
- 📋 **Activity Log** - Track all changes with persistent logging
- 🎨 **Modern UI** - Dark theme with intuitive interface

## 🤖 Supported AI Services

| Service | Description |
|---------|-------------|
| Microsoft Copilot | Windows 11 AI assistant with Bing Chat |
| Windows Recall | AI-powered screenshot timeline (Copilot+ PCs) |
| AI Explorer | AI exploration features in Windows |
| Bing Search | Web search integration in Start Menu |
| Web Search | AI suggestions in taskbar search |
| Windows Widgets | AI-personalized news widgets |
| Cortana (Legacy) | Voice assistant |
| Edge Copilot | Copilot sidebar in Microsoft Edge |
| AI Voice Typing | Enhanced voice dictation |
| Suggested Actions | AI-suggested actions when copying text |

## 📥 Installation

### Option 1: Download Release (Recommended)
1. Go to [Releases](https://github.com/waar19/win-ai-tools/releases)
2. Download `WinAIRemovalTool.exe`
3. Run as Administrator

### Option 2: Run from Source
```bash
# Clone the repository
git clone https://github.com/waar19/win-ai-tools.git
cd win-ai-tools

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🔨 Building from Source

### Prerequisites
- Python 3.10+
- pip

### Build Steps

```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller pillow

# Build the executable
pyinstaller --clean app.spec

# The executable will be in dist/WinAIRemovalTool.exe
```

Or use the build script:
```cmd
build.bat
```

### Build Output
- `dist/WinAIRemovalTool.exe` - Standalone executable (~35 MB)
- Includes Python runtime and all dependencies
- Automatically requests Administrator privileges

## 🛡️ How It Works

The application modifies Windows settings through:

1. **Registry Keys** - Modifies `HKEY_LOCAL_MACHINE` and `HKEY_CURRENT_USER` policies
2. **Appx Packages** - Removes Microsoft AI-related packages
3. **Windows Features** - Disables optional Windows features like Recall

All changes are reversible through the backup/restore functionality.

## ⚠️ Important Notes

- **Run as Administrator** - Required to modify system settings
- **Create Backup First** - Always backup before making changes
- **Windows Updates** - Some settings may reset after major Windows updates
- **SmartScreen Warning** - Windows may show a warning for unsigned executables

## 📁 Project Structure

```
win-ai-tools/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── app.spec            # PyInstaller configuration
├── app.manifest        # Windows UAC manifest
├── app.ico             # Application icon
├── build.bat           # Build script
├── CHANGELOG.md        # Version history
├── core/               # Core logic
│   ├── ai_services.py  # AI service definitions
│   ├── detector.py     # Service detection
│   ├── manager.py      # Enable/disable logic
│   └── logger.py       # Activity logging
└── ui/                 # User interface
    ├── main_window.py  # Main window
    ├── service_card.py # Service card widget
    ├── log_viewer.py   # Activity log panel
    └── styles.py       # Dark theme styles
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Packaged with [PyInstaller](https://pyinstaller.org/)
- Inspired by the need for user control over AI integrations in Windows 11
