from configparser import ConfigParser

config = ConfigParser()

def start_up():
    if not os.path.isfile('settings.ini'):
        write_settings()
    if os.path.isfile('settings.ini'):
        read_settings()

def write_settings():
    config.add_section('Configuartion')
    config.set('Configuartion', 'Save_Directory', '')
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

def read_settings():
    config.read('settings.ini')
    myPath = config.get('Configuartion', 'Save_Directory')

def set_path(path):
    myPath = path
    #update config
    config.read('settings.ini')
    config.set('Configuartion', 'Save_Directory', path)
    #Save new path
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)