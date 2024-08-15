from ShapeDisplayManager import ShapeDisplayManager
from OSCManager import OSCManager
from LEDManager import LEDManager
import asyncio

IP = "192.168.50.93"
PORT = 1338
LED_NUM = 210

async def loop():
    while True:
        await asyncio.sleep(0)

async def main():
    displayManager = ShapeDisplayManager(16)
    # ledManager = LEDManager(LED_NUM)
    displayManager.zeroAllServos()
    oscManager = OSCManager(IP, PORT, displayManager)
    transport, protocol = await oscManager.init_osc()

    await loop()

    transport.close()

asyncio.run(main())