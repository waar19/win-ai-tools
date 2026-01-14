"""
Configuration persistence module
Handles export and import of application settings and service states
"""

import json
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime
from .ai_services import AIService, ServiceStatus, get_all_services


class ConfigPersistence:
    """Manages configuration export/import"""
    
    @staticmethod
    def export_config(services: List[AIService], file_path: str) -> Tuple[bool, str]:
        """
        Export current service states to a JSON file.
        Returns (success, message)
        """
        try:
            export_data = {
                "meta": {
                    "app": "Windows AI Removal Tool",
                    "version": "1.1.0",
                    "timestamp": datetime.now().isoformat(),
                    "exported_services_count": len(services)
                },
                "services": {}
            }
            
            # Export state of each service
            for service in services:
                # We only really care about saving which ones are DISABLED
                # because ENABLED is the default Windows state
                export_data["services"][service.id] = {
                    "name": service.name,
                    "status": service.status.value
                }
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
                
            return True, f"Configuration exported successfully to {os.path.basename(file_path)}"
            
        except Exception as e:
            return False, f"Failed to export configuration: {str(e)}"
    
    @staticmethod
    def import_config(file_path: str) -> Tuple[bool, Dict[str, str], str]:
        """
        Import configuration from JSON file.
        Returns (success, services_config, message)
        where services_config is a dict mapping service_id -> desired_status
        """
        try:
            if not os.path.exists(file_path):
                return False, {}, f"File not found: {file_path}"
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Basic validation
            if "meta" not in data or "services" not in data:
                return False, {}, "Invalid configuration file format"
                
            # Extract service states
            services_config = {}
            for service_id, service_data in data["services"].items():
                if "status" in service_data:
                    services_config[service_id] = service_data["status"]
            
            return True, services_config, f"Loaded configuration with {len(services_config)} service settings"
            
        except json.JSONDecodeError:
            return False, {}, "Invalid JSON file"
        except Exception as e:
            return False, {}, f"Failed to import configuration: {str(e)}"
    
    @staticmethod
    def get_presets() -> Dict[str, Dict[str, str]]:
        """Get built-in configuration presets"""
        presets = {
            "privacy_max": {
                "name": "Maximum Privacy (Disable All)",
                "description": "Disables all detected AI services",
                "config": "DISABLE_ALL" # Special keyword
            },
            "balanced": {
                "name": "Balanced (Keep Search)",
                "description": "Disables Copilot and Recall, but keeps Search features",
                "config": {
                    "copilot": "disabled",
                    "recall": "disabled",
                    "ai_explorer": "disabled",
                    "bing_search": "enabled",
                    "web_search": "enabled"
                }
            },
            "reset": {
                "name": "Reset to Defaults (Enable All)",
                "description": "Re-enables all AI services (Windows Defaults)",
                "config": "ENABLE_ALL" # Special keyword
            }
        }
        return presets
