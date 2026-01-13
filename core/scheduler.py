"""
Windows Task Scheduler integration for maintaining AI service settings
"""

import subprocess
import os
import sys
from typing import Tuple


# Task configuration
TASK_NAME = "WinAIRemovalTool_Maintenance"
TASK_DESCRIPTION = "Maintains AI service settings after Windows Updates"


def get_exe_path() -> str:
    """Get the path to the current executable or script"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        return sys.executable
    else:
        # Running as script
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main.py'))


def is_task_installed() -> bool:
    """Check if the scheduled task exists"""
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


def create_task() -> Tuple[bool, str]:
    """
    Create a scheduled task to run the app at login and daily.
    Returns (success, message)
    """
    try:
        exe_path = get_exe_path()
        
        # Determine the command based on whether we're running as exe or script
        if exe_path.endswith('.exe'):
            task_command = f'"{exe_path}" --silent'
        else:
            python_path = sys.executable
            task_command = f'"{python_path}" "{exe_path}" --silent'
        
        # Create task XML for more control
        task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>{TASK_DESCRIPTION}</Description>
    <Author>WinAIRemovalTool</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT1M</Delay>
    </LogonTrigger>
    <CalendarTrigger>
      <StartBoundary>2024-01-01T09:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
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
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{exe_path if exe_path.endswith('.exe') else sys.executable}</Command>
      <Arguments>{'' if exe_path.endswith('.exe') else f'"{exe_path}"'} --silent</Arguments>
    </Exec>
  </Actions>
</Task>'''
        
        # Write XML to temp file
        import tempfile
        xml_path = os.path.join(tempfile.gettempdir(), 'wart_task.xml')
        with open(xml_path, 'w', encoding='utf-16') as f:
            f.write(task_xml)
        
        # Create task from XML
        result = subprocess.run(
            ['schtasks', '/Create', '/TN', TASK_NAME, '/XML', xml_path, '/F'],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        # Clean up temp file
        try:
            os.remove(xml_path)
        except:
            pass
        
        if result.returncode == 0:
            return True, "Scheduled task created successfully"
        else:
            return False, f"Failed to create task: {result.stderr}"
            
    except Exception as e:
        return False, f"Error creating task: {str(e)}"


def remove_task() -> Tuple[bool, str]:
    """
    Remove the scheduled task.
    Returns (success, message)
    """
    try:
        result = subprocess.run(
            ['schtasks', '/Delete', '/TN', TASK_NAME, '/F'],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            return True, "Scheduled task removed"
        else:
            return False, f"Failed to remove task: {result.stderr}"
            
    except Exception as e:
        return False, f"Error removing task: {str(e)}"


def run_task_now() -> Tuple[bool, str]:
    """
    Run the scheduled task immediately.
    Returns (success, message)
    """
    try:
        result = subprocess.run(
            ['schtasks', '/Run', '/TN', TASK_NAME],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            return True, "Task started"
        else:
            return False, f"Failed to run task: {result.stderr}"
            
    except Exception as e:
        return False, f"Error running task: {str(e)}"


def get_task_status() -> dict:
    """Get information about the scheduled task"""
    return {
        "installed": is_task_installed(),
        "task_name": TASK_NAME,
        "description": TASK_DESCRIPTION
    }
