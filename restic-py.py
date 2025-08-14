import sys
from typing import List

from colorama import Fore, Style

import utils


def run_all_configs() -> None:
    configs: List[utils.BackupConfig] = utils.find_backup_configs()
    print(Fore.LIGHTMAGENTA_EX + f"Found {len(configs)} backup configurations!")
    for config in configs:
        print(f"  - {config}")
    print()
    for config in configs:
        run_config(config)


def run_config(config: utils.BackupConfig) -> None:
    print(Fore.YELLOW + f"--- Starting {Style.BRIGHT}{config}{Style.NORMAL} Restic Backup ---")
    # TODO


if __name__ == "__main__":
    print(Fore.MAGENTA + "ResticPy - https://github.com/WaWalex/restic-py")

    argv_len = len(sys.argv)
    if argv_len == 1:
        print(Fore.LIGHTMAGENTA_EX + "(no args passed, running all backup configs)\n")
        run_all_configs()
    elif argv_len == 2:
        print(Fore.LIGHTMAGENTA_EX + f"(running config: {sys.argv[1]})\n")
        run_config(sys.argv[1])
    else:
        print(
            Fore.RED
            + "Invalid arguments!\n\t- no args: run all the backup configs\n\t- 1 arg: run backup config name (without extension) to run"
        )

    print(Fore.RESET)
