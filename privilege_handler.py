import ctypes
import os
import subprocess
import sys

from config_handler import CONFIG_PATH


class PrivilegeHandler:
    @staticmethod
    def is_admin():
        try:
            if sys.platform.startswith('win'):
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception as error:
            print(f"Error checking admin privileges: {error}")
            return False

    @staticmethod
    def run_as_admin():
        if sys.platform.startswith('win'):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        else:
            if os.path.exists('/usr/bin/pkexec'):
                subprocess.run(['pkexec', sys.executable] + sys.argv, env=os.environ)
                sys.exit(0)
            elif os.path.exists('/usr/bin/sudo'):
                subprocess.run(['sudo', '-E', sys.executable] + sys.argv)
                sys.exit(0)
            else:
                sys.exit(1)

    @staticmethod
    def require_admin_privileges():
        try:
            config_parent_directory = os.path.dirname(CONFIG_PATH)
            return not os.access(config_parent_directory, os.W_OK)
        except Exception as error:
            print(f"Error checking required privileges: {error}")
            return True