"""
Gestor de servicios AI
Habilita, deshabilita y remueve servicios AI de Windows
"""

import winreg
import subprocess
import os
import json
from datetime import datetime
from typing import Tuple, Optional
from .ai_services import AIService, ServiceStatus
from .i18n import t


class AIServiceManager:
    """Gestiona la habilitación/deshabilitación de servicios AI"""
    
    def __init__(self):
        self.backup_dir = os.path.join(os.path.expanduser("~"), ".win-ai-tools-backup")
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def disable_service(self, service: AIService) -> Tuple[bool, str]:
        """Deshabilita un servicio AI"""
        errors = []
        success_count = 0
        
        # Modificar Registry
        if service.registry_paths:
            for reg_info in service.registry_paths:
                success, error = self._set_registry_value(
                    reg_info["hive"],
                    reg_info["path"],
                    reg_info["key"],
                    reg_info["disable_value"]
                )
                if success:
                    success_count += 1
                else:
                    errors.append(error)
        
        # Remover Appx packages
        if service.appx_packages:
            for package in service.appx_packages:
                success, error = self._remove_appx_package(package)
                if success:
                    success_count += 1
                elif "not found" not in error.lower():
                    errors.append(error)
        
        # Deshabilitar Windows Feature
        if service.windows_feature:
            success, error = self._disable_windows_feature(service.windows_feature)
            if success:
                success_count += 1
            elif "not found" not in error.lower():
                errors.append(error)
        
        if success_count > 0:
            return True, t("service_disabled", count=success_count)
        else:
            return False, "; ".join(errors) if errors else t("no_changes")
    
    def enable_service(self, service: AIService) -> Tuple[bool, str]:
        """Habilita un servicio AI (restaura valores por defecto)"""
        errors = []
        success_count = 0
        
        # Modificar Registry
        if service.registry_paths:
            for reg_info in service.registry_paths:
                success, error = self._set_registry_value(
                    reg_info["hive"],
                    reg_info["path"],
                    reg_info["key"],
                    reg_info["enable_value"]
                )
                if success:
                    success_count += 1
                else:
                    errors.append(error)
        
        # Habilitar Windows Feature
        if service.windows_feature:
            success, error = self._enable_windows_feature(service.windows_feature)
            if success:
                success_count += 1
            elif "not found" not in error.lower():
                errors.append(error)
        
        if success_count > 0:
            return True, t("service_enabled", count=success_count)
        else:
            return False, "; ".join(errors) if errors else t("no_changes")
    
    def _set_registry_value(self, hive, path: str, key: str, value: int) -> Tuple[bool, str]:
        """Establece un valor en el registro de Windows"""
        try:
            # Crear la key si no existe
            reg_key = winreg.CreateKeyEx(
                hive,
                path,
                0,
                winreg.KEY_WRITE
            )
            winreg.SetValueEx(reg_key, key, 0, winreg.REG_DWORD, value)
            winreg.CloseKey(reg_key)
            return True, ""
        except PermissionError:
            return False, t("permission_error", path=f"{path}\\{key}")
        except Exception as e:
            return False, t("registry_error", error=str(e))
    
    def _remove_appx_package(self, package_name: str) -> Tuple[bool, str]:
        """Remueve un paquete Appx"""
        try:
            # Primero verificar si existe
            check_cmd = f"Get-AppxPackage -Name '*{package_name}*'"
            check_result = subprocess.run(
                ["powershell", "-Command", check_cmd],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if not check_result.stdout.strip():
                return True, "Package not found (already removed)"
            
            # Remover el paquete
            remove_cmd = f"Get-AppxPackage -Name '*{package_name}*' | Remove-AppxPackage"
            result = subprocess.run(
                ["powershell", "-Command", remove_cmd],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr or "Error removing package"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout removing package"
        except Exception as e:
            return False, str(e)
    
    def _disable_windows_feature(self, feature_name: str) -> Tuple[bool, str]:
        """Deshabilita una Windows Feature"""
        try:
            cmd = f"Disable-WindowsOptionalFeature -Online -FeatureName '{feature_name}' -NoRestart"
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0 or "not found" in result.stderr.lower():
                return True, ""
            else:
                return False, result.stderr or "Error disabling feature"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout disabling feature"
        except Exception as e:
            return False, str(e)
    
    def _enable_windows_feature(self, feature_name: str) -> Tuple[bool, str]:
        """Habilita una Windows Feature"""
        try:
            cmd = f"Enable-WindowsOptionalFeature -Online -FeatureName '{feature_name}' -NoRestart"
            result = subprocess.run(
                ["powershell", "-Command", cmd],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr or "Error enabling feature"
                
        except subprocess.TimeoutExpired:
            return False, "Timeout enabling feature"
        except Exception as e:
            return False, str(e)
    
    def create_backup(self, services: list) -> Tuple[bool, str]:
        """Crea backup de todas las configuraciones actuales"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.json")
            
            backup_data = {
                "timestamp": timestamp,
                "services": []
            }
            
            for service in services:
                service_backup = {
                    "id": service.id,
                    "name": service.name,
                    "registry_values": []
                }
                
                # Exportar valores de registry actuales
                if service.registry_paths:
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
                            
                            service_backup["registry_values"].append({
                                "path": reg_info["path"],
                                "key": reg_info["key"],
                                "value": value,
                                "hive": "HKLM" if reg_info["hive"] == winreg.HKEY_LOCAL_MACHINE else "HKCU"
                            })
                        except:
                            pass
                
                backup_data["services"].append(service_backup)
            
            with open(backup_file, 'w') as f:
                json.dump(backup_data, f, indent=2)
            
            return True, backup_file
            
        except Exception as e:
            return False, str(e)
    
    def get_backups(self) -> list:
        """Lista todos los backups disponibles"""
        try:
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith("backup_") and file.endswith(".json"):
                    path = os.path.join(self.backup_dir, file)
                    backups.append({
                        "filename": file,
                        "path": path,
                        "timestamp": file.replace("backup_", "").replace(".json", "")
                    })
            return sorted(backups, key=lambda x: x["timestamp"], reverse=True)
        except:
            return []
    
    def restore_backup(self, backup_path: str) -> Tuple[bool, str]:
        """Restaura configuraciones desde un backup"""
        try:
            with open(backup_path, 'r') as f:
                backup_data = json.load(f)
            
            restored_count = 0
            
            for service_data in backup_data.get("services", []):
                for reg_value in service_data.get("registry_values", []):
                    hive = winreg.HKEY_LOCAL_MACHINE if reg_value["hive"] == "HKLM" else winreg.HKEY_CURRENT_USER
                    success, _ = self._set_registry_value(
                        hive,
                        reg_value["path"],
                        reg_value["key"],
                        reg_value["value"]
                    )
                    if success:
                        restored_count += 1
            
            return True, f"Restaurados {restored_count} valores"
            
        except Exception as e:
            return False, str(e)
