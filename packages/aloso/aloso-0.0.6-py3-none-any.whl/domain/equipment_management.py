from dataclasses import dataclass
from ftplib import FTP
from typing import ClassVar

import config


@dataclass
class TypeEquipments:
    name: str = ""


@dataclass
class Equipments:
    name: str = ""
    ip: str = ""
    mac: str = ""
    equipment_type: TypeEquipments = TypeEquipments()
    equipment_dict: ClassVar[dict] = {}

    @staticmethod
    def ssh_open_connection(equipment_name):
        pass

    @staticmethod
    def load_all(file_path: str):
        pass

    @staticmethod
    def ftp_get_config_files():
        pass

    @staticmethod
    def new_name_file_from_ftp_dir(file_name: str):
        pass

    @staticmethod
    def get_date_from_ftp_file(file_name: str):
        pass

    @staticmethod
    def recent_date_detection(ftp: FTP):
        pass

    def server_exists(self):
        pass
