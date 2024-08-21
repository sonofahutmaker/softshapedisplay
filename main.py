from ShapeDisplayManager import ShapeDisplayManager
from OSCManager import OSCManager
import asyncio
import argparse
from os.path import exists
from utils import *

def check_ini():
    return exists("config.ini")

# command line arguments for running app
def parse_my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", required=not check_ini(),
                        help="ip address of device this is running on to receive data")
    parser.add_argument("-p", "--port", required=not check_ini(),
                        help="port number to receive OSC messages on")
    parser.add_argument("-n", "--num_servos", required=not check_ini())
    parser.add_argument("-d", "--data_range", nargs='+', 
                        help="possible range of data values low to high like '0.0 1.0'")
    parser.add_argument("-a", "--angle_range", nargs='+',
                        help = "for standard servo, angle range low to high like '180 0' \
                            with order dependent on orientation")
    parser.add_argument("-s", "--servo_type", choices=["standard", "cont"])

    # CONSTANTS FOR CONT ROTATION SERVOS
    # length of pusher shaft in mm, not including length of servo holder
    parser.add_argument("--shaft_len", help="for cont. rot servos, length of pusher shaft in mm") 
    parser.add_argument("-t", "--traversal_time",  
                        help="for cont. rot servos, time in secs to move \
                        shaft all the way up at full throttle")
    parser.add_argument("-f", "--forward_throttle",  
                        help="for cont. rot servos, direction and \
                            full power value for moving shafts up") # full positive throttle value
    parser.add_argument("-b", "--backward_throttle",
                        help="for cont. rot servos, direction and \
                            full power value for moving shafts down") # full negative throttle value
    parser.add_argument("-z", "--zero_throttle", 
                        help="for cont. rot. servos, throttle \
                            value that stops servo spinning")
    parser.add_argument("--speed", help="for cont. rot. servos, multiplier for throttle")

    args = parser.parse_args()
    return args

async def loop():
    while True:
        await asyncio.sleep(0)

async def main():
    args = parse_my_args()
    generate_ini(args)
    servo_type = retrieve_config('servo_type')
    displayManager = ShapeDisplayManager(int(retrieve_config('num_servos')), servo_type)
    await displayManager.zeroAllServos()
    oscManager = OSCManager(displayManager)
    transport, protocol = await oscManager.init_osc()

    await loop()

    transport.close()

asyncio.run(main())
