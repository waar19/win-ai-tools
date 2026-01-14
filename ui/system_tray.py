"""
System Tray Icon for Windows AI Removal Tool
"""

from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal
import os
from core.i18n import t
import core.autostart as autostart

class SystemTrayIcon(QSystemTrayIcon):
    """System tray icon with context menu"""
    
    # Signals
    show_window = pyqtSignal()
    run_maintenance = pyqtSignal()
    quit_app = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_icon()
        self._setup_menu()
        
        # Connect activation (double click/single click)
        self.activated.connect(self._on_activated)
        
    def _setup_icon(self):
        """Load and set icon"""
        # Try to load app.ico from root or ui folder
        root_dir = os.path.dirname(os.path.dirname(__file__))
        icon_path = os.path.join(root_dir, 'app.ico')
        
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        else:
            # Fallback to a standard icon if missing (or rely on window icon)
            self.setIcon(QIcon.fromTheme("system-help"))
            
        self.setToolTip(t("app_title"))
        
    def _setup_menu(self):
        """Create context menu"""
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #16213e;
                color: #eaeaea;
                border: 1px solid #0f3460;
            }
            QMenu::item {
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #0f3460;
            }
        """)
        
        # Open Dashboard
        self.open_action = QAction(t("tray_open"), menu)
        self.open_action.triggered.connect(self.show_window.emit)
        menu.addAction(self.open_action)
        
        menu.addSeparator()
        
        # Start with Windows
        self.autostart_action = QAction(t("tray_start_with_windows"), menu)
        self.autostart_action.setCheckable(True)
        self.autostart_action.setChecked(autostart.is_autostart_enabled())
        self.autostart_action.triggered.connect(self._toggle_autostart)
        menu.addAction(self.autostart_action)
        
        menu.addSeparator()
        
        # Quit
        self.quit_action = QAction(t("tray_quit"), menu)
        self.quit_action.triggered.connect(self.quit_app.emit)
        menu.addAction(self.quit_action)
        
        self.setContextMenu(menu)
        
    def _toggle_autostart(self, checked):
        """Toggle auto-start setting"""
        success, message = autostart.set_autostart(checked)
        
        if success:
            self.showMessage(
                t("app_title"),
                message,
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            # Revert state on failure
            self.autostart_action.setChecked(not checked)
            self.showMessage(
                t("error_title"),
                message,
                QSystemTrayIcon.MessageIcon.Warning,
                3000
            )
        
    def _on_activated(self, reason):
        """Handle tray icon click"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger or \
           reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window.emit()
            
    def update_tooltip(self, text):
        """Update hover text"""
        self.setToolTip(f"{t('app_title')}\n{text}")
