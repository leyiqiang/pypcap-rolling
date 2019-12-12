import yaml
from constants import *
import logging
import sys
from constants import *


class ConfigParser:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.config = yaml.load(file)

    @property
    def from_db_class_name(self):
        return self.config[FROM_DB_CLASS_NAME]

    @property
    def to_db_class_name(self):
        return self.config[TO_DB_CLASS_NAME]

    @property
    def from_db_host(self):
        return self.config[FROM_DB_HOST]

    @property
    def to_db_host(self):
        return self.config[TO_DB_HOST]

    @property
    def from_db_port(self):
        return self.config[FROM_DB_PORT]

    @property
    def to_db_port(self):
        return self.config[TO_DB_PORT]

    @property
    def time_before(self):
        time_before = int(self.config[TIME_BEFORE])
        return time_before
