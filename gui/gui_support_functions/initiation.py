from settings import settings
    
def grab_default_values():
    default_values = settings.get_default_values()
    return default_values

def wholesome_toggle_init():
    wholesome = settings.get_default_values().wholesome
    return wholesome

def lewd_toggle_init():
    lewd = settings.get_default_values().lewd
    return lewd

def duplication_toggle_init():
    duplication = settings.get_default_values().duplication
    return duplication