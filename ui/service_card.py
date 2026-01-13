"""
Widget para mostrar un servicio AI individual
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt
import sys
sys.path.append('..')
from core.ai_services import AIService, ServiceStatus


class ServiceCard(QFrame):
    """Widget card para mostrar información de un servicio AI"""
    
    disable_clicked = pyqtSignal(str)  # service_id
    enable_clicked = pyqtSignal(str)   # service_id
    
    def __init__(self, service: AIService, parent=None):
        super().__init__(parent)
        self.service = service
        self.setObjectName("serviceCard")
        self._setup_ui()
        self.update_status(service.status)
    
    def _setup_ui(self):
        """Configura la interfaz del card"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header con nombre y estado
        header_layout = QHBoxLayout()
        
        # Nombre del servicio
        self.name_label = QLabel(self.service.name)
        self.name_label.setObjectName("serviceName")
        header_layout.addWidget(self.name_label)
        
        header_layout.addStretch()
        
        # Estado
        self.status_label = QLabel("Detectando...")
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Descripción
        desc_label = QLabel(self.service.description)
        desc_label.setObjectName("serviceDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Botones de acción
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.enable_btn = QPushButton("Habilitar")
        self.enable_btn.setObjectName("success")
        self.enable_btn.clicked.connect(self._on_enable_clicked)
        button_layout.addWidget(self.enable_btn)
        
        self.disable_btn = QPushButton("Deshabilitar")
        self.disable_btn.setObjectName("danger")
        self.disable_btn.clicked.connect(self._on_disable_clicked)
        button_layout.addWidget(self.disable_btn)
        
        layout.addLayout(button_layout)
        
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    
    def update_status(self, status: ServiceStatus):
        """Actualiza la visualización del estado"""
        self.service.status = status
        
        if status == ServiceStatus.ENABLED:
            self.status_label.setText("● Activo")
            self.status_label.setObjectName("statusEnabled")
            self.disable_btn.setEnabled(True)
            self.enable_btn.setEnabled(False)
        elif status == ServiceStatus.DISABLED:
            self.status_label.setText("○ Deshabilitado")
            self.status_label.setObjectName("statusDisabled")
            self.disable_btn.setEnabled(False)
            self.enable_btn.setEnabled(True)
        elif status == ServiceStatus.NOT_INSTALLED:
            self.status_label.setText("✗ No instalado")
            self.status_label.setObjectName("statusNotInstalled")
            self.disable_btn.setEnabled(False)
            self.enable_btn.setEnabled(False)
        else:
            self.status_label.setText("? Desconocido")
            self.status_label.setObjectName("statusDisabled")
            self.disable_btn.setEnabled(True)
            self.enable_btn.setEnabled(True)
        
        # Forzar actualización de estilos
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
    
    def _on_disable_clicked(self):
        """Emite señal para deshabilitar el servicio"""
        self.disable_clicked.emit(self.service.id)
    
    def _on_enable_clicked(self):
        """Emite señal para habilitar el servicio"""
        self.enable_clicked.emit(self.service.id)
