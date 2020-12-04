import os
from configparser import ConfigParser

config = ConfigParser()


def start_up():
    if not os.path.isfile('settings/settings.ini'):
        write_settings()
    if os.path.isfile('settings/settings.ini'):
        read_settings()


def write_settings():
    config.add_section('Configuration')
    config.set('Configuration', 'Save_Directory', '')
    config.set('Configuration', 'Amount', '20')
    config.set('Configuration', 'Max_amount', '100')
    config.set('Configuration', 'Min_amount', '60')
    config.set('Configuration', 'Lewd', 'normal')
    config.set('Configuration', 'Wholesome', 'normal')
    config.set('Configuration', 'Duplication', 'normal')
    config.add_section('OneTimes')
    config.set('OneTimes', 'first_duplication', 'True')
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)


def read_settings():
    config.read('settings/settings.ini')
    sav_dir = config.get('Configuration', 'Save_Directory')
    return sav_dir


def get_default_values():
    config.read('settings/settings.ini')
    amount = config.get('Configuration', 'Amount')
    max_amount = config.get('Configuration', 'Max_amount')
    min_amount = config.get('Configuration', 'Min_amount')
    lewd = config.get('Configuration', 'Lewd')
    wholesome = config.get('Configuration', 'Wholesome')
    duplication = config.get('Configuration', 'Duplication')
    default_values = DefaultValues(int(amount), int(max_amount), int(min_amount), lewd, wholesome, duplication)
    return default_values

def set_default_values(amount, max_amount, min_amount, lewd, wholesome, duplication):
    config.read('settings/settings.ini')
    config.set('Configuration', 'Amount', amount)
    config.set('Configuration', 'Max_amount', max_amount)
    config.set('Configuration', 'Min_amount', min_amount)
    config.set('Configuration', 'Lewd', lewd)
    config.set('Configuration', 'Wholesome', wholesome)
    config.set('Configuration', 'Duplication', duplication)
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
    # update config
    config.read('settings/settings.ini')
    config.set('Configuration', 'Save_Directory', path)
    # Save new path
    with open('settings/settings.ini', 'w') as configfile:
        config.write(configfile)


class DefaultValues:
    def __init__(self, amount, max_amount, min_amount, lewd, wholesome, duplication):
        self.amount = amount
        self.max_amount = max_amount
        self.min_amount = min_amount
        self.lewd = lewd
        self.wholesome = wholesome
        self.duplication = duplication