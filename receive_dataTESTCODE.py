import asyncio
import sys
import time

import numpy as np
from adafruit_servokit import ServoKit
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

kit = ServoKit(channels=16)
np.set_printoptions(threshold=sys.maxsize)

ip = "127.0.0.1"
port = 1337


def grid_val_handler(address, *args):
    print(f"{address}: {args}")
    moveServo(0, args[2])
    DATA_GRID[args[0]][args[1]] = args[2]


dispatcher = Dispatcher()
dispatcher.map("/gridval", grid_val_handler)

NUM_ROWS = 50
NUM_COLS = 50
DATA_RANGE = [-10, 10]
DATA_GRID = np.zeros((NUM_ROWS, NUM_COLS))
HIGH_ANGLE = 180
LOW_ANGLE = 0


def moveServo(servoNum, dataval):
    angle = (dataval - DATA_RANGE[0]) * (HIGH_ANGLE - LOW_ANGLE) / (
        DATA_RANGE[1] - DATA_RANGE[0]
    ) + LOW_ANGLE
    # will either need to make bigger gear or make servo turn x num of times to get to pos
    kit.servo[servoNum].angle = angle


async def loop():
    while True:
        # print("would be setting actuators, interpretting input etc here")
        # print(DATA_GRID)
        await asyncio.sleep(0)


async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()
    kit.servo[0].angle = 90

    await loop()

    transport.close()


asyncio.run(init_main())
