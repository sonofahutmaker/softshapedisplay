import configparser

# data range
DATA_LOW = 0
DATA_HIGH = 1

# CONSTANTS FOR CONT ROTATION SERVOS
# shaft consts in mm
# length of pusher shaft in mm, not including length of servo holder (6 inches)
SHAFT_LENGTH_MM = 152.4
# shafts will be zeroed to be halfway extended
SHAFT_BOTTOM_POS = -SHAFT_LENGTH_MM/2
SHAFT_TOP_POS = SHAFT_LENGTH_MM/2
# time for gear to turn and shaft to move from bottom to top pos in secs at full speed
WHOLE_SHAFT_TRAVERSAL_TIME = 2.1
FORWARD_THROTTLE = -1 # full positive throttle value
BACKWARD_THROTTLE = 1 # full negative throttle value
ZERO_THROTTLE = 0.02
SPEED = 1 # float value between 0.0 - 1.0

# ANGLE RANGE CONSTANTS FOR STANDARD SERVOS
ZERO_ANGLE = 90
LOWEST_ANGLE = 180
HIGHEST_ANGLE = 0

DEFAULTS = {'data_range': ["0.0", "1.0"], 
            'angle_range': ["180", "0"]}

# must have IP address and port num on first config
def generate_ini(args):
    #if not in args, look in ini
    #if not in ini, look to defaults
    args_keys = ['ip', 'port', 'data_range','angle_range']
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

# STANDARD SERVO FUNCTION
def dataValueToAngle(val):
    angle = (val - DATA_LOW) * (HIGHEST_ANGLE - LOWEST_ANGLE) / (
        DATA_HIGH - DATA_LOW
    ) + LOWEST_ANGLE
    return angle

# CONT. ROTATION SERVO FUNCTIONS BELOW
# convert data value to shaft top position in mm
# middle of data range == 0mm up/down=
def dataValueToShaftHeight(val):
    newPos = (val - DATA_LOW) * (SHAFT_TOP_POS - SHAFT_BOTTOM_POS) / (
        DATA_HIGH - DATA_LOW
    ) + SHAFT_BOTTOM_POS
    return newPos

def getDistanceToTravel(currPosition, nextPosition):
    return nextPosition - currPosition

def getTimeToPosition(distance):
    # may have to be adjusted to account for variable force on shaft as silicone stretches
    travelTime = WHOLE_SHAFT_TRAVERSAL_TIME * (abs(distance)/SHAFT_LENGTH_MM) * SPEED
    return travelTime

def getThrottle(distance):
    if distance < 0: # traveling down
        return BACKWARD_THROTTLE * SPEED
    elif distance > 0: #travling up
        return FORWARD_THROTTLE * SPEED
    # if somehow distance is actually the same as before
    return ZERO_THROTTLE
