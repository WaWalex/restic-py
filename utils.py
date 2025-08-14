import os
from typing import List

from models.backup_config import BackupConfig


def find_backup_configs(directory: str = "./config") -> List[BackupConfig]:
    configs = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".json"):
                full_path = os.path.join(dirpath, filename)
                configs.append(BackupConfig.from_json(full_path))
    return configs
