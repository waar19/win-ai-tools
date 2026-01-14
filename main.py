"""
Windows AI Removal Tool
Application to manage and remove AI services from Windows 11
"""

import sys
import argparse
import ctypes
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt


def is_admin():
    """Check if the application is running as administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_silent_mode(auto_restore=False):
    """
    Run in silent mode - check for changes and optionally auto-restore.
    Used by scheduled task to maintain settings after Windows Updates.
    
    Args:
        auto_restore: If True, automatically restore settings without user interaction
    """
    from core.change_monitor import ChangeMonitor
    from core.logger import activity_logger
    
    monitor = ChangeMonitor()
    
    # Log start
    activity_logger.log(
        level="INFO",
        action="MAINTENANCE",
        service_id="system",
        service_name="System",
        details="Silent maintenance started"
    )
    
    # Check if we have a baseline
    if not monitor.has_baseline():
        # First run - save current state as baseline
        monitor.save_current_state()
        print("Silent mode: First run - baseline snapshot saved")
        return 0
    
    # Check for changes
    report = monitor.check_for_changes()
    
    if report.is_empty:
        print("Silent mode: No changes detected")
        return 0
    
    # Found changes
    print(f"Silent mode: Detected {report.total_changes} changes")
    print(monitor.get_change_summary(report))
    
    if report.has_reenabled_services:
        activity_logger.log(
            level="WARNING",
            action="CHANGES_DETECTED",
            service_id="system",
            service_name="System",
            details=f"{report.reenabled_count} service(s) re-enabled by Windows Update"
        )
        
        if auto_restore:
            # Automatically restore settings
            success, fail, messages = monitor.auto_restore()
            
            print(f"Auto-restore: {success} restored, {fail} failed")
            for msg in messages:
                print(f"  {msg}")
            
            if success > 0:
                monitor.save_current_state()
                activity_logger.log(
                    level="INFO",
                    action="AUTO_RESTORE",
                    service_id="system",
                    service_name="System",
                    details=f"Auto-restored {success} services"
                )
            
            return 0 if fail == 0 else 1
        else:
            # Just notify - user will see alert when they open the app
            print("Silent mode: User will be notified on next app launch")
            return 0
    
    return 0


def run_gui_mode(start_minimized=False):
    """Run the graphical user interface"""
    from ui.main_window import MainWindow
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Check admin permissions
    if not is_admin():
        from core.i18n import t
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(t("permissions_required"))
        msg.setText(t("admin_required"))
        msg.setInformativeText(t("run_as_admin"))
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        # Continue anyway to show interface (read-only)
    
    window = MainWindow() # TODO: Pass start_minimized if window supports it, or handle here
    
    if not start_minimized:
        window.show()
    else:
        # Just ensure tray is setup (happens in specific method now)
        pass
        
    return app.exec()


def main():
    parser = argparse.ArgumentParser(description='Windows AI Removal Tool')
    parser.add_argument(
        '--silent', '-s',
        action='store_true',
        help='Run in silent mode without GUI (for scheduled tasks)'
    )
    parser.add_argument(
        '--minimized', '-m',
        action='store_true',
        help='Start application minimized to system tray'
    )
    parser.add_argument(
        '--auto-restore',
        action='store_true',
        dest='auto_restore',
        help='Automatically restore settings if changes detected (use with --silent)'
    )
    
    args = parser.parse_args()
    
    if args.silent:
        sys.exit(run_silent_mode(auto_restore=args.auto_restore))
    else:
        sys.exit(run_gui_mode(start_minimized=args.minimized))


if __name__ == "__main__":
    main()
