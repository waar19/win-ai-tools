"""
Internationalization (i18n) support for the application
Supports: English (en), German (de), Spanish (es)
"""

import locale

# Available languages
LANGUAGES = {
    "en": "English",
    "de": "Deutsch", 
    "es": "Español"
}

# Default language
DEFAULT_LANGUAGE = "en"

# Translations dictionary
TRANSLATIONS = {
    "en": {
        # Window
        "app_title": "Windows AI Removal Tool",
        "app_subtitle": "Manage and remove AI services from Windows 11",
        
        # Status
        "detecting_services": "Detecting AI services...",
        "services_found": "Found {count} AI services • {enabled} active",
        "disabling": "Disabling {name}...",
        "enabling": "Enabling {name}...",
        "success": "✓ {message}",
        "error": "✗ Error: {message}",
        "disabled_count": "✓ Disabled {success}/{total} services",
        
        # Buttons
        "refresh": "🔄 Refresh",
        "create_backup": "💾 Create Backup",
        "restore": "↩️ Restore",
        "disable_all": "🚫 Disable All",
        "enable": "Enable",
        "disable": "Disable",
        "export_config": "📤 Export Config",
        "import_config": "📥 Import Config",
        "presets": "⚡ Presets",
        
        # Presets
        "preset_privacy_max": "Maximum Privacy (Disable All)",
        "preset_balanced": "Balanced (Keep Search)",
        "preset_reset": "Reset to Defaults (Enable All)",
        "preset_applied": "Preset '{name}' applied successfully!",
        
        # System Tray
        "tray_open": "Open Dashboard",
        "tray_quit": "Quit Application",
        "tray_start_with_windows": "Start with Windows",
        "minimize_to_tray_hint": "App is running in background. Click icon to open.",
        
        # Headers
        "detected_services": "🛡️ Detected AI Services",
        "activity_log": "📋 Activity Log",
        
        # Dialogs
        "confirm": "Confirm",
        "confirm_disable": "Do you want to disable {name}?\n\nThis will modify system settings.",
        "confirm_disable_all": "Are you sure you want to disable ALL {count} AI services?\n\nIt's recommended to create a backup first.",
        "confirm_restore": "Do you want to restore from backup {timestamp}?",
        "backup_created": "Backup Created",
        "backup_saved": "Backup saved to:\n{path}",
        "backup_error": "Could not create backup: {error}",
        "no_backups": "No Backups",
        "no_backups_available": "No backups available to restore.",
        "restored": "Restored",
        "restore_error": "Error restoring: {error}",
        "info": "Information",
        "no_active_services": "No active services to disable.",
        "warning": "⚠️ Confirm",
        "error_title": "Error",
        "config_exported": "Configuration exported successfully!",
        "config_imported": "Configuration imported successfully.\nApplying settings now...",
        "import_error": "Error importing configuration: {error}",
        
        # Service status
        "status_enabled": "● Active",
        "status_disabled": "○ Disabled",
        "status_not_installed": "✗ Not installed",
        "status_unknown": "? Unknown",
        
        # Log
        "no_activity": "No activity recorded",
        
        # Permissions
        "permissions_required": "Permissions Required",
        "admin_required": "This application requires administrator permissions to modify system settings.",
        "run_as_admin": "Please run the application as Administrator.",
        
        # Language
        "language": "Language",
        
        # Update
        "update_available": "New version {version} is available!",
        "download_update": "⬇️ Download",
        
        # Scheduler
        "auto_maintenance": "Auto-Maintenance",
        "auto_maintenance_desc": "Re-apply settings after Windows Updates (runs at startup & daily)",
        "scheduler_active": "● Active",
        "scheduler_inactive": "○ Inactive",
    },
    
    "de": {
        # Window
        "app_title": "Windows AI-Entfernungstool",
        "app_subtitle": "KI-Dienste von Windows 11 verwalten und entfernen",
        
        # Status
        "detecting_services": "KI-Dienste werden erkannt...",
        "services_found": "{count} KI-Dienste gefunden • {enabled} aktiv",
        "disabling": "{name} wird deaktiviert...",
        "enabling": "{name} wird aktiviert...",
        "success": "✓ {message}",
        "error": "✗ Fehler: {message}",
        "disabled_count": "✓ {success}/{total} Dienste deaktiviert",
        
        # Buttons
        "refresh": "🔄 Aktualisieren",
        "create_backup": "💾 Backup erstellen",
        "restore": "↩️ Wiederherstellen",
        "disable_all": "🚫 Alle deaktivieren",
        "enable": "Aktivieren",
        "disable": "Deaktivieren",
        "export_config": "📤 Config Exportieren",
        "import_config": "📥 Config Importieren",
        "presets": "⚡ Vorlagen",
        
        # Presets
        "preset_privacy_max": "Maximale Privatsphäre (Alle aus)",
        "preset_balanced": "Ausgewogen (Suche behalten)",
        "preset_reset": "Zurücksetzen (Alle an)",
        "preset_applied": "Vorlage '{name}' erfolgreich angewendet!",
        
        # System Tray
        "tray_open": "Dashboard Öffnen",
        "tray_quit": "Beenden",
        "tray_start_with_windows": "Mit Windows starten",
        "minimize_to_tray_hint": "App läuft im Hintergrund. Klicken zum Öffnen.",
        
        # Headers
        "detected_services": "🛡️ Erkannte KI-Dienste",
        "activity_log": "📋 Aktivitätsprotokoll",
        
        # Dialogs
        "confirm": "Bestätigen",
        "confirm_disable": "Möchten Sie {name} deaktivieren?\n\nDies ändert Systemeinstellungen.",
        "confirm_disable_all": "Sind Sie sicher, dass Sie ALLE {count} KI-Dienste deaktivieren möchten?\n\nEs wird empfohlen, zuerst ein Backup zu erstellen.",
        "confirm_restore": "Möchten Sie vom Backup {timestamp} wiederherstellen?",
        "backup_created": "Backup erstellt",
        "backup_saved": "Backup gespeichert unter:\n{path}",
        "backup_error": "Backup konnte nicht erstellt werden: {error}",
        "no_backups": "Keine Backups",
        "no_backups_available": "Keine Backups zum Wiederherstellen verfügbar.",
        "restored": "Wiederhergestellt",
        "restore_error": "Fehler beim Wiederherstellen: {error}",
        "info": "Information",
        "no_active_services": "Keine aktiven Dienste zum Deaktivieren.",
        "warning": "⚠️ Bestätigen",
        "error_title": "Fehler",
        "config_exported": "Konfiguration erfolgreich exportiert!",
        "config_imported": "Konfiguration erfolgreich importiert.\nEinstellungen werden angewendet...",
        "import_error": "Fehler beim Importieren der Konfiguration: {error}",
        
        # Service status
        "status_enabled": "● Aktiv",
        "status_disabled": "○ Deaktiviert",
        "status_not_installed": "✗ Nicht installiert",
        "status_unknown": "? Unbekannt",
        
        # Log
        "no_activity": "Keine Aktivität aufgezeichnet",
        
        # Permissions
        "permissions_required": "Berechtigungen erforderlich",
        "admin_required": "Diese Anwendung benötigt Administratorrechte, um Systemeinstellungen zu ändern.",
        "run_as_admin": "Bitte führen Sie die Anwendung als Administrator aus.",
        
        # Language
        "language": "Sprache",
        
        # Update
        "update_available": "Neue Version {version} ist verfügbar!",
        "download_update": "⬇️ Herunterladen",
        
        # Scheduler
        "auto_maintenance": "Auto-Wartung",
        "auto_maintenance_desc": "Einstellungen nach Windows-Updates erneut anwenden (läuft beim Start & täglich)",
        "scheduler_active": "● Aktiv",
        "scheduler_inactive": "○ Inaktiv",
    },
    
    "es": {
        # Window
        "app_title": "Herramienta de Eliminación de AI de Windows",
        "app_subtitle": "Gestiona y remueve servicios de Inteligencia Artificial de Windows 11",
        
        # Status
        "detecting_services": "Detectando servicios AI...",
        "services_found": "Encontrados {count} servicios AI • {enabled} activos",
        "disabling": "Deshabilitando {name}...",
        "enabling": "Habilitando {name}...",
        "success": "✓ {message}",
        "error": "✗ Error: {message}",
        "disabled_count": "✓ Deshabilitados {success}/{total} servicios",
        
        # Buttons
        "refresh": "🔄 Actualizar",
        "create_backup": "💾 Crear Backup",
        "restore": "↩️ Restaurar",
        "disable_all": "🚫 Deshabilitar Todo",
        "enable": "Habilitar",
        "disable": "Deshabilitar",
        "export_config": "📤 Exportar Config",
        "import_config": "📥 Importar Config",
        "presets": "⚡ Preajustes",
        
        # Presets
        "preset_privacy_max": "Privacidad Máxima (Desactivar Todo)",
        "preset_balanced": "Balanceado (Mantener Búsqueda)",
        "preset_reset": "Restaurar Defaults (Activar Todo)",
        "preset_applied": "¡Preajuste '{name}' aplicado exitosamente!",
        
        # System Tray
        "tray_open": "Abrir Dashboard",
        "tray_quit": "Salir",
        "tray_start_with_windows": "Iniciar con Windows",
        "minimize_to_tray_hint": "La app se ejecuta en segundo plano. Clic para abrir.",
        
        # Headers
        "detected_services": "🛡️ Servicios AI Detectados",
        "activity_log": "📋 Log de Actividad",
        
        # Dialogs
        "confirm": "Confirmar",
        "confirm_disable": "¿Desea deshabilitar {name}?\n\nEsto modificará configuraciones del sistema.",
        "confirm_disable_all": "¿Está seguro de deshabilitar TODOS los {count} servicios AI?\n\nSe recomienda crear un backup primero.",
        "confirm_restore": "¿Desea restaurar desde el backup del {timestamp}?",
        "backup_created": "Backup Creado",
        "backup_saved": "Backup guardado en:\n{path}",
        "backup_error": "No se pudo crear backup: {error}",
        "no_backups": "Sin Backups",
        "no_backups_available": "No hay backups disponibles para restaurar.",
        "restored": "Restaurado",
        "restore_error": "Error restaurando: {error}",
        "info": "Información",
        "no_active_services": "No hay servicios activos para deshabilitar.",
        "warning": "⚠️ Confirmar",
        "error_title": "Error",
        "config_exported": "¡Configuración exportada exitosamente!",
        "config_imported": "Configuración importada exitosamente.\nAplicando ajustes ahora...",
        "import_error": "Error al importar configuración: {error}",
        
        # Service status
        "status_enabled": "● Activo",
        "status_disabled": "○ Deshabilitado",
        "status_not_installed": "✗ No instalado",
        "status_unknown": "? Desconocido",
        
        # Log
        "no_activity": "Sin actividad registrada",
        
        # Permissions
        "permissions_required": "Permisos Requeridos",
        "admin_required": "Esta aplicación requiere permisos de administrador para modificar configuraciones del sistema.",
        "run_as_admin": "Por favor, ejecute la aplicación como Administrador.",
        
        # Language
        "language": "Idioma",
        
        # Update
        "update_available": "¡Nueva versión {version} disponible!",
        "download_update": "⬇️ Descargar",
        
        # Scheduler
        "auto_maintenance": "Auto-Mantenimiento",
        "auto_maintenance_desc": "Re-aplicar configuración después de Windows Updates (ejecuta al inicio y diariamente)",
        "scheduler_active": "● Activo",
        "scheduler_inactive": "○ Inactivo",
    }
}


class I18n:
    """Internationalization manager"""
    
    _current_language = DEFAULT_LANGUAGE
    _listeners = []
    
    @classmethod
    def get_system_language(cls) -> str:
        """Detect system language"""
        try:
            lang_code = locale.getdefaultlocale()[0]
            if lang_code:
                lang = lang_code.split('_')[0].lower()
                if lang in LANGUAGES:
                    return lang
        except:
            pass
        return DEFAULT_LANGUAGE
    
    @classmethod
    def get_language(cls) -> str:
        """Get current language"""
        return cls._current_language
    
    @classmethod
    def set_language(cls, lang: str):
        """Set current language"""
        if lang in LANGUAGES:
            cls._current_language = lang
            # Notify listeners
            for listener in cls._listeners:
                try:
                    listener()
                except:
                    pass
    
    @classmethod
    def add_listener(cls, callback):
        """Add language change listener"""
        cls._listeners.append(callback)
    
    @classmethod
    def remove_listener(cls, callback):
        """Remove language change listener"""
        if callback in cls._listeners:
            cls._listeners.remove(callback)
    
    @classmethod
    def t(cls, key: str, **kwargs) -> str:
        """Get translated string"""
        lang = cls._current_language
        if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
            text = TRANSLATIONS[lang][key]
        elif key in TRANSLATIONS[DEFAULT_LANGUAGE]:
            text = TRANSLATIONS[DEFAULT_LANGUAGE][key]
        else:
            return key
        
        # Apply format arguments
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        
        return text


# Shortcut function
def t(key: str, **kwargs) -> str:
    """Shortcut for I18n.t()"""
    return I18n.t(key, **kwargs)
