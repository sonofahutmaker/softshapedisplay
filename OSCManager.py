from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio
from utils import *
from servo_utils import *
import ShapeDisplayManager

class OSCManager:
    def __init__(self, ip, port, manager):
        self.ip = ip
        self.port = port
        self.manager = manager

    async def init_osc(self):
        print("init osc with ip", self.ip, "and port ", self.port)
        dispatcher = Dispatcher()
        dispatcher.map("/block", self.message_handler)
        server = AsyncIOOSCUDPServer((self.ip, self.port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        return transport, protocol
    
    # messages will be like "/block servoNum dataVal"
    def message_handler(self, address, *args):
        print(f"{address}: {args}")
        servoNum = args[0]
        dataVal = args[1]
        newAng = dataValueToAngle(dataVal)
        positions = self.manager.getLatestPositionsGrid()
        kit = self.manager.getServoKit()

        moveServo(servoNum, newAng, kit)
        positions = self.manager.getLatestPositionsGrid()
        saveServoPosition(servoNum, newAng, positions)