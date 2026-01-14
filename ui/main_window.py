"""
Main application window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame,
    QMessageBox, QProgressBar, QApplication, QSplitter,
    QFileDialog, QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

import sys
import os
sys.path.append('..')

from .styles import DARK_THEME
from .service_card import ServiceCard
from .log_viewer import LogViewerWidget
from .language_selector import LanguageSelector
from .update_banner import UpdateBanner
from .scheduler_toggle import SchedulerToggle
from .system_tray import SystemTrayIcon # Added import
from core.detector import AIServiceDetector
from core.manager import AIServiceManager
from core.ai_services import AIService, ServiceStatus
from core.logger import activity_logger
from core.i18n import I18n, t
from core.persistence import ConfigPersistence
from core.updater import UpdateChecker, UpdateInfo


class DetectionWorker(QThread):
    """Worker thread to detect services without blocking UI"""
    finished = pyqtSignal(list)
    
    def __init__(self, detector: AIServiceDetector):
        super().__init__()
        self.detector = detector
    
    def run(self):
        services = self.detector.detect_all()
        self.finished.emit(services)


class ActionWorker(QThread):
    """Worker thread to execute actions without blocking UI"""
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
    """Main window of Windows AI Removal Tool"""
    
    def __init__(self):
        super().__init__()
        self.detector = AIServiceDetector()
        self.manager = AIServiceManager()
        self.service_cards = {}
        self.current_worker = None
        
        # Detect system language
        I18n.set_language(I18n.get_system_language())
        
        self._setup_window()
        self._setup_ui()
        self._apply_styles()
        self._setup_tray()
        self._start_detection()
        
        # Listen for language changes
        I18n.add_listener(self._on_language_changed)
        
        # Check for updates in background
        self._check_for_updates()
    
    def _setup_window(self):
        """Configure window properties"""
        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)
        
        # Try to load icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_ui(self):
        """Configure user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Update banner placeholder (hidden by default)
        self.update_banner_container = QVBoxLayout()
        main_layout.addLayout(self.update_banner_container)
        
        # Header with language selector
        header_layout = QVBoxLayout()
        
        # Top bar with language selector
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        
        lang_label = QLabel("🌍")
        lang_label.setStyleSheet("font-size: 16px;")
        top_bar.addWidget(lang_label)
        
        self.language_selector = LanguageSelector()
        top_bar.addWidget(self.language_selector)
        
        header_layout.addLayout(top_bar)
        
        self.title_label = QLabel(f"🤖 {t('app_title')}")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.title_label)
        
        self.subtitle_label = QLabel(t("app_subtitle"))
        self.subtitle_label.setObjectName("subtitle")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.subtitle_label)
        
        main_layout.addLayout(header_layout)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(20)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel(t("detecting_services"))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Main splitter with services and log
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel: Scroll area for services
        services_panel = QWidget()
        services_layout = QVBoxLayout(services_panel)
        services_layout.setContentsMargins(0, 0, 0, 0)
        
        self.services_header = QLabel(t("detected_services"))
        self.services_header.setStyleSheet("font-size: 14px; font-weight: bold; color: #00d4ff; padding: 5px;")
        services_layout.addWidget(self.services_header)
        
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
        
        # Right panel: Log viewer
        self.log_viewer = LogViewerWidget()
        splitter.addWidget(self.log_viewer)
        
        # Splitter proportions (60% services, 40% log)
        splitter.setSizes([600, 400])
        
        main_layout.addWidget(splitter, 1)
        
        # Scheduler toggle widget
        self.scheduler_toggle = SchedulerToggle()
        main_layout.addWidget(self.scheduler_toggle)
        
        # Safety Warnings
        warning_layout = QHBoxLayout()
        self.safety_label = QLabel(t("safety_warning"))
        self.safety_label.setStyleSheet("color: #ffcc00; font-weight: bold; margin-left: 10px;")
        self.backup_label = QLabel(t("backup_reminder"))
        self.backup_label.setStyleSheet("color: #00d4ff; font-style: italic; margin-right: 10px;")
        
        warning_layout.addWidget(self.safety_label)
        warning_layout.addStretch()
        warning_layout.addWidget(self.backup_label)
        
        main_layout.addLayout(warning_layout)
        
        # Footer with global buttons
        footer_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton(t("refresh"))
        self.refresh_btn.clicked.connect(self._start_detection)
        footer_layout.addWidget(self.refresh_btn)
        
        footer_layout.addStretch()
        
        self.backup_btn = QPushButton(t("create_backup"))
        self.backup_btn.clicked.connect(self._create_backup)
        footer_layout.addWidget(self.backup_btn)
        
        self.restore_btn = QPushButton(t("restore"))
        self.restore_btn.clicked.connect(self._restore_backup)
        footer_layout.addWidget(self.restore_btn)
        
        footer_layout.addStretch()
        
        # Export/Import buttons
        self.export_btn = QPushButton(t("export_config"))
        self.export_btn.clicked.connect(self._export_config)
        footer_layout.addWidget(self.export_btn)
        
        self.import_btn = QPushButton(t("import_config"))
        self.import_btn.clicked.connect(self._import_config)
        footer_layout.addWidget(self.import_btn)
        
        self.presets_btn = QPushButton(t("presets"))
        self.presets_btn.clicked.connect(self._show_presets_menu)
        footer_layout.addWidget(self.presets_btn)
        
        footer_layout.addStretch()
        
        self.disable_all_btn = QPushButton(t("disable_all"))
        self.disable_all_btn.setObjectName("danger")
        self.disable_all_btn.clicked.connect(self._disable_all)
        footer_layout.addWidget(self.disable_all_btn)
        
        main_layout.addLayout(footer_layout)
    
    def _apply_styles(self):
        """Apply CSS styles"""
        self.setStyleSheet(DARK_THEME)
    
    def _on_language_changed(self):
        """Update UI when language changes"""
        self.setWindowTitle(t("app_title"))
        self.title_label.setText(f"🤖 {t('app_title')}")
        self.subtitle_label.setText(t("app_subtitle"))
        self.services_header.setText(t("detected_services"))
        self.refresh_btn.setText(t("refresh"))
        self.backup_btn.setText(t("create_backup"))
        self.restore_btn.setText(t("restore"))
        self.restore_btn.setText(t("restore"))
        self.export_btn.setText(t("export_config"))
        self.import_btn.setText(t("import_config"))
        self.presets_btn.setText(t("presets"))
        self.disable_all_btn.setText(t("disable_all"))
        
        # Update service cards
        for card in self.service_cards.values():
            card.update_translations()
        
        # Update log viewer
        self.log_viewer.update_translations()
        
        # Update status
        if hasattr(self, '_last_services_count'):
            enabled = self._last_enabled_count
            count = self._last_services_count
            self.status_label.setText(t("services_found", count=count, enabled=enabled))
    
    def _start_detection(self):
        """Start service detection in background"""
        self.progress_bar.setVisible(True)
        self.status_label.setText(t("detecting_services"))
        
        self.detection_worker = DetectionWorker(self.detector)
        self.detection_worker.finished.connect(self._on_detection_finished)
        self.detection_worker.start()
    
    def _on_detection_finished(self, services):
        """Callback when detection finishes"""
        self.progress_bar.setVisible(False)
        
        # Clear previous cards
        for card in self.service_cards.values():
            card.deleteLater()
        self.service_cards.clear()
        
        # Create new cards and log detection
        for service in services:
            card = ServiceCard(service)
            card.disable_clicked.connect(self._on_disable_service)
            card.enable_clicked.connect(self._on_enable_service)
            
            # Insert before stretch
            self.services_layout.insertWidget(
                self.services_layout.count() - 1, 
                card
            )
            self.service_cards[service.id] = card
            
            # Log detection
            activity_logger.log_detection(service.id, service.name, service.status.value)
        
        enabled_count = sum(1 for s in services if s.status == ServiceStatus.ENABLED)
        self._last_services_count = len(services)
        self._last_enabled_count = enabled_count
        
        self.status_label.setText(t("services_found", count=len(services), enabled=enabled_count))
        
        # Update log viewer
        self.log_viewer.refresh()
    
    def _on_disable_service(self, service_id: str):
        """Handle disable service click"""
        if self.current_worker and self.current_worker.isRunning():
            return
        
        service = next((s for s in self.detector.services if s.id == service_id), None)
        if not service:
            return
        
        # Confirm action
        reply = QMessageBox.question(
            self,
            t("confirm"),
            t("confirm_disable", name=service.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        self._run_action("disable", service)
    
    def _on_enable_service(self, service_id: str):
        """Handle enable service click"""
        if self.current_worker and self.current_worker.isRunning():
            return
        
        service = next((s for s in self.detector.services if s.id == service_id), None)
        if not service:
            return
        
        self._run_action("enable", service)
    
    def _run_action(self, action: str, service: AIService):
        """Execute action in background"""
        self.progress_bar.setVisible(True)
        
        if action == "disable":
            self.status_label.setText(t("disabling", name=service.name))
        else:
            self.status_label.setText(t("enabling", name=service.name))
        
        self.current_worker = ActionWorker(action, self.manager, service)
        self.current_worker.finished.connect(
            lambda success, msg: self._on_action_finished(success, msg, service, action)
        )
        self.current_worker.start()
    
    def _on_action_finished(self, success: bool, message: str, service: AIService, action: str):
        """Callback when action finishes"""
        self.progress_bar.setVisible(False)
        
        # Log action
        if action == "disable":
            activity_logger.log_disable(service.id, service.name, success, message)
        else:
            activity_logger.log_enable(service.id, service.name, success, message)
        
        if success:
            self.status_label.setText(t("success", message=message))
            # Update card state
            updated_service = self.detector.refresh_service(service.id)
            if updated_service and service.id in self.service_cards:
                self.service_cards[service.id].update_status(updated_service.status)
        else:
            self.status_label.setText(t("error", message=message))
            QMessageBox.warning(self, t("error_title"), message)
        
        # Update log viewer
        self.log_viewer.refresh()
    
    def _create_backup(self):
        """Create backup of current configurations"""
        success, result = self.manager.create_backup(self.detector.services)
        
        # Log backup
        activity_logger.log_backup(success, result)
        
        if success:
            QMessageBox.information(
                self,
                t("backup_created"),
                t("backup_saved", path=result)
            )
        else:
            QMessageBox.warning(self, t("error_title"), t("backup_error", error=result))
        
        self.log_viewer.refresh()
    
    def _restore_backup(self):
        """Restore from latest backup"""
        backups = self.manager.get_backups()
        
        if not backups:
            QMessageBox.information(
                self,
                t("no_backups"),
                t("no_backups_available")
            )
            return
        
        # Use most recent backup
        latest = backups[0]
        
        reply = QMessageBox.question(
            self,
            t("confirm"),
            t("confirm_restore", timestamp=latest['timestamp']),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        success, message = self.manager.restore_backup(latest['path'])
        
        # Log restoration
        activity_logger.log_restore(success, message)
        
        if success:
            QMessageBox.information(self, t("restored"), message)
            self._start_detection()  # Refresh states
        else:
            QMessageBox.warning(self, t("error_title"), t("restore_error", error=message))
        
        self.log_viewer.refresh()
    
    def _disable_all(self):
        """Disable all AI services"""
        enabled_services = [
            s for s in self.detector.services 
            if s.status == ServiceStatus.ENABLED
        ]
        
        if not enabled_services:
            QMessageBox.information(
                self,
                t("info"),
                t("no_active_services")
            )
            return
        
        reply = QMessageBox.warning(
            self,
            t("warning"),
            t("confirm_disable_all", count=len(enabled_services)),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Create automatic backup first
        self.manager.create_backup(self.detector.services)
        activity_logger.log_backup(True, "Auto-backup before disabling all")
        
        # Disable all
        self.progress_bar.setVisible(True)
        success_count = 0
        
        for service in enabled_services:
            self.status_label.setText(t("disabling", name=service.name))
            QApplication.processEvents()
            
            success, message = self.manager.disable_service(service)
            activity_logger.log_disable(service.id, service.name, success, message)
            
            if success:
                success_count += 1
        
        self.progress_bar.setVisible(False)
        self.status_label.setText(t("disabled_count", success=success_count, total=len(enabled_services)))
        
        # Refresh states and log
        self._start_detection()
        self.log_viewer.refresh()
    
    def _check_for_updates(self):
        """Check for updates in background"""
        self.update_checker = UpdateChecker()
        self.update_checker.check_async(self._on_update_check_complete)
    
    def _on_update_check_complete(self, update_info: UpdateInfo):
        """Called when update check completes"""
        if update_info and update_info.is_newer:
            # Create and show update banner
            banner = UpdateBanner(
                update_info.version,
                update_info.html_url,
                self
            )
            self.update_banner_container.addWidget(banner)
    
    def _export_config(self):
        """Export current configuration to JSON"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                t("export_config"),
                "win-ai-tools-config.json",
                "JSON Files (*.json)"
            )
            
            if not file_path:
                return
            
            success, message = ConfigPersistence.export_config(self.detector.services, file_path)
            
            if success:
                QMessageBox.information(self, t("success", message=""), t("config_exported"))
                activity_logger.log_backup(True, f"Config exported to {file_path}")
            else:
                QMessageBox.warning(self, t("error_title"), message)
                
        except Exception as e:
            QMessageBox.critical(self, t("error_title"), str(e))

    def _import_config(self):
        """Import configuration from JSON"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                t("import_config"),
                "",
                "JSON Files (*.json)"
            )
            
            if not file_path:
                return
            
            success, config, message = ConfigPersistence.import_config(file_path)
            
            if not success:
                QMessageBox.warning(self, t("error_title"), t("import_error", error=message))
                return
            
            # Apply configuration
            self.progress_bar.setVisible(True)
            self.status_label.setText(t("config_imported"))
            QApplication.processEvents()
            
            applied_count = 0
            
            # Disable services marked as disabled in config
            for service_id, status in config.items():
                if status == "disabled":
                    service = next((s for s in self.detector.services if s.id == service_id), None)
                    if service and service.status != ServiceStatus.DISABLED:
                        # Disable it
                        success_disable, msg = self.manager.disable_service(service)
                        if success_disable:
                            applied_count += 1
                        activity_logger.log_disable(service.id, service.name, success_disable, "Imported config")
            
            self.progress_bar.setVisible(False)
            self.status_label.setText(t("success", message=f"Config imported: {applied_count} changes applied"))
            QMessageBox.information(self, t("info"), t("config_imported"))
            
            # Refresh
            self._start_detection()
            self.log_viewer.refresh()
            
        except Exception as e:
            QMessageBox.critical(self, t("error_title"), str(e))
    
    def _setup_tray(self):
        """Initialize system tray icon"""
        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show_window.connect(self._show_window)
        self.tray_icon.quit_app.connect(self._quit_app)
        self.tray_icon.show()
        
    def _show_window(self):
        """Show and restore window"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.activateWindow()
        
    def _quit_app(self):
        """Quit the application"""
        QApplication.quit()
        
    def closeEvent(self, event):
        """Handle close event - minimize to tray instead of exit"""
        if self.tray_icon.isVisible():
            if not getattr(self, '_tray_hint_shown', False):
                self.tray_icon.showMessage(
                    t("app_title"),
                    t("minimize_to_tray_hint"),
                    QSystemTrayIcon.MessageIcon.Information,
                    2000
                )
                self._tray_hint_shown = True
                
            self.hide()
            event.ignore()
        else:
            event.accept()
    
    def _show_presets_menu(self):
        """Show menu with configuration presets"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #16213e;
                color: #eaeaea;
                border: 1px solid #0f3460;
            }
            QMenu::item {
                padding: 8px 20px;
            }
            QMenu::item:selected {
                background-color: #0f3460;
            }
        """)
        
        presets = ConfigPersistence.get_presets()
        
        for key, data in presets.items():
            # Translate preset name if possible
            tr_key = f"preset_{key}"
            name = t(tr_key)
            if name == tr_key:
                name = data["name"]
                
            action = QAction(name, self)
            action.setToolTip(data["description"])
            
            # Use default argument capture directly in lambda
            # We must bind key=key to capture the current value
            action.triggered.connect(lambda checked, k=key: self._apply_preset(k))
            
            menu.addAction(action)
            
        menu.exec(self.presets_btn.mapToGlobal(self.presets_btn.rect().topLeft()))
        
    def _apply_preset(self, preset_key: str):
        """Apply selected preset"""
        presets = ConfigPersistence.get_presets()
        if preset_key not in presets:
            return
            
        data = presets[preset_key]
        config = data["config"]
        
        self.progress_bar.setVisible(True)
        self.status_label.setText(t("enabling")) # Generic message
        QApplication.processEvents()
        
        applied_count = 0
        
        # Handle special keywords
        if config == "DISABLE_ALL":
            self._disable_all()
            return
        elif config == "ENABLE_ALL":
            # Enable all services
            for service in self.detector.services:
                if service.status != ServiceStatus.ENABLED:
                    self._run_action("enable", service)
                    # We can't easily wait for all async actions here without refactoring
                    # So we just trigger them and let the queue/UI handle it
            return
            
        # Handle dict config
        elif isinstance(config, dict):
             for service_id, status in config.items():
                service = next((s for s in self.detector.services if s.id == service_id), None)
                if not service:
                    continue
                    
                if status == "disabled" and service.status != ServiceStatus.DISABLED:
                     self._run_action("disable", service)
                     applied_count += 1
                elif status == "enabled" and service.status != ServiceStatus.ENABLED:
                     self._run_action("enable", service)
                     applied_count += 1

        # Show success toast/message (simplified)
        tr_key = f"preset_{preset_key}"
        name = t(tr_key)
        if name == tr_key:
            name = data["name"]
            
        self.status_label.setText(t("preset_applied", name=name))
        
        # Refresh
        self._start_detection()
        self.log_viewer.refresh()
