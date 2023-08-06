# A set of string format helper functions.

def hhmm(seconds):
    hours = int(seconds / 3600)
    minutes = int(round(seconds % 3600)/60)
    return '{:02d}:{:02d}'.format(hours, minutes)

def temperature_5_digits(temperature):
    if not temperature:
        return ' --.-'
    else:
        return '{: 5.1F}'.format(temperature)

def dt_string(timestamp):
    '''Format a datetime object in the preferred format (no microseconds).'''
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
