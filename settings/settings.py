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
    config.set('Configuartion', 'Amount', '20')
    config.set('Configuartion', 'Max_amount', '100')
    config.set('Configuartion', 'Min_amount', '60')
    config.add_section('OneTimes')
    config.set('OneTimes', 'first_duplication', 'True')
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)

def read_settings():
    config.read('settings/settings.ini')
    sav_dir = config.get('Configuartion', 'Save_Directory')
    return sav_dir

def get_default_values():
    config.read('settings/settings.ini')
    amount = config.get('Configuartion', 'Amount')
    max_amount = config.get('Configuartion', 'Max_amount')
    min_amount = config.get('Configuartion', 'Min_amount')
    return int(amount), int(max_amount), int(min_amount)

def set_default_values(amount, max_amount, min_amount):
    config.read('settings/settings.ini')
    config.set('Configuartion', 'Amount', amount)
    config.set('Configuartion', 'Max_amount', max_amount)
    config.set('Configuartion', 'Min_amount', min_amount)
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)

def get_first_duplication():
    config.read('settings/settings.ini')
    first_duplication_status = config.get('OneTimes', 'first_duplication')
    if first_duplication_status == 'True':
        return True
    elif first_duplication_status == 'False':
        return False

def first_duplication_warning_done():
    config.read('settings/settings.ini')
    config.set('OneTimes', 'first_duplication', 'False')
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)


def set_path(path):
    sav_dir = path
    #update config
    config.read('settings/settings.ini')
    config.set('Configuartion', 'Save_Directory', path)
    #Save new path
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)