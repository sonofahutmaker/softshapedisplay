from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

# kit.servo[0].angle =180
while True:
    kit.servo[0].angle=180
    time.sleep(1)
    kit.servo[0].angle =0