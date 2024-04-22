import ShapeDisplayManager, OSCManager
import asyncio

IP = "127.0.0.1"
PORT = 1337

async def loop():
    while True:
        # print("would be setting actuators, interpretting input etc here")
        await asyncio.sleep(0)

async def main():
    displayManager = ShapeDisplayManager(16)
    await displayManager.zeroAllServos()
    oscManager = OSCManager(IP, PORT)
    transport, protocol = await oscManager.init_osc()

    await loop()

    transport.close()