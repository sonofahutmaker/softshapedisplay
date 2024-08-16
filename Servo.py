from utils import *

class Servo:
    def __init__(self):
        self.data_low = float(retrieve_config("low", "data_range"))
        self.data_high = float(retrieve_config("high", "data_range"))

    # save current servo pos in data structure
    def saveServoPosition(servoNum, pos, positions):
        positions[servoNum] = pos
        return positions
    
    