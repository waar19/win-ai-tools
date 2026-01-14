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


def run_silent_mode():
    """
    Run in silent mode - apply settings without UI.
    Used by scheduled task to maintain settings after Windows Updates.
    """
    from core.detector import AIServiceDetector
    from core.manager import AIServiceManager
    from core.logger import activity_logger
    from core.ai_services import ServiceStatus
    
    detector = AIServiceDetector()
    manager = AIServiceManager()
    
    # Detect all services
    services = detector.detect_all()
    
    # Re-apply disabled settings for services that should be disabled
    # (based on registry backup or previous state)
    activity_logger.log(
        activity_logger.LogLevel.INFO if hasattr(activity_logger, 'LogLevel') else None,
        "MAINTENANCE",
        "system",
        "System",
        "Silent maintenance started"
    )
    
    # For now, just log the current state
    enabled_count = sum(1 for s in services if s.status == ServiceStatus.ENABLED)
    print(f"Silent mode: Found {len(services)} services, {enabled_count} enabled")
    
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
    
    args = parser.parse_args()
    
    if args.silent:
        sys.exit(run_silent_mode())
    else:
        sys.exit(run_gui_mode(start_minimized=args.minimized))


if __name__ == "__main__":
    main()
