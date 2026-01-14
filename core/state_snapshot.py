"""
State Snapshot Manager
Saves and compares AI service states to detect changes after Windows Updates
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from .ai_services import AIService, ServiceStatus


@dataclass
class ServiceChange:
    """Represents a change in a service's status"""
    service_id: str
    service_name: str
    previous_status: str
    current_status: str
    
    @property
    def was_reenabled(self) -> bool:
        """Check if service was re-enabled (likely by Windows Update)"""
        return (self.previous_status == ServiceStatus.DISABLED.value and 
                self.current_status == ServiceStatus.ENABLED.value)


class StateSnapshot:
    """Manages saving and comparing service state snapshots"""
    
    def __init__(self):
        self.snapshot_dir = self._get_snapshot_dir()
        self.snapshot_file = os.path.join(self.snapshot_dir, "state_snapshot.json")
    
    def _get_snapshot_dir(self) -> str:
        """Get the directory for storing snapshots"""
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        snapshot_dir = os.path.join(appdata, 'WinAIRemovalTool')
        os.makedirs(snapshot_dir, exist_ok=True)
        return snapshot_dir
    
    def save_snapshot(self, services: List[AIService]) -> Tuple[bool, str]:
        """
        Save current state of all services to a JSON file.
        Returns (success, message)
        """
        try:
            snapshot_data = {
                "meta": {
                    "app": "Windows AI Removal Tool",
                    "version": "1.2.0",
                    "timestamp": datetime.now().isoformat(),
                    "services_count": len(services)
                },
                "services": {}
            }
            
            for service in services:
                snapshot_data["services"][service.id] = {
                    "name": service.name,
                    "status": service.status.value if service.status else ServiceStatus.UNKNOWN.value
                }
            
            with open(self.snapshot_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot_data, f, indent=2, ensure_ascii=False)
            
            return True, f"Snapshot saved with {len(services)} services"
            
        except Exception as e:
            return False, f"Failed to save snapshot: {str(e)}"
    
    def load_snapshot(self) -> Optional[Dict[str, Any]]:
        """
        Load the last saved snapshot.
        Returns the snapshot data or None if no snapshot exists.
        """
        try:
            if not os.path.exists(self.snapshot_file):
                return None
            
            with open(self.snapshot_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception:
            return None
    
    def get_snapshot_timestamp(self) -> Optional[str]:
        """Get the timestamp of the last snapshot"""
        snapshot = self.load_snapshot()
        if snapshot and "meta" in snapshot:
            return snapshot["meta"].get("timestamp")
        return None
    
    def compare(self, current_services: List[AIService]) -> List[ServiceChange]:
        """
        Compare current service states with the saved snapshot.
        Returns a list of ServiceChange objects for services that changed.
        """
        changes = []
        saved_snapshot = self.load_snapshot()
        
        if not saved_snapshot or "services" not in saved_snapshot:
            return changes
        
        saved_services = saved_snapshot["services"]
        
        for service in current_services:
            if service.id in saved_services:
                saved_status = saved_services[service.id].get("status", ServiceStatus.UNKNOWN.value)
                current_status = service.status.value if service.status else ServiceStatus.UNKNOWN.value
                
                # Only report if status actually changed
                if saved_status != current_status:
                    changes.append(ServiceChange(
                        service_id=service.id,
                        service_name=service.name,
                        previous_status=saved_status,
                        current_status=current_status
                    ))
        
        return changes
    
    def has_snapshot(self) -> bool:
        """Check if a snapshot file exists"""
        return os.path.exists(self.snapshot_file)
    
    def delete_snapshot(self) -> bool:
        """Delete the snapshot file"""
        try:
            if os.path.exists(self.snapshot_file):
                os.remove(self.snapshot_file)
            return True
        except Exception:
            return False
    
    def get_reenabled_services(self, current_services: List[AIService]) -> List[ServiceChange]:
        """
        Get only the services that were re-enabled (the most important ones to notify about).
        These are typically services re-enabled by Windows Updates.
        """
        all_changes = self.compare(current_services)
        return [change for change in all_changes if change.was_reenabled]
