import os
import subprocess
from typing import List

from colorama import Fore, Style

from models.backup_config import MountDrive


def mount_drive(drive: MountDrive) -> None:
    mount_point = drive.mount_location
    device_uuid = drive.device_uuid

    print(f"{Fore.YELLOW}Checking if mount point {mount_point} exists...{Style.RESET_ALL}")

    if not os.path.isdir(mount_point):
        print(f"{Fore.CYAN}Mount point {mount_point} does not exist. Creating it...{Style.RESET_ALL}")
        try:
            os.makedirs(mount_point)
            print(f"{Fore.GREEN}Mount point {mount_point} created successfully.{Style.RESET_ALL}")
        except OSError as e:
            print(f"{Fore.RED}Error: Failed to create mount point {mount_point}. {e}{Style.RESET_ALL}")
            return
    else:
        print(f"{Fore.GREEN}Mount point {mount_point} already exists.{Style.RESET_ALL}")

    if os.path.ismount(mount_point):
        print(f"{Fore.CYAN}Drive with UUID {device_uuid} is already mounted at {mount_point}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.MAGENTA}Attempting to mount drive with UUID {device_uuid} to {mount_point}...{Style.RESET_ALL}")

        mount_command = ["sudo", "mount", "-U", device_uuid, mount_point]

        try:
            subprocess.run(mount_command, check=True, capture_output=True, text=True)
            print(f"{Fore.GREEN}Drive {device_uuid} successfully mounted to {mount_point}.{Style.RESET_ALL}")
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}Error: Failed to mount drive {device_uuid} to {mount_point}.{Style.RESET_ALL}")
            print(f"{Fore.RED}Command output: {e.stdout.strip()}{Style.RESET_ALL}")
            print(f"{Fore.RED}Error output: {e.stderr.strip()}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(
                f"{Fore.RED}Error: The 'mount' command was not found. Please ensure it is in your system's PATH.{Style.RESET_ALL}"
            )
