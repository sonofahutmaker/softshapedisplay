import asyncio
from utils import *

def zeroServo(servoNum, servoKit):
    print("zeroing servonum ", servoNum)
    servoKit.servo[servoNum].angle = ZERO_ANGLE

async def zeroContServo(servoNum, servoKit):
    print("zeroing servonum ", servoNum)
    print("setting servo " , servoNum, "to throttle ", FORWARD_THROTTLE * SPEED)
    servoKit.continuous_servo[servoNum].throttle = FORWARD_THROTTLE * SPEED
    await asyncio.sleep(WHOLE_SHAFT_TRAVERSAL_TIME * SPEED)
    servoKit.continuous_servo[servoNum].throttle = BACKWARD_THROTTLE * SPEED
    print("setting servo ", servoNum, "to throttle ", BACKWARD_THROTTLE * SPEED)
    await asyncio.sleep((WHOLE_SHAFT_TRAVERSAL_TIME * SPEED)/2)
    print("stopping servo ", servoNum)
    servoKit.continuous_servo[servoNum].throttle = ZERO_THROTTLE

# save current servo pos in data structure
def saveServoPosition(servoNum, pos, positions):
    positions[servoNum] = pos
    return positions

async def moveContServo(servoNum, newPos, positions, servoKit):
    oldPos = positions[servoNum]
    dist = getDistanceToTravel(oldPos, newPos)
    timeTaken = getTimeToPosition(dist)
    throttle = getThrottle(dist)
    servoKit.continuous_servo[servoNum].throttle = throttle
    print("moveServo setting servo ", servoNum," throttle to ", throttle)
    await asyncio.sleep(timeTaken)
    print("after ", timeTaken, "seconds, stopping servo ", servoNum)
    servoKit.continuous_servo[servoNum].throttle = ZERO_THROTTLE

def moveServo(servoNum, newAngle, servoKit):
    print("moving servo ", servoNum, "to ", newAngle)
    servoKit.servo[servoNum].angle = newAngle