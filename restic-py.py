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
    print(f"{Fore.YELLOW}--- Starting {Style.BRIGHT}{config}{Style.NORMAL} Restic Backup using Restic-Py ---{Style.RESET_ALL}")

    if config.mount_drives:
        core.mount_drive(config.mount_drives)

    # Add Restic backup logic here


if __name__ == "__main__":
    init(autoreset=True)

    print(f"{Fore.MAGENTA}ResticPy - https://github.com/WaWalex/restic-py{Style.RESET_ALL}")

    argv_len = len(sys.argv)
    if argv_len == 1:
        print(f"{Fore.LIGHTCYAN_EX}(no args passed, running all backup configs){Style.RESET_ALL}\n")
        run_all_configs()
    elif argv_len == 2:
        print(f"{Fore.LIGHTCYAN_EX}(running config: {sys.argv[1]}){Style.RESET_ALL}\n")

        try:
            config_obj = BackupConfig.from_json(f"./config/{sys.argv[1]}.json")
            run_config(config_obj)
        except (FileNotFoundError, ValueError) as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Invalid arguments!{Style.RESET_ALL}")
        print(f"{Fore.RED}\t- no args: run all backup configs{Style.RESET_ALL}")
        print(f"{Fore.RED}\t- 1 arg: run backup config name (without extension){Style.RESET_ALL}")
