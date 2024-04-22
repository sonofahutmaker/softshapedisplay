import asyncio
from adafruit_servokit import ServoKit 
import servo_utils

class ShapeDisplayManager:
    def __init__(self, num_servos):
        print("initializing shape display manager with num servos: " + num_servos)
        self.num_servos = num_servos
        self.kit = ServoKit(channels=self.num_servos)
        self.positions = [0] * self.num_servos

    async def zeroAllServos(self):
        await asyncio.gather(servo_utils.zeroServo(i, self.kit) for i in range(0,self.num_servos))
    
    def getLatestPositionsGrid(self):
        return self.positions
    
    def getServoKit(self):
        return self.kit
    
    def updatePositionGrid(self, servoNum, newPos):
        self.positions = servo_utils.saveServoPosition(servoNum, newPos, self.positions)