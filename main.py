from ShapeDisplayManager import ShapeDisplayManager
from OSCManager import OSCManager
import asyncio
import argparse
from os.path import exists
from utils import *

IP = "192.168.50.93"
PORT = 1338

def check_ini():
    return exists("config.ini")

def parse_my_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", required=not check_ini())
    parser.add_argument("-p", "--port", required=not check_ini())
    parser.add_argument("-d", "--data_range", nargs='+')
    parser.add_argument("-a", "--angle_range", nargs='+')

    args = parser.parse_args()
    return args

async def loop():
    while True:
        await asyncio.sleep(0)

async def main():
    args = parse_my_args()
    generate_ini(args)
    displayManager = ShapeDisplayManager(16)
    displayManager.zeroAllServos()
    oscManager = OSCManager(IP, PORT, displayManager)
    transport, protocol = await oscManager.init_osc()

    await loop()

    transport.close()

asyncio.run(main())