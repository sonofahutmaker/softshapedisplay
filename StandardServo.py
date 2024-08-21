from Servo import Servo
from utils import *

# class instantiated when using standard rotational servos
class StandardServo(Servo):
    def __init__(self):
        super().__init__()
        # pulling config values for angle range
        self.lowest_angle = float(retrieve_config('low', 'angle_range'))
        self.highest_angle = float(retrieve_config('high', 'angle_range'))
        self.zero_angle = (max(self.lowest_angle, self.highest_angle) - 
                           min(self.lowest_angle, self.highest_angle))/2
        self.zero_val = self.zero_angle
        
    async def zeroServo(self, servoNum, servoKit):
        print("zeroing servonum ", servoNum)
        servoKit.servo[servoNum].angle = self.zero_angle
    
    # update one servo to appropriate angle for data val
    async def moveServo(self, servoNum, positions, servoKit, data_val, shapeManager):
        newAngle = self.dataValueToAngle(data_val)
        print("moving servo ", servoNum, "to ", newAngle)
        servoKit.servo[servoNum].angle = newAngle
        shapeManager.updatePositionGrid(servoNum, newAngle)

    # converting data value to angle servo needs to be set to
    def dataValueToAngle(self, val):
        angle = (val - self.data_low) * (self.highest_angle - self.lowest_angle) / (
            self.data_high - self.data_low
        ) + self.lowest_angle
        return angle