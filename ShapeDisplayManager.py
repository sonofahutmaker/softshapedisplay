from adafruit_servokit import ServoKit 
import servo_utils
from utils import *
from StandardServo import StandardServo
from ContinuousServo import ContinuousServo

class ShapeDisplayManager:
    def __init__(self, num_servos, servo_type):
        print("initializing shape display manager with num servos: ", num_servos)
        self.num_servos = num_servos
        self.kit = ServoKit(channels=self.num_servos)
        if servo_type == ServoType.STANDARD.value:
            self.servos = StandardServo()
        elif servo_type == ServoType.CONT.value:
            self.servos = ContinuousServo()
        self.positions = [self.servos.zero_val] * self.num_servos 
    
    def zeroAllServos(self): #may need to change to await when cont servos
        for i in range(self.num_servos):
            self.servos.zeroServo(i, self.kit)
    
    def getLatestPositionsGrid(self):
        return self.positions
    
    def getServoKit(self):
        return self.kit
    
    def updatePositionGrid(self, servoNum, newPos):
        self.positions = servo_utils.saveServoPosition(servoNum, newPos, self.positions)