from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer
import asyncio
from utils import *
from servo_utils import *
import ShapeDisplayManager
import LEDManager

class OSCManager:
    def __init__(self, ip, port, manager, ledManager):
        self.ip = ip
        self.port = port
        self.manager = manager
        self.ledManager = ledManager

    async def init_osc(self):
        print("init osc with ip", self.ip, "and port ", self.port)
        dispatcher = Dispatcher()
        dispatcher.map("/block", self.list_message_handler)
        server = AsyncIOOSCUDPServer((self.ip, self.port), dispatcher, asyncio.get_event_loop())
        transport, protocol = await server.create_serve_endpoint()
        return transport, protocol
    
    def list_message_handler(self, address, *args):
        print(f"{address}: {args}")
        for i in range(len(args)):
            servoNum = i
            dataVal = args[i]
            newAng = dataValueToAngle(dataVal)
            positions = self.manager.getLatestPositionsGrid()
            kit = self.manager.getServoKit()

            moveServo(servoNum, newAng, kit)
            positions = self.manager.getLatestPositionsGrid()
            saveServoPosition(servoNum, newAng, positions)

    def led_message_handler(self, address, *args): 
        #messages will have row and col number
        #like row col brightness
        brightness = args[2]
        row = args[0]
        col = args[1]
        self.ledManager(row, col, brightness)

    def servos_led_message_handler(self, address, *args):
        for i in range(0,16): 
            servoNum = i
            dataVal = args[i]
            newAng = dataValueToAngle(dataVal)
            positions = self.manager.getLatestPositionsGrid()
            kit = self.manager.getServoKit()

            moveServo(servoNum, newAng, kit)
            positions = self.manager.getLatestPositionsGrid()
            saveServoPosition(servoNum, newAng, positions)
        for i in range(16, len(args)):
            brightness = args[i]
            self.ledManager.setLight(i-15, brightness)
    
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