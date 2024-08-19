import configparser
from enum import Enum

class ServoType(Enum):
    STANDARD = "standard"
    CONT = "cont"

DEFAULTS = {'data_range': ["0.0", "1.0"], 
            'angle_range': ["180", "0"],
            'servo_type': ServoType.STANDARD.value,
            'shaft_len': "152.4",
            'traversal_time': "2.1",
            'forward_throttle': "-1",
            'backward_throttle': "1",
            'zero_throttle': "0.02",
            'speed': "1"
            }

def retrieve_config(key, cat="DEFAULT"):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if cat in config and key in config[cat]:
        return config[cat][key]
    return None

# must have IP address and port num on first config
def generate_ini(args):
    #if not in args, look in ini
    #if not in ini, look to defaults
    args_keys = ['ip', 'port', 'data_range','angle_range', 'servo_type',
                'shaft_len', 'traversal_time', 'forward_throttle',
                'backward_throttle', 'zero_throttle', 'speed', 'num_servos']
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'DEFAULT' not in config:
        config['DEFAULT'] = {}
    argsdict = vars(args)
    for key in args_keys:
        if argsdict[key]:
            if isinstance(argsdict[key], list):
                config[key] = {}
                config[key]["low"] = argsdict[key][0]
                config[key]["high"] = argsdict[key][1]
            else:
                config['DEFAULT'][key] = argsdict[key]
        else:
            if key not in config and key not in config['DEFAULT']:
                default = DEFAULTS[key]
                if isinstance(default, list):
                    config[key] = {}
                    config[key]["low"] = default[0]
                    config[key]["high"] = default[1]
                else:
                    config['DEFAULT'][key] = default

    with open('config.ini', 'w') as configfile:
        config.write(configfile)