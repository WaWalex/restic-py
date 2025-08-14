import os
import subprocess
import sys
from typing import List

from colorama import Fore, Style

from models.backup_config import BackupItem, MountDrive, ResticConfiguration


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


def run_cmd(cmd: str) -> None:
    print(f"{Fore.YELLOW}--- Running command: {Style.BRIGHT}{cmd}{Style.NORMAL} ---")

    try:
        subprocess.run(cmd, shell=True, check=True, executable="/bin/bash", stdout=sys.stdout, stderr=sys.stderr)
        print(f"{Fore.GREEN}Command executed successfully.{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Command failed with exit code {e.returncode}{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: The specified executable was not found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")


def backup(restic_configuration: ResticConfiguration, backup_item: BackupItem) -> None:
    print(f"{Fore.CYAN}--- Starting Restic backup for folder: {Style.BRIGHT}{backup_item.folder}{Style.NORMAL} ---")

    try:
        command = [
            "restic",
            "-r",
            restic_configuration.repository_location,
            "--password-file",
            restic_configuration.repository_password,
            "backup",
            backup_item.folder,
            "--tag",
            backup_item.restic_tag,
        ]
        subprocess.run(command, check=True, stdout=sys.stdout, stderr=sys.stderr)
        print(f"{Fore.GREEN}Restic backup completed successfully.{Style.RESET_ALL}")
    except FileNotFoundError:
        print(
            f"{Fore.RED}Error: 'restic' command not found. Please ensure Restic is installed and in your PATH.{Style.RESET_ALL}"
        )
        raise
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Restic backup failed with exit code {e.returncode}.{Style.RESET_ALL}")
        raise
