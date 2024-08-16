from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio
from utils import *
from servo_utils import *

class OSCManager:
    def __init__(self, ip, port, manager):
        self.ip = ip
        self.port = port
        self.manager = manager

    async def init_osc(self):
        print("init osc with ip", self.ip, "and port ", self.port)
        dispatcher = Dispatcher()
        dispatcher.map("/block", self.block_message_handler)
        dispatcher.map("/list", self.list_message_handler)
        server = AsyncIOOSCUDPServer((self.ip, self.port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        return transport, protocol
    
    # messages will be like "/list 0 1 .5 1 .7 ..." with 
    # a list of data values for the whole number of servos
    def list_message_handler(self, address, *args):
        print(f"{address}: {args}")
        for i in range(len(args)):
            servoNum = i
            dataVal = args[i]
            newAng = dataValueToAngle(dataVal)
            # positions = self.manager.getLatestPositionsGrid()
            kit = self.manager.getServoKit()

            moveServo(servoNum, newAng, kit)
            positions = self.manager.getLatestPositionsGrid()
            saveServoPosition(servoNum, newAng, positions)
    
    # messages will be like "/block servoNum dataVal"
    def block_message_handler(self, address, *args):
        print(f"{address}: {args}")
        servoNum = args[0]
        dataVal = args[1]
        newAng = dataValueToAngle(dataVal)
        # positions = self.manager.getLatestPositionsGrid()
        kit = self.manager.getServoKit()

        moveServo(servoNum, newAng, kit)
        positions = self.manager.getLatestPositionsGrid()
        saveServoPosition(servoNum, newAng, positions)