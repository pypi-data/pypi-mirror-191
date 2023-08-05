from dataclasses import dataclass, field
from typing import List


@dataclass
class Alias:
    name: str = ""
    open_data: List[str] = field(default_factory=list)

    def get_alias(self, alias_file_path: str):
        pass

    def alias_is_available(self):
        pass

    def create_alias(self, server_ip: str, alias_file_path: str):
        pass
