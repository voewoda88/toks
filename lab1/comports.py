import serial
import random

import globalVariables

class ComPort:
    def comPortReiciving(self, number):
        receivedData = ""
        if number == 0:
            while True:
                data = self.serReciever2.read()
                if data:
                    receivedData += data.decode('utf-8')
                else:
                    break
        else:
            while True:
                data = self.serReciever1.read()
                if data:
                    receivedData += data.decode('utf-8')
                else:
                    break

        return receivedData

    def comPortTexting(self, number, text):
        sendBytes = 0
        if number == 0:
            for char in text:
                sendBytes += self.serSender1.write(char.encode())
        else:
            for char in text:
                sendBytes += self.serSender2.write(char.encode())

        return sendBytes

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