from dataclasses import dataclass


@dataclass
class Certificate:
    country: str = ""
    state: str = ""
    locality: str = ""
    organization: str = ""
    unit: str = ""
    common: str = ""
    mail: str = ""

    def renew(self):
        pass
