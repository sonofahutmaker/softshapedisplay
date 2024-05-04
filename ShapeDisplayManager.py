from adafruit_servokit import ServoKit 
import servo_utils
from utils import *

class ShapeDisplayManager:
    def __init__(self, num_servos):
        print("initializing shape display manager with num servos: ", num_servos)
        self.num_servos = num_servos
        self.kit = ServoKit(channels=self.num_servos)
        self.positions = [ZERO_ANGLE] * self.num_servos

    def zeroAllServos(self):
        for i in range(self.num_servos):
            servo_utils.zeroServo(i, self.kit)
    
    def getLatestPositionsGrid(self):
        return self.positions
    
    def getServoKit(self):
        return self.kit
    
    def updatePositionGrid(self, servoNum, newPos):
        self.positions = servo_utils.saveServoPosition(servoNum, newPos, self.positions)