"""
Widget para mostrar el log de actividad
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QPushButton
)
from PyQt6.QtCore import Qt
import sys
sys.path.append('..')
from core.logger import activity_logger, LogEntry


class LogEntryWidget(QFrame):
    """Widget para mostrar una entrada individual del log"""
    
    def __init__(self, entry: LogEntry, parent=None):
        super().__init__(parent)
        self._setup_ui(entry)
    
    def _setup_ui(self, entry: LogEntry):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Ícono según nivel
        icon_map = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        icon = icon_map.get(entry.level, "•")
        
        icon_label = QLabel(icon)
        icon_label.setFixedWidth(25)
        layout.addWidget(icon_label)
        
        # Timestamp
        time_label = QLabel(entry.timestamp.split(" ")[1] if " " in entry.timestamp else entry.timestamp)
        time_label.setStyleSheet("color: #666; font-size: 11px;")
        time_label.setFixedWidth(70)
        layout.addWidget(time_label)
        
        # Acción
        action_colors = {
            "DISABLE": "#e94560",
            "ENABLE": "#4ade80",
            "BACKUP": "#00d4ff",
            "RESTORE": "#fbbf24",
            "DETECTION": "#888"
        }
        action_label = QLabel(entry.action)
        action_label.setStyleSheet(f"color: {action_colors.get(entry.action, '#888')}; font-weight: bold; font-size: 11px;")
        action_label.setFixedWidth(80)
        layout.addWidget(action_label)
        
        # Servicio
        service_label = QLabel(entry.service_name)
        service_label.setStyleSheet("color: #aaa; font-size: 12px;")
        service_label.setFixedWidth(150)
        layout.addWidget(service_label)
        
        # Mensaje
        message_label = QLabel(entry.message)
        message_label.setStyleSheet("color: #eaeaea; font-size: 12px;")
        message_label.setWordWrap(True)
        layout.addWidget(message_label, 1)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 4px;
                margin: 2px 0;
            }
        """)


class LogViewerWidget(QWidget):
    """Panel de visualización del log de actividad"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self.refresh()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("📋 Log de Actividad")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00d4ff;")
        header.addWidget(title)
        
        header.addStretch()
        
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(30, 30)
        refresh_btn.clicked.connect(self.refresh)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #16213e;
                border: 1px solid #0f3460;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0f3460;
            }
        """)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # Scroll area para las entradas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1a1a2e;
                border: 1px solid #0f3460;
                border-radius: 8px;
            }
        """)
        
        self.entries_container = QWidget()
        self.entries_layout = QVBoxLayout(self.entries_container)
        self.entries_layout.setContentsMargins(5, 5, 5, 5)
        self.entries_layout.setSpacing(3)
        self.entries_layout.addStretch()
        
        scroll_area.setWidget(self.entries_container)
        layout.addWidget(scroll_area)
    
    def refresh(self):
        """Actualiza las entradas del log"""
        # Limpiar entradas anteriores
        while self.entries_layout.count() > 1:
            item = self.entries_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Obtener entradas
        entries = activity_logger.get_entries(limit=50)
        
        if not entries:
            empty_label = QLabel("Sin actividad registrada")
            empty_label.setStyleSheet("color: #666; font-style: italic; padding: 20px;")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.entries_layout.insertWidget(0, empty_label)
        else:
            for entry in entries:
                widget = LogEntryWidget(entry)
                self.entries_layout.insertWidget(self.entries_layout.count() - 1, widget)
