"""Platform utilities for cross-platform support."""

import platform
import sys
import subprocess
from pathlib import Path


class PlatformInfo:
    """Provides cross-platform information."""
    
    @staticmethod
    def get_system():
        """Get system type: 'Windows', 'Linux', 'Darwin' (macOS)."""
        return platform.system()
    
    @staticmethod
    def is_windows():
        """Check if running on Windows."""
        return platform.system() == 'Windows'
    
    @staticmethod
    def is_linux():
        """Check if running on Linux."""
        return platform.system() == 'Linux'
    
    @staticmethod
    def is_macos():
        """Check if running on macOS."""
        return platform.system() == 'Darwin'
    
    @staticmethod
    def get_venv_activate_command():
        """Get the correct venv activation command for current platform."""
        venv_path = Path(__file__).parent.parent / 'venv'
        
        if PlatformInfo.is_windows():
            return f"{venv_path}\\Scripts\\activate.bat"
        else:
            return f"source {venv_path}/bin/activate"
    
    @staticmethod
    def get_python_executable():
        """Get the current Python executable path."""
        return sys.executable
    
    @staticmethod
    def require_admin():
        """Check if running with admin/root privileges."""
        if PlatformInfo.is_windows():
            try:
                import ctypes
                return ctypes.windll.shell.IsUserAnAdmin()
            except Exception:
                return False
        else:
            # Unix-like systems
            return subprocess.call(['id', '-u'], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL) == 0
    
    @staticmethod
    def get_network_interfaces():
        """Get list of available network interfaces."""
        try:
            from scapy.all import get_if_list
            return get_if_list()
        except Exception:
            return []
    
    @staticmethod
    def print_system_info():
        """Print system information."""
        print(f"System: {PlatformInfo.get_system()}")
        print(f"Python: {platform.python_version()}")
        print(f"Executable: {PlatformInfo.get_python_executable()}")
        print(f"Admin/Root: {'Yes' if PlatformInfo.require_admin() else 'No'}")
        
        interfaces = PlatformInfo.get_network_interfaces()
        if interfaces:
            print(f"Network Interfaces: {', '.join(interfaces)}")
