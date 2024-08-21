from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio
from utils import *

class OSCManager:
    def __init__(self, manager):
        self.ip = retrieve_config("ip")
        self.port = retrieve_config("port")
        self.manager = manager

    # will wait for osc messages and then map to handler functions
    async def init_osc(self):
        print("init osc with ip", self.ip, "and port ", self.port)
        dispatcher = Dispatcher()
        # new handler functions with unique addresses can follow the below 
        dispatcher.map("/block", self.block_message_handler)
        dispatcher.map("/list", self.list_message_handler)
        server = AsyncIOOSCUDPServer((self.ip, self.port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        return transport, protocol
    
    # messages will be like "/list 0 1 .5 1 .7 ..." with 
    # a list of data values for the whole number of servos
    def list_message_handler(self, address, *args):
        print(f"{address}: {args}")
        evloop = asyncio.get_event_loop()
        kit = self.manager.getServoKit()
        for i in range(len(args)):
            servoNum = i
            dataVal = args[i]
            positions = self.manager.getLatestPositionsGrid()
            evloop.create_task(self.manager.servos.moveServo(servoNum, positions, kit, dataVal, self.manager))
    
    # messages will be like "/block servoNum dataVal"
    def block_message_handler(self, address, *args):
        print(f"{address}: {args}")
        servoNum = args[0]
        dataVal = args[1]
        evloop = asyncio.get_event_loop()
        positions = self.manager.getLatestPositionsGrid()
        kit = self.manager.getServoKit()
        evloop.create_task(self.manager.servos.moveServo(servoNum, positions, kit, dataVal, self.manager))