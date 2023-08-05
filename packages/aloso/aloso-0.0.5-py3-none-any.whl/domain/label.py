from dataclasses import dataclass


@dataclass
class Label:
    label_name: str

    #    contacts: list[Contact]

    @staticmethod
    def get_all():
        pass

    @staticmethod
    def get_label_by_id(id_label):
        pass

    def get_contacts_by_label_id(self):
        pass

    def create(self):
        pass

    def delete(self):
        pass
