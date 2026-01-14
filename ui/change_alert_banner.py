"""
Change Alert Banner Widget
Shows alert when AI services have been modified (e.g., by Windows Update)
"""

from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import pyqtSignal

from core.i18n import t
from core.change_monitor import ChangeReport


class ChangeAlertBanner(QFrame):
    """
    Banner that appears when changes are detected in AI service settings.
    Provides options to restore, accept, or dismiss the alert.
    """
    
    # Signals
    restore_clicked = pyqtSignal()
    accept_clicked = pyqtSignal()
    dismiss_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._apply_styles()
        self.hide()  # Hidden by default
    
    def _setup_ui(self):
        """Setup the banner UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Left side: Icon and message
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)
        
        self.title_label = QLabel(t("changes_detected"))
        self.title_label.setObjectName("alert_title")
        
        self.message_label = QLabel("")
        self.message_label.setObjectName("alert_message")
        self.message_label.setWordWrap(True)
        
        left_layout.addWidget(self.title_label)
        left_layout.addWidget(self.message_label)
        
        layout.addLayout(left_layout, stretch=1)
        
        # Right side: Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        self.restore_btn = QPushButton(t("restore_settings"))
        self.restore_btn.setObjectName("restore_btn")
        self.restore_btn.clicked.connect(self.restore_clicked.emit)
        
        self.accept_btn = QPushButton(t("accept_changes"))
        self.accept_btn.setObjectName("accept_btn")
        self.accept_btn.clicked.connect(self.accept_clicked.emit)
        
        self.dismiss_btn = QPushButton(t("dismiss"))
        self.dismiss_btn.setObjectName("dismiss_btn")
        self.dismiss_btn.clicked.connect(self._on_dismiss)
        
        button_layout.addWidget(self.restore_btn)
        button_layout.addWidget(self.accept_btn)
        button_layout.addWidget(self.dismiss_btn)
        
        layout.addLayout(button_layout)
    
    def _apply_styles(self):
        """Apply styles to the banner"""
        self.setStyleSheet("""
            ChangeAlertBanner {
                background-color: #2d1f1f;
                border: 1px solid #e53935;
                border-radius: 8px;
            }
            
            #alert_title {
                color: #ffab91;
                font-size: 14px;
                font-weight: bold;
            }
            
            #alert_message {
                color: #e0e0e0;
                font-size: 12px;
            }
            
            #restore_btn {
                background-color: #e53935;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            #restore_btn:hover {
                background-color: #f44336;
            }
            
            #accept_btn {
                background-color: #0f3460;
                color: white;
                border: 1px solid #1e5f74;
                padding: 8px 16px;
                border-radius: 4px;
            }
            
            #accept_btn:hover {
                background-color: #1e5f74;
            }
            
            #dismiss_btn {
                background-color: transparent;
                color: #999;
                border: 1px solid #333;
                padding: 8px 12px;
                border-radius: 4px;
            }
            
            #dismiss_btn:hover {
                background-color: #333;
                color: #fff;
            }
        """)
    
    def show_alert(self, report: ChangeReport):
        """
        Show the alert banner with information about detected changes.
        """
        if report.is_empty:
            self.hide()
            return
        
        # Build message
        if report.has_reenabled_services:
            services = [c.service_name for c in report.changes if c.was_reenabled]
            service_list = ", ".join(services[:3])
            if len(services) > 3:
                service_list += f" (+{len(services) - 3} more)"
            
            message = t("services_reenabled", count=report.reenabled_count)
            message += f"\n{service_list}"
        else:
            message = f"{report.total_changes} service(s) changed since last check."
        
        self.message_label.setText(message)
        self.show()
    
    def _on_dismiss(self):
        """Handle dismiss button click"""
        self.hide()
        self.dismiss_clicked.emit()
    
    def update_translations(self):
        """Update text when language changes"""
        self.title_label.setText(t("changes_detected"))
        self.restore_btn.setText(t("restore_settings"))
        self.accept_btn.setText(t("accept_changes"))
        self.dismiss_btn.setText(t("dismiss"))
