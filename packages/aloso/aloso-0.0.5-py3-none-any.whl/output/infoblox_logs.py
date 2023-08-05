from dataclasses import dataclass

from domain.alias import Alias


@dataclass
class InfoBlox(Alias):

    def printer(self):
        print("InfoBlox")
