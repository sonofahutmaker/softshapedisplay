from utils import *

# save current servo pos in data structure
def saveServoPosition(servoNum, pos, positions):
    positions[servoNum] = pos
    return positions
