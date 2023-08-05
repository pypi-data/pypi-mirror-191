from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

import config

Base = declarative_base()

engine = create_engine(f'{config.database_resource}:///{config.database_file}')

from output.contact_database import Contact
from output.site_database import Site, SitesContacts
from output.label_database import Label, LabelsContacts
