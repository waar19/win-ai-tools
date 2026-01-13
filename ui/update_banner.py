"""
Update notification banner widget
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal
import webbrowser


class UpdateBanner(QFrame):
    """Banner to show when an update is available"""
    
    dismissed = pyqtSignal()
    
    def __init__(self, version: str, download_url: str, parent=None):
        super().__init__(parent)
        self.download_url = download_url
        self._setup_ui(version)
    
    def _setup_ui(self, version: str):
        self.setObjectName("updateBanner")
        self.setStyleSheet("""
            #updateBanner {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f3460, stop:1 #16213e);
                border: 1px solid #00d4ff;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Icon
        icon_label = QLabel("🔔")
        icon_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(icon_label)
        
        # Message
        message = QLabel(f"New version <b>{version}</b> is available!")
        message.setStyleSheet("color: #eaeaea; font-size: 13px;")
        layout.addWidget(message)
        
        layout.addStretch()
        
        # Download button
        download_btn = QPushButton("⬇️ Download")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d4ff;
                color: #1a1a2e;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00b8e6;
            }
        """)
        download_btn.clicked.connect(self._on_download)
        layout.addWidget(download_btn)
        
        # Dismiss button
        dismiss_btn = QPushButton("✕")
        dismiss_btn.setFixedSize(24, 24)
        dismiss_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: #eaeaea;
            }
        """)
        dismiss_btn.clicked.connect(self._on_dismiss)
        layout.addWidget(dismiss_btn)
    
    def _on_download(self):
        """Open download URL in browser"""
        try:
            webbrowser.open(self.download_url)
        except:
            pass
    
    def _on_dismiss(self):
        """Hide the banner"""
        self.setVisible(False)
        self.dismissed.emit()
