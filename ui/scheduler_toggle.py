"""
Toggle widget for scheduled task settings
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
    QPushButton, QFrame, QCheckBox
)
from PyQt6.QtCore import pyqtSignal, Qt
import sys
sys.path.append('..')
from core.scheduler import is_task_installed, create_task, remove_task
from core.i18n import t, I18n


class SchedulerToggle(QFrame):
    """Toggle widget to enable/disable scheduled maintenance"""
    
    status_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._refresh_status()
        
        # Listen for language changes
        I18n.add_listener(self._on_language_changed)
    
    def _setup_ui(self):
        self.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icon and text
        info_layout = QVBoxLayout()
        
        title_layout = QHBoxLayout()
        icon = QLabel("⏰")
        icon.setStyleSheet("font-size: 18px;")
        title_layout.addWidget(icon)
        
        self.title_label = QLabel(t("auto_maintenance"))
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #eaeaea;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        info_layout.addLayout(title_layout)
        
        self.desc_label = QLabel(t("auto_maintenance_desc"))
        self.desc_label.setStyleSheet("font-size: 11px; color: #888;")
        self.desc_label.setWordWrap(True)
        info_layout.addWidget(self.desc_label)
        
        layout.addLayout(info_layout, 1)
        
        # Status indicator
        self.status_label = QLabel("...")
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        # Toggle button
        self.toggle_btn = QPushButton(t("enable"))
        self.toggle_btn.setFixedWidth(80)
        self.toggle_btn.clicked.connect(self._on_toggle)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #0f3460;
                color: #eaeaea;
                border: 1px solid #00d4ff;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #00d4ff;
                color: #1a1a2e;
            }
        """)
        layout.addWidget(self.toggle_btn)
    
    def _refresh_status(self):
        """Refresh the current status"""
        installed = is_task_installed()
        
        if installed:
            self.status_label.setText(t("scheduler_active"))
            self.status_label.setStyleSheet("color: #4ade80; font-size: 12px;")
            self.toggle_btn.setText(t("disable"))
        else:
            self.status_label.setText(t("scheduler_inactive"))
            self.status_label.setStyleSheet("color: #888; font-size: 12px;")
            self.toggle_btn.setText(t("enable"))
    
    def _on_toggle(self):
        """Handle toggle button click"""
        from PyQt6.QtWidgets import QMessageBox
        
        installed = is_task_installed()
        
        if installed:
            success, message = remove_task()
        else:
            success, message = create_task()
        
        if not success:
            # Check if it's a permissions issue
            if "access" in message.lower() or "denied" in message.lower():
                error_msg = t("scheduler_needs_admin")
            else:
                error_msg = message
                
            QMessageBox.warning(
                self,
                t("error_title"),
                error_msg
            )
        
        self._refresh_status()
        self.status_changed.emit(is_task_installed())
    
    def _on_language_changed(self):
        """Update UI when language changes"""
        self.title_label.setText(t("auto_maintenance"))
        self.desc_label.setText(t("auto_maintenance_desc"))
        self._refresh_status()
    
    def is_enabled(self) -> bool:
        """Check if scheduled task is enabled"""
        return is_task_installed()
