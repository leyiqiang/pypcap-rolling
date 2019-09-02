import yaml
import logging
import sys
from constants import *


class ConfigParser:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.config = yaml.load(file)

    @property
    def db_class_name(self):
        return self.config[DB_CLASS_NAME]

    @property
    def db_host(self):
        return self.config[DB_HOST]

    @property
    def db_port(self):
        return self.config[DB_PORT]

    @property
    def sniff_config(self):
        return self.config[SNIFF_CONFIG]

    @property
    def mode(self):
        return self.config[MODE]
