import random
import time
from pythonosc.udp_client import SimpleUDPClient

NUM_ROWS = 50
NUM_COLS = 50
DATA_RANGE = [-1, 1]

client = SimpleUDPClient("127.0.0.1", 1338)

# client.send_message("/block", [0, .5])

while True:
    x = random.randint(0, 15)
    # y = random.randint(0, NUM_COLS-1)
    val = random.uniform(DATA_RANGE[0], DATA_RANGE[1])
    # # print(x, y, val)
    # client.send_message("/gridval", [x, y, val])
    client.send_message("/block", [x, val])
    time.sleep(1)