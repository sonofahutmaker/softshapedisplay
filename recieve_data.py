from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

ip = "127.0.0.1"
port = 1337

def grid_val_handler(address, *args):
    print(f"{address}: {args}")
    DATA_GRID[args[0]][args[1]] = args[2]

dispatcher = Dispatcher()
dispatcher.map("/gridval", grid_val_handler)

NUM_ROWS = 50
NUM_COLS = 50
DATA_RANGE = [-10, 10]
DATA_GRID = np.zeros((NUM_ROWS, NUM_COLS))

async def loop():
    while True:
        # print("would be setting actuators, interpretting input etc here")
        # print(DATA_GRID)
        await asyncio.sleep(0)

async def init_main():
    server = AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()

    await loop()

    transport.close()

asyncio.run(init_main())
