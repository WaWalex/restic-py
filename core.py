import os
import subprocess
import sys
from typing import List, Optional, Union

from colorama import Fore, Style

from models.backup_config import BackupItem, MountDrive, ResticConfiguration


def _execute_command(
    cmd: Union[str, List[str]], success_msg: str, error_msg: str, shell: bool = False, **kwargs
) -> None:
    print(f"{Fore.YELLOW}Executing: {Style.BRIGHT}{' '.join(cmd) if isinstance(cmd, list) else cmd}{Style.RESET_ALL}")
    try:
        subprocess.run(cmd, check=True, shell=shell, stdout=sys.stdout, stderr=sys.stderr, **kwargs)
        print(f"{Fore.GREEN}{success_msg}{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}{error_msg}. Command failed with exit code {e.returncode}{Style.RESET_ALL}")
        raise
    except FileNotFoundError:
        print(f"{Fore.RED}{error_msg}. Command not found. Please ensure it is in your system's PATH.{Style.RESET_ALL}")
        raise
    except Exception as e:
        print(f"{Fore.RED}{error_msg}. An unexpected error occurred: {e}{Style.RESET_ALL}")
        raise


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
        mount_command = ["sudo", "mount", "-U", device_uuid, mount_point]
        try:
            _execute_command(
                cmd=mount_command,
                success_msg=f"Drive {device_uuid} successfully mounted to {mount_point}.",
                error_msg=f"Error: Failed to mount drive {device_uuid} to {mount_point}.",
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            # Re-printing the error output for this specific case
            print(f"{Fore.RED}Command output: {e.stdout.strip()}{Style.RESET_ALL}")
            print(f"{Fore.RED}Error output: {e.stderr.strip()}{Style.RESET_ALL}")
        except e:
            return


def run_cmd(cmd: str) -> None:
    _execute_command(
        cmd=cmd,
        success_msg="Command executed successfully.",
        error_msg="Error: Command failed",
        shell=True,
        executable="/bin/bash",
    )


def backup(restic_configuration: ResticConfiguration, backup_item: BackupItem) -> None:
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

    _execute_command(
        cmd=command, success_msg="Restic backup completed successfully.", error_msg="Error: Restic backup failed"
    )
