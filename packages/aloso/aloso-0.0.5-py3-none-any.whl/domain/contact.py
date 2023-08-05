from dataclasses import dataclass

from domain.label import Label
from domain.site import Site


@dataclass
class Contact:
    last_name: str
    first_name: str
    number: str
    mail: str
    address: str
    commentary: str
    sites: list[Site]
    labels: list[Label]

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def get_contact_by_id(id_contact):
        pass

    def get_labels_by_contact_name(self):
        pass

    def get_sites_by_contact_id(self):
        pass

    def get_labels_by_contact_id(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    @staticmethod
    def get_contacts_by_label(label: Label):
        pass
