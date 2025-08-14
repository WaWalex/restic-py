import json
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class MountDrive:
    device_uuid: str
    mount_location: str


@dataclass
class BackupItem:
    folder: str
    restic_tag: str


@dataclass
class BackupConfig:
    config_file_path: str
    mount_drives: List[MountDrive] = field(default_factory=list)
    pre_backup_cmd: Optional[str] = None
    backup: List[BackupItem] = field(default_factory=list)
    post_backup_cmd: Optional[str] = None
    run_post_backup_cmd_on_backup_failure: bool = False

    @classmethod
    def from_json(cls, config_file_path: str):
        try:
            with open(config_file_path, "r") as file:
                data = json.load(file)

            mount_drives_data = [MountDrive(**d) for d in data.get("mount_drives", [])]
            backup_data = [BackupItem(**d) for d in data.get("backup", [])]

            return cls(
                config_file_path=config_file_path,
                mount_drives=mount_drives_data,
                pre_backup_cmd=data.get("pre_backup_cmd"),
                backup=backup_data,
                post_backup_cmd=data.get("post_backup_cmd"),
                run_post_backup_cmd_on_backup_failure=data.get("run_post_backup_cmd_on_backup_failure", False),
            )

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Invalid JSON format in file: {config_file_path}", doc=None, pos=None)
        except TypeError as e:
            raise ValueError(f"JSON structure mismatch with dataclasses: {e}")

    def __str__(self):
        filename_with_ext = os.path.basename(self.config_file_path)
        filename_without_ext, _ = os.path.splitext(filename_with_ext)
        return filename_without_ext
