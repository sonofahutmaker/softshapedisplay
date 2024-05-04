from adafruit_servokit import ServoKit
import time
from servo_utils import *
import asyncio

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
# for i in range(0, 16):
#     moveServo(i, LOWEST_ANGLE, kit)

moveServo(0, LOWEST_ANGLE, kit)
time.sleep(1)

for i in range(LOWEST_ANGLE, HIGHEST_ANGLE, -1):
    print("going to ", i)
    moveServo(0, i, kit)
    time.sleep(0.01)
