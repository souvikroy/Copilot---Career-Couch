import configparser, os

CONFIG_FILE = './config/config-local.ini' if os.path.exists("./config/config-local.ini") else './config/config.ini'

class Base:

    def __init__(self):
        self.is_local_env = True if 'local' in CONFIG_FILE else False
        self.cfg = self.setup_config(CONFIG_FILE)

    def setup_config(self, config_filename):
        configParser   = configparser.RawConfigParser()   
        configParser.read(config_filename)
        return configParser