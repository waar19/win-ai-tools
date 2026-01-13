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
from core.i18n import t


class SchedulerToggle(QFrame):
    """Toggle widget to enable/disable scheduled maintenance"""
    
    status_changed = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._refresh_status()
    
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
        
        title = QLabel("Auto-Maintenance")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #eaeaea;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        info_layout.addLayout(title_layout)
        
        desc = QLabel("Re-apply settings after Windows Updates (runs at startup & daily)")
        desc.setStyleSheet("font-size: 11px; color: #888;")
        desc.setWordWrap(True)
        info_layout.addWidget(desc)
        
        layout.addLayout(info_layout, 1)
        
        # Status indicator
        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        # Toggle button
        self.toggle_btn = QPushButton("Enable")
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
            self.status_label.setText("● Active")
            self.status_label.setStyleSheet("color: #4ade80; font-size: 12px;")
            self.toggle_btn.setText("Disable")
        else:
            self.status_label.setText("○ Inactive")
            self.status_label.setStyleSheet("color: #888; font-size: 12px;")
            self.toggle_btn.setText("Enable")
    
    def _on_toggle(self):
        """Handle toggle button click"""
        installed = is_task_installed()
        
        if installed:
            success, message = remove_task()
        else:
            success, message = create_task()
        
        self._refresh_status()
        self.status_changed.emit(is_task_installed())
    
    def is_enabled(self) -> bool:
        """Check if scheduled task is enabled"""
        return is_task_installed()
