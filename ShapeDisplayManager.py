from adafruit_servokit import ServoKit 
from utils import *
from StandardServo import StandardServo
from ContinuousServo import ContinuousServo
import asyncio

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
    
    async def zeroAllServos(self):
        async with asyncio.TaskGroup() as tg:
            for i in range(self.num_servos):
                tg.create_task(self.servos.zeroServo(i, self.kit))

    def getLatestPositionsGrid(self):
        return self.positions
    
    def getServoKit(self):
        return self.kit
    
    def updatePositionGrid(self, servoNum, newPos):
        self.positions = self.servos.saveServoPosition(servoNum, newPos, self.positions)