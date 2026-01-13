"""
Sistema de logging para registrar todas las acciones de la aplicación
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class LogLevel(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class LogEntry:
    """Representa una entrada del log"""
    timestamp: str
    level: str
    action: str
    service_id: str
    service_name: str
    message: str
    details: Dict[str, Any] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class ActivityLogger:
    """Gestiona el registro de actividades de la aplicación"""
    
    def __init__(self):
        self.log_dir = os.path.join(os.path.expanduser("~"), ".win-ai-tools-logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.current_log_file = os.path.join(
            self.log_dir, 
            f"activity_{datetime.now().strftime('%Y%m%d')}.json"
        )
        self._entries: List[LogEntry] = []
        self._load_today_logs()
    
    def _load_today_logs(self):
        """Carga los logs del día actual si existen"""
        try:
            if os.path.exists(self.current_log_file):
                with open(self.current_log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._entries = [
                        LogEntry(**entry) for entry in data.get("entries", [])
                    ]
        except Exception:
            self._entries = []
    
    def _save_logs(self):
        """Guarda los logs en archivo"""
        try:
            data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "entries": [entry.to_dict() for entry in self._entries]
            }
            with open(self.current_log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def log(self, level: LogLevel, action: str, service_id: str, 
            service_name: str, message: str, details: Dict = None):
        """Agrega una entrada al log"""
        entry = LogEntry(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            level=level.value,
            action=action,
            service_id=service_id,
            service_name=service_name,
            message=message,
            details=details
        )
        self._entries.append(entry)
        self._save_logs()
        return entry
    
    def log_detection(self, service_id: str, service_name: str, status: str):
        """Log de detección de servicio"""
        return self.log(
            LogLevel.INFO,
            "DETECTION",
            service_id,
            service_name,
            f"Servicio detectado con estado: {status}"
        )
    
    def log_disable(self, service_id: str, service_name: str, success: bool, message: str):
        """Log de deshabilitación de servicio"""
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        return self.log(
            level,
            "DISABLE",
            service_id,
            service_name,
            message
        )
    
    def log_enable(self, service_id: str, service_name: str, success: bool, message: str):
        """Log de habilitación de servicio"""
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        return self.log(
            level,
            "ENABLE",
            service_id,
            service_name,
            message
        )
    
    def log_backup(self, success: bool, path: str):
        """Log de creación de backup"""
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        msg = f"Backup creado: {path}" if success else f"Error creando backup: {path}"
        return self.log(
            level,
            "BACKUP",
            "system",
            "Sistema",
            msg
        )
    
    def log_restore(self, success: bool, message: str):
        """Log de restauración de backup"""
        level = LogLevel.SUCCESS if success else LogLevel.ERROR
        return self.log(
            level,
            "RESTORE",
            "system",
            "Sistema",
            message
        )
    
    def get_entries(self, limit: int = 50) -> List[LogEntry]:
        """Obtiene las últimas entradas del log"""
        return list(reversed(self._entries[-limit:]))
    
    def get_entries_for_service(self, service_id: str, limit: int = 20) -> List[LogEntry]:
        """Obtiene entradas de un servicio específico"""
        filtered = [e for e in self._entries if e.service_id == service_id]
        return list(reversed(filtered[-limit:]))
    
    def get_all_log_files(self) -> List[str]:
        """Lista todos los archivos de log disponibles"""
        try:
            files = [f for f in os.listdir(self.log_dir) if f.endswith('.json')]
            return sorted(files, reverse=True)
        except:
            return []
    
    def clear_old_logs(self, days_to_keep: int = 30):
        """Elimina logs más antiguos que X días"""
        try:
            cutoff = datetime.now().timestamp() - (days_to_keep * 86400)
            for filename in os.listdir(self.log_dir):
                filepath = os.path.join(self.log_dir, filename)
                if os.path.getmtime(filepath) < cutoff:
                    os.remove(filepath)
        except:
            pass


# Instancia global del logger
activity_logger = ActivityLogger()
