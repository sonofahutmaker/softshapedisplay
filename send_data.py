import random
import time
from pythonosc.udp_client import SimpleUDPClient

NUM_ROWS = 50
NUM_COLS = 50
DATA_RANGE = [-10, 10]

client = SimpleUDPClient("10.0.1.119", 1337)

while True:
    x = random.randint(0, NUM_ROWS-1)
    y = random.randint(0, NUM_COLS-1)
    val = random.uniform(DATA_RANGE[0], DATA_RANGE[1])
    # print(x, y, val)
    client.send_message("/block", [x, y, val])
    time.sleep(1)