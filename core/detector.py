"""
Detector de servicios AI
Verifica el estado actual de cada servicio en el sistema
"""

import winreg
import subprocess
from typing import List, Optional
from .ai_services import AIService, ServiceStatus, get_all_services


class AIServiceDetector:
    """Detecta y verifica el estado de servicios AI en Windows"""
    
    def __init__(self):
        self.services = get_all_services()
    
    def detect_all(self) -> List[AIService]:
        """Detecta el estado de todos los servicios AI"""
        for service in self.services:
            service.status = self._detect_service_status(service)
        return self.services
    
    def _detect_service_status(self, service: AIService) -> ServiceStatus:
        """Detecta el estado de un servicio específico"""
        # Verificar registry paths
        if service.registry_paths:
            registry_status = self._check_registry_status(service)
            if registry_status != ServiceStatus.UNKNOWN:
                return registry_status
        
        # Verificar Appx packages
        if service.appx_packages:
            appx_status = self._check_appx_status(service)
            if appx_status != ServiceStatus.UNKNOWN:
                return appx_status
        
        # Verificar Windows Feature
        if service.windows_feature:
            feature_status = self._check_windows_feature(service)
            if feature_status != ServiceStatus.UNKNOWN:
                return feature_status
        
        return ServiceStatus.UNKNOWN
    
    def _check_registry_status(self, service: AIService) -> ServiceStatus:
        """Verifica el estado basado en llaves de registro"""
        for reg_info in service.registry_paths:
            try:
                key = winreg.OpenKey(
                    reg_info["hive"],
                    reg_info["path"],
                    0,
                    winreg.KEY_READ
                )
                value, _ = winreg.QueryValueEx(key, reg_info["key"])
                winreg.CloseKey(key)
                
                if value == reg_info["disable_value"]:
                    return ServiceStatus.DISABLED
                elif value == reg_info["enable_value"]:
                    return ServiceStatus.ENABLED
                    
            except FileNotFoundError:
                # Key no existe, servicio probablemente habilitado por defecto
                continue
            except PermissionError:
                continue
            except Exception:
                continue
        
        # Si no encontramos keys deshabilitantes, asumimos habilitado
        return ServiceStatus.ENABLED
    
    def _check_appx_status(self, service: AIService) -> ServiceStatus:
        """Verifica si paquetes Appx están instalados"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", "Get-AppxPackage | Select-Object Name | ConvertTo-Json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return ServiceStatus.UNKNOWN
            
            output = result.stdout.strip()
            if not output:
                return ServiceStatus.UNKNOWN
            
            # Buscar paquetes
            for package_name in service.appx_packages:
                if package_name.lower() in output.lower():
                    return ServiceStatus.ENABLED
            
            return ServiceStatus.NOT_INSTALLED
            
        except Exception:
            return ServiceStatus.UNKNOWN
    
    def _check_windows_feature(self, service: AIService) -> ServiceStatus:
        """Verifica si una Windows Feature está habilitada"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", 
                 f"Get-WindowsOptionalFeature -Online -FeatureName '{service.windows_feature}' | Select-Object State | ConvertTo-Json"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0 or "not found" in result.stderr.lower():
                return ServiceStatus.NOT_INSTALLED
            
            if "Enabled" in result.stdout:
                return ServiceStatus.ENABLED
            elif "Disabled" in result.stdout:
                return ServiceStatus.DISABLED
            
            return ServiceStatus.UNKNOWN
            
        except Exception:
            return ServiceStatus.UNKNOWN
    
    def refresh_service(self, service_id: str) -> Optional[AIService]:
        """Actualiza el estado de un servicio específico"""
        for service in self.services:
            if service.id == service_id:
                service.status = self._detect_service_status(service)
                return service
        return None
