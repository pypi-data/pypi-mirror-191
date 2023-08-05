from dataclasses import dataclass


@dataclass
class Site:
    site_name: str

    #    contacts: list[Contact]

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def get_site_by_id(id_site):
        pass

    def get_contacts_by_site_id(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
