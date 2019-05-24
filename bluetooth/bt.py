import threading
import time
import sys
import serial
from score import *


class bluetooth:
    def __init__(self, port: str, baudrate: int=9600):
        """ Initialize an BT object, and auto-connect it. """
        # The port name is the name shown in control panel
        # And the baudrate is the communication setting, default value of HC-05 is 9600.
        self.ser = serial.Serial(port, baudrate=baudrate)
        
    def is_open(self) -> bool:
        return self.ser.is_open

    def waiting(self) -> bool:
        return self.ser.in_waiting

    def do_connect(self, port: str, baudrate: int=9600) -> bool:
        """ Connect to the specify port with particular baudrate """
        # Connection function. Disconnect the previous communication, specify a new one.
        self.disconnect()

        try:
            self.ser = serial.Serial(port, baudrate=baudrate)
            return True
        except:
            return False

    def disconnect(self):
        """ Close the connection. """
        self.ser.close()

    def write(self, output: str):
        # Write the byte to the output buffer, encoded by utf-8.
        send = output.encode("utf-8")
        self.ser.write(send)

    def readString(self) -> str:
        receiveMsg = None
        # Scan the input buffer until meet a '\n'. return none if doesn't exist.
        if(self.waiting()):
            receiveMsg = self.ser.readline().decode("utf-8")[:-1]
        return receiveMsg

def read():
    msg = None
    inf = open( "./cmd.txt", "r" )
    cmds = [ k.strip() for k in inf ]
    cmd_counter = 0
    halt = False
    scoreboard = Scoreboard( "./UID.csv" )
    while True:
        if bt.waiting():
            msg = bt.readString()
            print( msg )
            if not halt:
                if msg == "track":
                    bt.write( cmds[cmd_counter] + '\n' )
                elif msg == "reach":
                    cmd_counter += 1
                    if cmd_counter >= len(cmds):
                        cmd_counter = 0
                elif msg[:4] = "RFID":
                    rfid = msg[7:]
                    scoreboard.add_UID( rfid )
                    print( 'current score:', scoreboard.getCurrentScore() )

def write():
    while True:
        msgWrite = input()
        if msgWrite == "exit": sys.exit()
        bt.write(msgWrite + "\n")

if __name__ == "__main__":
    # Please modify the port name.
    bt = bluetooth("/dev/rfcomm0")
    while not bt.is_open(): pass
    print("BT Connected!")

    readThread = threading.Thread(target=read)
    readThread.setDaemon(True)
    readThread.start()

    while True:

        msgWrite = input()
        if msgWrite == "exit": sys.exit()
        bt.write(msgWrite + "\n")


