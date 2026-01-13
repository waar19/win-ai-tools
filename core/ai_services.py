"""
Definición de servicios AI de Windows 11 y métodos para detectar/modificar
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any
import subprocess
import json
import winreg
import os


class ServiceStatus(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    NOT_INSTALLED = "not_installed"
    UNKNOWN = "unknown"


@dataclass
class AIService:
    """Representa un servicio AI de Windows"""
    id: str
    name: str
    description: str
    status: ServiceStatus = ServiceStatus.UNKNOWN
    
    # Registry paths para detectar/modificar
    registry_paths: List[Dict[str, Any]] = None
    
    # Appx package names
    appx_packages: List[str] = None
    
    # Windows Feature name
    windows_feature: Optional[str] = None


# Definición de servicios AI conocidos
AI_SERVICES = [
    AIService(
        id="copilot",
        name="Microsoft Copilot",
        description="Asistente AI integrado en Windows 11 con acceso a Bing Chat",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsCopilot",
                "key": "TurnOffWindowsCopilot",
                "disable_value": 1,
                "enable_value": 0,
                "hive": winreg.HKEY_LOCAL_MACHINE
            },
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                "key": "ShowCopilotButton",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ],
        appx_packages=[
            "Microsoft.Copilot",
            "Microsoft.Windows.Ai.Copilot.Provider"
        ]
    ),
    AIService(
        id="recall",
        name="Windows Recall",
        description="Captura snapshots de pantalla para búsqueda AI (Copilot+ PCs)",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI",
                "key": "AllowRecallEnablement",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_LOCAL_MACHINE
            },
            {
                "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI",
                "key": "DisableAIDataAnalysis",
                "disable_value": 1,
                "enable_value": 0,
                "hive": winreg.HKEY_LOCAL_MACHINE
            }
        ],
        windows_feature="Recall"
    ),
    AIService(
        id="ai_explorer",
        name="AI Explorer",
        description="Funciones de exploración AI en Windows",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Windows\WindowsAI",
                "key": "DisableAIDataAnalysis",
                "disable_value": 1,
                "enable_value": 0,
                "hive": winreg.HKEY_LOCAL_MACHINE
            }
        ],
        appx_packages=[
            "MicrosoftWindows.Client.AIX"
        ]
    ),
    AIService(
        id="bing_search",
        name="Bing Search en Start Menu",
        description="Integración de búsqueda web Bing en el menú inicio",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Windows\Explorer",
                "key": "DisableSearchBoxSuggestions",
                "disable_value": 1,
                "enable_value": 0,
                "hive": winreg.HKEY_LOCAL_MACHINE
            },
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search",
                "key": "BingSearchEnabled",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ]
    ),
    AIService(
        id="web_search",
        name="Web Search en Taskbar",
        description="Sugerencias web y AI en la búsqueda de la barra de tareas",
        registry_paths=[
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search",
                "key": "CortanaConsent",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ]
    ),
    AIService(
        id="windows_widgets",
        name="Windows Widgets (AI News)",
        description="Widgets con noticias personalizadas por AI en el escritorio",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Dsh",
                "key": "AllowNewsAndInterests",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_LOCAL_MACHINE
            },
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
                "key": "TaskbarDa",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ],
        appx_packages=[
            "MicrosoftWindows.Client.WebExperience"
        ]
    ),
    AIService(
        id="cortana",
        name="Cortana (Legacy)",
        description="Asistente de voz Cortana (versión legacy)",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
                "key": "AllowCortana",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_LOCAL_MACHINE
            },
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Search",
                "key": "CortanaEnabled",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ],
        appx_packages=[
            "Microsoft.549981C3F5F10"
        ]
    ),
    AIService(
        id="edge_copilot",
        name="Edge Copilot Sidebar",
        description="Panel lateral de Copilot en Microsoft Edge",
        registry_paths=[
            {
                "path": r"SOFTWARE\Policies\Microsoft\Edge",
                "key": "HubsSidebarEnabled",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_LOCAL_MACHINE
            },
            {
                "path": r"SOFTWARE\Policies\Microsoft\Edge",
                "key": "CopilotCDPPageContext",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_LOCAL_MACHINE
            }
        ]
    ),
    AIService(
        id="ai_voice_typing",
        name="AI Voice Typing",
        description="Dictado por voz con transcripción AI mejorada",
        registry_paths=[
            {
                "path": r"SOFTWARE\Microsoft\Speech_OneCore\Preferences",
                "key": "VoiceActivationEnableAboveLockscreen",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            },
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\CPSS\Store\VoiceActivation",
                "key": "Value",
                "disable_value": 0,
                "enable_value": 1,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ]
    ),
    AIService(
        id="suggested_actions",
        name="Suggested Actions",
        description="Acciones sugeridas por AI al copiar texto/fechas",
        registry_paths=[
            {
                "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\SmartActionPlatform\SmartClipboard",
                "key": "Disabled",
                "disable_value": 1,
                "enable_value": 0,
                "hive": winreg.HKEY_CURRENT_USER
            }
        ]
    )
]


def get_all_services() -> List[AIService]:
    """Retorna lista de todos los servicios AI definidos"""
    return AI_SERVICES.copy()
