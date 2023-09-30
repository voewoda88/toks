import serial
import random
import globalVariables
from mypacket import MyPacket

class ComPort:
    def comPortReiciving(self, number):
        data = ""
        if number == 0:
            while True:
                receivedData = self.serReciever2.read(5)
                if not receivedData:
                    break
                data += chr(receivedData[3])
        else:
            while True:
                receivedData = self.serReciever1.read(5)
                if not receivedData:
                    break
                data += chr(receivedData[3])

        return data


    def comPortTexting(self, number, text):
        if number == 0:
            for char in text:
                self.packet.packageFormation(self.firstPair - 1, char)
                stuffedPacket = self.packet.byteStuffing()
                self.serSender1.write(stuffedPacket)
        else:
            for char in text:
                self.packet.packageFormation(self.secondPair - 1, char)
                stuffedPacket = self.packet.byteStuffing()
                self.serSender2.write(stuffedPacket)


    def openComPortPair1(self, parity):
        match self.firstPair:
            case 1:
                self.serSender1 = serial.Serial(globalVariables.serialPortSender1, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever1 = serial.Serial(globalVariables.serialPortReciever1, baudrate=9600, timeout=1,
                                                  parity=parity)
            case 2:
                self.serSender1 = serial.Serial(globalVariables.serialPortSender2, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever1 = serial.Serial(globalVariables.serialPortReciever2, baudrate=9600, timeout=1,
                                                  parity=parity)
            case 3:
                self.serSender1 = serial.Serial(globalVariables.serialPortSender3, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever1 = serial.Serial(globalVariables.serialPortReciever3, baudrate=9600, timeout=1,
                                                  parity=parity)
            case 4:
                self.serSender1 = serial.Serial(globalVariables.serialPortSender4, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever1 = serial.Serial(globalVariables.serialPortReciever4, baudrate=9600, timeout=1,
                                                  parity=parity)

    def openComPortPair2(self, parity):
        match self.secondPair:
            case 1:
                self.serSender2 = serial.Serial(globalVariables.serialPortSender1, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever2 = serial.Serial(globalVariables.serialPortReciever1, baudrate=9600, timeout=1,
                                                  parity=parity)
            case 2:
                self.serSender2 = serial.Serial(globalVariables.serialPortSender2, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever2 = serial.Serial(globalVariables.serialPortReciever2, baudrate=9600, timeout=1,
                                                  parity=parity)
            case 3:
                self.serSender2 = serial.Serial(globalVariables.serialPortSender3, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever2 = serial.Serial(globalVariables.serialPortReciever3, baudrate=9600, timeout=1,
                                                  parity=parity)
            case 4:
                self.serSender2 = serial.Serial(globalVariables.serialPortSender4, baudrate=9600, timeout=1,
                                                parity=parity)
                self.serReciever2 = serial.Serial(globalVariables.serialPortReciever4, baudrate=9600, timeout=1,
                                                  parity=parity)

    def __init__(self):
        self.firstPair = None
        self.secondPair = None
        self.packet = MyPacket()

        self.firstPair = random.randint(1, 4)

        while True:
            self.secondPair = random.randint(1,4)
            if self.secondPair != self.firstPair:
                break

    def __del__(self):
        self.serSender1.close()
        self.serReciever1.close()

        self.serSender2.close()
        self.serReciever2.close()