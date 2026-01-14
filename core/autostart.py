"""
Auto-start management using Windows Task Scheduler
Allows the app to start minimized with admin privileges without UAC prompt at login
"""

import subprocess
import os
import sys
from typing import Tuple

TASK_NAME = "WinAIRemovalTool_Tray"
TASK_DESCRIPTION = "Starts Windows AI Removal Tool minimized in system tray"

def get_exe_path() -> str:
    """Get the path to the current executable or script"""
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))

def is_autostart_enabled() -> bool:
    """Check if auto-start task exists"""
    try:
        result = subprocess.run(
            ['schtasks', '/Query', '/TN', TASK_NAME],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.returncode == 0
    except Exception:
        return False

def set_autostart(enabled: bool) -> Tuple[bool, str]:
    """Enable or disable auto-start"""
    if enabled:
        return _create_task()
    else:
        return _remove_task()

def _create_task() -> Tuple[bool, str]:
    """Create the scheduled task"""
    try:
        exe_path = get_exe_path()
        
        # Command execution
        if exe_path.endswith('.exe'):
            cmd = exe_path
            args = "--minimized"
        else:
            cmd = sys.executable
            args = f'"{exe_path}" --minimized'
            
        # XML Definition
        task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>{TASK_DESCRIPTION}</Description>
    <Author>WinAIRemovalTool</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{cmd}</Command>
      <Arguments>{args}</Arguments>
    </Exec>
  </Actions>
</Task>'''
        
        # Write XML to temp
        import tempfile
        xml_path = os.path.join(tempfile.gettempdir(), 'wart_autostart.xml')
        with open(xml_path, 'w', encoding='utf-16') as f:
            f.write(task_xml)
            
        # Create task
        result = subprocess.run(
            ['schtasks', '/Create', '/TN', TASK_NAME, '/XML', xml_path, '/F'],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Cleanup
        try:
            os.remove(xml_path)
        except:
            pass
            
        if result.returncode == 0:
            return True, "Auto-start enabled"
        else:
            return False, f"Failed to enable auto-start: {result.stderr}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def _remove_task() -> Tuple[bool, str]:
    """Remove the scheduled task"""
    try:
        result = subprocess.run(
            ['schtasks', '/Delete', '/TN', TASK_NAME, '/F'],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            return True, "Auto-start disabled"
        else:
            return False, f"Failed to disable: {result.stderr}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
