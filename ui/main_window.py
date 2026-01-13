"""
Ventana principal de la aplicación
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame,
    QMessageBox, QProgressBar, QApplication, QTabWidget, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon

import sys
import os
sys.path.append('..')

from .styles import DARK_THEME
from .service_card import ServiceCard
from .log_viewer import LogViewerWidget
from core.detector import AIServiceDetector
from core.manager import AIServiceManager
from core.ai_services import AIService, ServiceStatus
from core.logger import activity_logger


class DetectionWorker(QThread):
    """Worker thread para detectar servicios sin bloquear UI"""
    finished = pyqtSignal(list)
    
    def __init__(self, detector: AIServiceDetector):
        super().__init__()
        self.detector = detector
    
    def run(self):
        services = self.detector.detect_all()
        self.finished.emit(services)


class ActionWorker(QThread):
    """Worker thread para ejecutar acciones sin bloquear UI"""
    finished = pyqtSignal(bool, str)
    
    def __init__(self, action: str, manager: AIServiceManager, service: AIService):
        super().__init__()
        self.action = action
        self.manager = manager
        self.service = service
    
    def run(self):
        if self.action == "disable":
            success, message = self.manager.disable_service(self.service)
        else:
            success, message = self.manager.enable_service(self.service)
        self.finished.emit(success, message)


class MainWindow(QMainWindow):
    """Ventana principal de Windows AI Removal Tool"""
    
    def __init__(self):
        super().__init__()
        self.detector = AIServiceDetector()
        self.manager = AIServiceManager()
        self.service_cards = {}
        self.current_worker = None
        
        self._setup_window()
        self._setup_ui()
        self._apply_styles()
        self._start_detection()
    
    def _setup_window(self):
        """Configura propiedades de la ventana"""
        self.setWindowTitle("Windows AI Removal Tool")
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)
        
        # Intentar cargar el ícono
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_ui(self):
        """Configura la interfaz de usuario"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QVBoxLayout()
        
        title = QLabel("🤖 Windows AI Removal Tool")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Gestiona y remueve servicios de Inteligencia Artificial de Windows 11")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addLayout(header_layout)
        
        # Barra de progreso (oculta inicialmente)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminado
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Detectando servicios AI...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Splitter principal con servicios y log
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo: Scroll area para los servicios
        services_panel = QWidget()
        services_layout = QVBoxLayout(services_panel)
        services_layout.setContentsMargins(0, 0, 0, 0)
        
        services_header = QLabel("🛡️ Servicios AI Detectados")
        services_header.setStyleSheet("font-size: 14px; font-weight: bold; color: #00d4ff; padding: 5px;")
        services_layout.addWidget(services_header)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.services_container = QWidget()
        self.services_layout = QVBoxLayout(self.services_container)
        self.services_layout.setSpacing(10)
        self.services_layout.addStretch()
        
        scroll_area.setWidget(self.services_container)
        services_layout.addWidget(scroll_area)
        
        splitter.addWidget(services_panel)
        
        # Panel derecho: Log viewer
        self.log_viewer = LogViewerWidget()
        splitter.addWidget(self.log_viewer)
        
        # Proporciones del splitter (60% servicios, 40% log)
        splitter.setSizes([600, 400])
        
        main_layout.addWidget(splitter, 1)
        
        # Footer con botones globales
        footer_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self._start_detection)
        footer_layout.addWidget(refresh_btn)
        
        footer_layout.addStretch()
        
        backup_btn = QPushButton("💾 Crear Backup")
        backup_btn.clicked.connect(self._create_backup)
        footer_layout.addWidget(backup_btn)
        
        restore_btn = QPushButton("↩️ Restaurar")
        restore_btn.clicked.connect(self._restore_backup)
        footer_layout.addWidget(restore_btn)
        
        footer_layout.addStretch()
        
        disable_all_btn = QPushButton("🚫 Deshabilitar Todo")
        disable_all_btn.setObjectName("danger")
        disable_all_btn.clicked.connect(self._disable_all)
        footer_layout.addWidget(disable_all_btn)
        
        main_layout.addLayout(footer_layout)
    
    def _apply_styles(self):
        """Aplica los estilos CSS"""
        self.setStyleSheet(DARK_THEME)
    
    def _start_detection(self):
        """Inicia la detección de servicios en background"""
        self.progress_bar.setVisible(True)
        self.status_label.setText("Detectando servicios AI...")
        
        self.detection_worker = DetectionWorker(self.detector)
        self.detection_worker.finished.connect(self._on_detection_finished)
        self.detection_worker.start()
    
    def _on_detection_finished(self, services):
        """Callback cuando termina la detección"""
        self.progress_bar.setVisible(False)
        
        # Limpiar cards anteriores
        for card in self.service_cards.values():
            card.deleteLater()
        self.service_cards.clear()
        
        # Crear nuevos cards y loggear detección
        for service in services:
            card = ServiceCard(service)
            card.disable_clicked.connect(self._on_disable_service)
            card.enable_clicked.connect(self._on_enable_service)
            
            # Insertar antes del stretch
            self.services_layout.insertWidget(
                self.services_layout.count() - 1, 
                card
            )
            self.service_cards[service.id] = card
            
            # Log de detección
            activity_logger.log_detection(service.id, service.name, service.status.value)
        
        enabled_count = sum(1 for s in services if s.status == ServiceStatus.ENABLED)
        self.status_label.setText(
            f"Encontrados {len(services)} servicios AI • {enabled_count} activos"
        )
        
        # Actualizar log viewer
        self.log_viewer.refresh()
    
    def _on_disable_service(self, service_id: str):
        """Maneja click en deshabilitar servicio"""
        if self.current_worker and self.current_worker.isRunning():
            return
        
        service = next((s for s in self.detector.services if s.id == service_id), None)
        if not service:
            return
        
        # Confirmar acción
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"¿Desea deshabilitar {service.name}?\n\nEsto modificará configuraciones del sistema.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self._run_action("disable", service)
    
    def _on_enable_service(self, service_id: str):
        """Maneja click en habilitar servicio"""
        if self.current_worker and self.current_worker.isRunning():
            return
        
        service = next((s for s in self.detector.services if s.id == service_id), None)
        if not service:
            return
        
        self._run_action("enable", service)
    
    def _run_action(self, action: str, service: AIService):
        """Ejecuta una acción en background"""
        self.progress_bar.setVisible(True)
        self.status_label.setText(
            f"{'Deshabilitando' if action == 'disable' else 'Habilitando'} {service.name}..."
        )
        
        self.current_worker = ActionWorker(action, self.manager, service)
        self.current_worker.finished.connect(
            lambda success, msg: self._on_action_finished(success, msg, service, action)
        )
        self.current_worker.start()
    
    def _on_action_finished(self, success: bool, message: str, service: AIService, action: str):
        """Callback cuando termina una acción"""
        self.progress_bar.setVisible(False)
        
        # Loggear la acción
        if action == "disable":
            activity_logger.log_disable(service.id, service.name, success, message)
        else:
            activity_logger.log_enable(service.id, service.name, success, message)
        
        if success:
            self.status_label.setText(f"✓ {message}")
            # Actualizar estado del card
            updated_service = self.detector.refresh_service(service.id)
            if updated_service and service.id in self.service_cards:
                self.service_cards[service.id].update_status(updated_service.status)
        else:
            self.status_label.setText(f"✗ Error: {message}")
            QMessageBox.warning(self, "Error", message)
        
        # Actualizar log viewer
        self.log_viewer.refresh()
    
    def _create_backup(self):
        """Crea backup de configuraciones actuales"""
        success, result = self.manager.create_backup(self.detector.services)
        
        # Loggear backup
        activity_logger.log_backup(success, result)
        
        if success:
            QMessageBox.information(
                self,
                "Backup Creado",
                f"Backup guardado en:\n{result}"
            )
        else:
            QMessageBox.warning(self, "Error", f"No se pudo crear backup: {result}")
        
        self.log_viewer.refresh()
    
    def _restore_backup(self):
        """Restaura desde el último backup"""
        backups = self.manager.get_backups()
        
        if not backups:
            QMessageBox.information(
                self,
                "Sin Backups",
                "No hay backups disponibles para restaurar."
            )
            return
        
        # Usar el backup más reciente
        latest = backups[0]
        
        reply = QMessageBox.question(
            self,
            "Confirmar Restauración",
            f"¿Desea restaurar desde el backup del {latest['timestamp']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        success, message = self.manager.restore_backup(latest['path'])
        
        # Loggear restauración
        activity_logger.log_restore(success, message)
        
        if success:
            QMessageBox.information(self, "Restaurado", message)
            self._start_detection()  # Refrescar estados
        else:
            QMessageBox.warning(self, "Error", f"Error restaurando: {message}")
        
        self.log_viewer.refresh()
    
    def _disable_all(self):
        """Deshabilita todos los servicios AI"""
        enabled_services = [
            s for s in self.detector.services 
            if s.status == ServiceStatus.ENABLED
        ]
        
        if not enabled_services:
            QMessageBox.information(
                self,
                "Información",
                "No hay servicios activos para deshabilitar."
            )
            return
        
        reply = QMessageBox.warning(
            self,
            "⚠️ Confirmar",
            f"¿Está seguro de deshabilitar TODOS los {len(enabled_services)} servicios AI?\n\n"
            "Se recomienda crear un backup primero.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Crear backup automático primero
        self.manager.create_backup(self.detector.services)
        activity_logger.log_backup(True, "Auto-backup antes de deshabilitar todo")
        
        # Deshabilitar todos
        self.progress_bar.setVisible(True)
        success_count = 0
        
        for service in enabled_services:
            self.status_label.setText(f"Deshabilitando {service.name}...")
            QApplication.processEvents()
            
            success, message = self.manager.disable_service(service)
            activity_logger.log_disable(service.id, service.name, success, message)
            
            if success:
                success_count += 1
        
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"✓ Deshabilitados {success_count}/{len(enabled_services)} servicios")
        
        # Refrescar estados y log
        self._start_detection()
        self.log_viewer.refresh()
