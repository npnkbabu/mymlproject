from src.data_collector import DataCollector
import os
import argparse
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
CONFIG_PATH = os.path.join(BASE_DIR,'config')
CONFIG_FILE = 'newsdatasource.json'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', dest='config',
                      help='Absolute path to configuration file.')
    args = parser.parse_args()
    if not args.config:
        print('no config file')
        exit()
    else:
        with open(os.path.join(CONFIG_PATH,CONFIG_FILE), 'r') as file:
            __config = json.load(file)
    __dataFetchConfig = __config.get('Collection')
    obj = DataCollector(__dataFetchConfig)