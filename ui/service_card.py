"""
Widget to display an individual AI service
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt
import sys
sys.path.append('..')
from core.ai_services import AIService, ServiceStatus
from core.i18n import t


class ServiceCard(QFrame):
    """Card widget to display AI service information"""
    
    disable_clicked = pyqtSignal(str)  # service_id
    enable_clicked = pyqtSignal(str)   # service_id
    
    def __init__(self, service: AIService, parent=None):
        super().__init__(parent)
        self.service = service
        self.setObjectName("serviceCard")
        self._setup_ui()
        self.update_status(service.status)
    
    def _setup_ui(self):
        """Configure card interface"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header with name and status
        header_layout = QHBoxLayout()
        
        # Service name
        self.name_label = QLabel(self.service.name)
        self.name_label.setObjectName("serviceName")
        header_layout.addWidget(self.name_label)
        
        header_layout.addStretch()
        
        # Status
        self.status_label = QLabel(t("detecting_services"))
        header_layout.addWidget(self.status_label)
        
        layout.addLayout(header_layout)
        
        # Description
        desc_label = QLabel(self.service.description)
        desc_label.setObjectName("serviceDescription")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.enable_btn = QPushButton(t("enable"))
        self.enable_btn.setObjectName("success")
        self.enable_btn.clicked.connect(self._on_enable_clicked)
        button_layout.addWidget(self.enable_btn)
        
        self.disable_btn = QPushButton(t("disable"))
        self.disable_btn.setObjectName("danger")
        self.disable_btn.clicked.connect(self._on_disable_clicked)
        button_layout.addWidget(self.disable_btn)
        
        layout.addLayout(button_layout)
        
        self.setMinimumHeight(120)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    
    def update_status(self, status: ServiceStatus):
        """Update status visualization"""
        self.service.status = status
        
        if status == ServiceStatus.ENABLED:
            self.status_label.setText(t("status_enabled"))
            self.status_label.setObjectName("statusEnabled")
            self.disable_btn.setEnabled(True)
            self.enable_btn.setEnabled(False)
        elif status == ServiceStatus.DISABLED:
            self.status_label.setText(t("status_disabled"))
            self.status_label.setObjectName("statusDisabled")
            self.disable_btn.setEnabled(False)
            self.enable_btn.setEnabled(True)
        elif status == ServiceStatus.NOT_INSTALLED:
            self.status_label.setText(t("status_not_installed"))
            self.status_label.setObjectName("statusNotInstalled")
            self.disable_btn.setEnabled(False)
            self.enable_btn.setEnabled(False)
        else:
            self.status_label.setText(t("status_unknown"))
            self.status_label.setObjectName("statusDisabled")
            self.disable_btn.setEnabled(True)
            self.enable_btn.setEnabled(True)
        
        # Force style update
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
    
    def update_translations(self):
        """Update button texts when language changes"""
        self.enable_btn.setText(t("enable"))
        self.disable_btn.setText(t("disable"))
        # Re-apply status to update status text
        self.update_status(self.service.status)
    
    def _on_disable_clicked(self):
        """Emit signal to disable service"""
        self.disable_clicked.emit(self.service.id)
    
    def _on_enable_clicked(self):
        """Emit signal to enable service"""
        self.enable_clicked.emit(self.service.id)
