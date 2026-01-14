"""
Change Monitor
Orchestrates the detection of changes in AI service settings
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass

from .detector import AIServiceDetector
from .manager import AIServiceManager
from .state_snapshot import StateSnapshot, ServiceChange
from .ai_services import AIService, ServiceStatus
from .logger import activity_logger


@dataclass
class ChangeReport:
    """Summary of detected changes"""
    total_changes: int
    reenabled_count: int
    disabled_count: int
    changes: List[ServiceChange]
    snapshot_timestamp: Optional[str]
    
    @property
    def has_reenabled_services(self) -> bool:
        """Check if any services were re-enabled (likely by Windows Update)"""
        return self.reenabled_count > 0
    
    @property
    def is_empty(self) -> bool:
        """Check if there are no changes"""
        return self.total_changes == 0


class ChangeMonitor:
    """
    Monitors and manages changes in AI service states.
    Detects when Windows Updates re-enable services and allows restoration.
    """
    
    def __init__(self):
        self.detector = AIServiceDetector()
        self.manager = AIServiceManager()
        self.snapshot = StateSnapshot()
    
    def check_for_changes(self) -> ChangeReport:
        """
        Detect current state and compare with saved snapshot.
        Returns a ChangeReport with all detected changes.
        """
        # Get current service states
        current_services = self.detector.detect_all()
        
        # Compare with snapshot
        changes = self.snapshot.compare(current_services)
        
        # Count re-enabled vs disabled
        reenabled = sum(1 for c in changes if c.was_reenabled)
        disabled = sum(1 for c in changes if not c.was_reenabled)
        
        return ChangeReport(
            total_changes=len(changes),
            reenabled_count=reenabled,
            disabled_count=disabled,
            changes=changes,
            snapshot_timestamp=self.snapshot.get_snapshot_timestamp()
        )
    
    def get_change_summary(self, report: ChangeReport) -> str:
        """
        Get a human-readable summary of the changes.
        """
        if report.is_empty:
            return "No changes detected since last snapshot."
        
        lines = []
        
        if report.reenabled_count > 0:
            lines.append(f"⚠️ {report.reenabled_count} service(s) were re-enabled:")
            for change in report.changes:
                if change.was_reenabled:
                    lines.append(f"  • {change.service_name}")
        
        if report.disabled_count > 0:
            lines.append(f"✓ {report.disabled_count} service(s) were disabled:")
            for change in report.changes:
                if not change.was_reenabled:
                    lines.append(f"  • {change.service_name}")
        
        return "\n".join(lines)
    
    def auto_restore(self, changes: List[ServiceChange] = None) -> Tuple[int, int, List[str]]:
        """
        Automatically restore services to their previous (disabled) state.
        Only restores services that were re-enabled.
        
        Returns (success_count, fail_count, messages)
        """
        if changes is None:
            report = self.check_for_changes()
            changes = [c for c in report.changes if c.was_reenabled]
        
        success_count = 0
        fail_count = 0
        messages = []
        
        for change in changes:
            if not change.was_reenabled:
                continue
            
            # Find the service
            service = next(
                (s for s in self.detector.services if s.id == change.service_id),
                None
            )
            
            if not service:
                fail_count += 1
                messages.append(f"Service not found: {change.service_id}")
                continue
            
            # Disable the service
            success, msg = self.manager.disable_service(service)
            
            if success:
                success_count += 1
                messages.append(f"✓ Restored: {service.name}")
                activity_logger.log(
                    level="INFO",
                    action="AUTO_RESTORE",
                    service_id=service.id,
                    service_name=service.name,
                    details=f"Auto-restored after Windows Update"
                )
            else:
                fail_count += 1
                messages.append(f"✗ Failed: {service.name} - {msg}")
        
        return success_count, fail_count, messages
    
    def save_current_state(self) -> Tuple[bool, str]:
        """
        Save current service states as the new baseline snapshot.
        Call this after user makes changes to remember their preferences.
        """
        services = self.detector.detect_all()
        return self.snapshot.save_snapshot(services)
    
    def has_baseline(self) -> bool:
        """Check if we have a saved baseline to compare against"""
        return self.snapshot.has_snapshot()
    
    def accept_current_state(self) -> Tuple[bool, str]:
        """
        Accept the current state as the new baseline.
        Call this when user wants to keep the changes made by Windows Update.
        """
        return self.save_current_state()
