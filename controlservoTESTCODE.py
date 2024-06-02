from adafruit_servokit import ServoKit
import time
from servo_utils import *
import asyncio
import random

kit = ServoKit(channels=16)
# kit.servo[0].angle = 0
async def main():
    while True:
        print("going")
        kit.servo[0].angle=180
        time.sleep(1)
        kit.servo[0].angle =0
        time.sleep(1)

# asyncio.run(main())
for i in range(0, 16):
    moveServo(i, LOWEST_ANGLE, kit)

# moveServo(12, HIGHEST_ANGLE, kit)
# time.sleep(3)
# while True:
#     moveServo(12, LOWEST_ANGLE, kit)
#     moveServo(8, LOWEST_ANGLE, kit)
#     time.sleep(2)
#     moveServo(12, HIGHEST_ANGLE, kit)
#     moveServo(8, HIGHEST_ANGLE, kit)
#     time.sleep(2)

# while True:
#     for i in range(0, 16):
#         moveServo(i, LOWEST_ANGLE, kit)
#     time.sleep(2)
#     for i in range(0, 16):
#             moveServo(i, HIGHEST_ANGLE, kit)
#     time.sleep(2)

# for i in range(LOWEST_ANGLE, HIGHEST_ANGLE, -1):
#     print("going to ", i)
#     moveServo(0, i, kit)
#     time.sleep(0.01)


# for i in range(0, 16):
#     dataval = random.random()
#     newAng = dataValueToAngle(dataval)
#     moveServo(i, newAng, kit)