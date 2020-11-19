from configparser import ConfigParser
import os

config = ConfigParser()

def start_up():
    if not os.path.isfile('settings/settings.ini'):
        write_settings()
    if os.path.isfile('settings/settings.ini'):
        read_settings()

def write_settings():
    config.add_section('Configuartion')
    config.set('Configuartion', 'Save_Directory', '')
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)

def read_settings():
    config.read('settings/settings.ini')
    sav_dir = config.get('Configuartion', 'Save_Directory')
    return sav_dir

def set_path(path):
    sav_dir = path
    #update config
    config.read('settings/settings.ini')
    config.set('Configuartion', 'Save_Directory', path)
    #Save new path
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)