import sys
from typing import List

from colorama import Fore, Style, init

import core
import utils
from models.backup_config import BackupConfig


def run_all_configs() -> None:
    configs: List[BackupConfig] = utils.find_backup_configs()
    print(f"{Fore.LIGHTCYAN_EX}Found {len(configs)} backup configurations!{Style.RESET_ALL}")
    for config in configs:
        print(f"  - {Fore.MAGENTA}{config}{Style.RESET_ALL}")
    print()
    for config in configs:
        run_config(config)


def run_config(config: BackupConfig) -> None:
    print(f"{Fore.YELLOW}--- Starting {Style.BRIGHT}{config}{Style.NORMAL} Restic Backup using Restic-Py ---")

    if config.mount_drives:
        core.mount_drive(config.mount_drives)

    if config.pre_backup_cmd:
        core.run_cmd(config.pre_backup_cmd)

    if config.backup:
        try:
            for backup_item in config.backup:
                core.backup(backup_item)
        except Exception as e:
            print(f"{Fore.RED}Error during backup: {e}")
            if config.run_post_backup_cmd_on_backup_failure and config.post_backup_cmd:
                core.run_cmd(config.post_backup_cmd)
            return

    if config.post_backup_cmd:
        core.run_cmd(config.post_backup_cmd)


if __name__ == "__main__":
    init(autoreset=True)

    print(f"{Fore.MAGENTA}ResticPy - https://github.com/WaWalex/restic-py{Style.RESET_ALL}")

    argv_len = len(sys.argv)
    if argv_len == 1:
        print(f"{Fore.LIGHTCYAN_EX}(running all backup configs){Style.RESET_ALL}\n")
        run_all_configs()
    else:
        print(f"{Fore.RED}Invalid arguments!{Style.RESET_ALL}")
        print(f"{Fore.RED}\t- no args: run all backup configs{Style.RESET_ALL}")
