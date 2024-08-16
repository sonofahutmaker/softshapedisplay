from ShapeDisplayManager import ShapeDisplayManager
from OSCManager import OSCManager
import asyncio
import argparse
from os.path import exists
from utils import *

def check_ini():
    return exists("config.ini")

def parse_my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", required=not check_ini())
    parser.add_argument("-p", "--port", required=not check_ini())
    parser.add_argument("-d", "--data_range", nargs='+')
    parser.add_argument("-a", "--angle_range", nargs='+')
    parser.add_argument("-s", "--servo_type", choices=["standard", "cont"])

    # CONSTANTS FOR CONT ROTATION SERVOS
    # length of pusher shaft in mm, not including length of servo holder (6 inches)
    parser.add_argument("--shaft_len") 
    # time for gear to turn and shaft to move from bottom to top pos in secs at full speed
    parser.add_argument("-t", "--traversal_time")
    parser.add_argument("-f", "--forward_throttle") # full positive throttle value
    parser.add_argument("-b", "--backward_throttle") # full negative throttle value
    parser.add_argument("-z", "--zero_throttle")
    parser.add_argument("--speed")

    args = parser.parse_args()
    return args

async def loop():
    while True:
        await asyncio.sleep(0)

async def main():
    args = parse_my_args()
    generate_ini(args)
    servo_type = retrieve_config('servo_type')
    displayManager = ShapeDisplayManager(16, servo_type)
    displayManager.zeroAllServos()
    oscManager = OSCManager(displayManager)
    transport, protocol = await oscManager.init_osc()

    await loop()

    transport.close()

asyncio.run(main())