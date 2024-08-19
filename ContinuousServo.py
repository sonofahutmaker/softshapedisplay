from Servo import Servo
from utils import *
import asyncio

class ContinuousServo(Servo):
    def __init__(self):
        super().__init__()
        self.shaft_len = float(retrieve_config('shaft_len'))
        self.traversal_time = float(retrieve_config('traversal_time'))
        self.forward_throttle = float(retrieve_config('forward_throttle'))
        self.zero_throttle  = float(retrieve_config('zero_throttle'))
        self.backward_throttle = float(retrieve_config('backward_throttle'))
        self.speed = float(retrieve_config('speed'))
        self.zero_val = self.dataValueToShaftHeight(0)
    
    # CONT. ROTATION SERVO FUNCTIONS BELOW
    # convert data value to shaft top position in mm
    # middle of data range == 0mm up/down=
    def dataValueToShaftHeight(self, val):
        SHAFT_BOTTOM_POS = -self.shaft_len/2
        SHAFT_TOP_POS = self.shaft_len/2
        newPos = (val - self.data_low) * (SHAFT_TOP_POS - SHAFT_BOTTOM_POS) / (
            self.data_high - self.data_low
        ) + SHAFT_BOTTOM_POS
        return newPos
    
    def getDistanceToTravel(self, currPosition, nextPosition):
        return nextPosition - currPosition
    
    def getTimeToPosition(self, distance):
        # may have to be adjusted to account for variable force on shaft as silicone stretches
        travelTime = self.traversal_time * (abs(distance)/self.shaft_len) * self.speed
        return travelTime
    
    def getThrottle(self, distance):
        if distance < 0: # traveling down
            return self.backward_throttle * self.speed
        elif distance > 0: #travling up
            return self.forward_throttle * self.speed
        # if somehow distance is actually the same as before
        return self.zero_throttle
    
    async def zeroServo(self, servoNum, servoKit):
        print("zeroing servonum ", servoNum)
        print("setting servo " , servoNum, "to throttle ", self.forward_throttle * self.speed)
        servoKit.continuous_servo[servoNum].throttle = self.forward_throttle * self.speed
        await asyncio.sleep(self.traversal_time * self.speed)
        servoKit.continuous_servo[servoNum].throttle = self.backward_throttle * self.speed
        print("setting servo ", servoNum, "to throttle ", self.backward_throttle * self.speed)
        await asyncio.sleep((self.traversal_time * self.speed)/2)
        print("stopping servo ", servoNum)
        servoKit.continuous_servo[servoNum].throttle = self.zero_throttle

    async def moveServo(self, servoNum, positions, servoKit, data_val, shapeManager):
        oldPos = positions[servoNum]
        newPos = self.dataValueToShaftHeight(data_val)
        dist = self.getDistanceToTravel(oldPos, newPos)
        timeTaken = self.getTimeToPosition(dist)
        throttle = self.getThrottle(dist)
        servoKit.continuous_servo[servoNum].throttle = throttle
        print("moveServo setting servo ", servoNum," throttle to ", throttle)
        await asyncio.sleep(timeTaken)
        print("after ", timeTaken, "seconds, stopping servo ", servoNum)
        servoKit.continuous_servo[servoNum].throttle = self.zero_throttle
        shapeManager.updatePositionGrid(servoNum, newPos)