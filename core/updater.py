"""
Auto-update checker using GitHub Releases API
"""

import urllib.request
import json
from dataclasses import dataclass
from typing import Optional, Tuple
import threading


# Current version of the application
CURRENT_VERSION = "1.1.0"

# GitHub repository info
GITHUB_OWNER = "waar19"
GITHUB_REPO = "win-ai-tools"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"


@dataclass
class UpdateInfo:
    """Information about an available update"""
    version: str
    download_url: str
    release_notes: str
    html_url: str
    is_newer: bool


def parse_version(version_str: str) -> Tuple[int, ...]:
    """Parse version string to tuple for comparison"""
    # Remove 'v' prefix if present
    v = version_str.lstrip('v')
    try:
        return tuple(int(x) for x in v.split('.'))
    except:
        return (0, 0, 0)


def is_newer_version(current: str, latest: str) -> bool:
    """Check if latest version is newer than current"""
    current_tuple = parse_version(current)
    latest_tuple = parse_version(latest)
    return latest_tuple > current_tuple


def check_for_updates() -> Optional[UpdateInfo]:
    """
    Check GitHub for the latest release.
    Returns UpdateInfo if successful, None if failed.
    """
    try:
        # Create request with User-Agent (required by GitHub API)
        request = urllib.request.Request(
            GITHUB_API_URL,
            headers={
                'User-Agent': f'WinAIRemovalTool/{CURRENT_VERSION}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        
        # Fetch with timeout
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # Parse release info
        tag_name = data.get('tag_name', '')
        
        # Find Windows executable asset
        download_url = ""
        for asset in data.get('assets', []):
            if asset.get('name', '').endswith('.exe'):
                download_url = asset.get('browser_download_url', '')
                break
        
        # If no exe found, use the release page
        if not download_url:
            download_url = data.get('html_url', '')
        
        return UpdateInfo(
            version=tag_name,
            download_url=download_url,
            release_notes=data.get('body', ''),
            html_url=data.get('html_url', ''),
            is_newer=is_newer_version(CURRENT_VERSION, tag_name)
        )
        
    except Exception as e:
        print(f"Update check failed: {e}")
        return None


class UpdateChecker:
    """Async update checker with callback"""
    
    def __init__(self):
        self._thread: Optional[threading.Thread] = None
        self._result: Optional[UpdateInfo] = None
        self._callback = None
    
    def check_async(self, callback):
        """
        Check for updates in background thread.
        Calls callback(UpdateInfo) when done.
        """
        self._callback = callback
        self._thread = threading.Thread(target=self._check_thread, daemon=True)
        self._thread.start()
    
    def _check_thread(self):
        """Background thread for update check"""
        result = check_for_updates()
        self._result = result
        
        if self._callback and result:
            try:
                self._callback(result)
            except:
                pass
    
    def get_result(self) -> Optional[UpdateInfo]:
        """Get the result of the last check"""
        return self._result


def get_current_version() -> str:
    """Get current application version"""
    return CURRENT_VERSION
