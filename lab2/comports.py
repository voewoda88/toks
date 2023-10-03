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
        self.counter += 1
        self.logWindow.addLog("Группа пакетов: " + str(self.counter), "")
        self.logWindow.addLog("", "")
        if number == 0:
            for char in text:
                self.packet.packageFormation((self.firstPair * 2) - 2, char)
                conversationPacket = self.packet.conversationPackageToBytes()
                self.logWindow.addLog("Пакет до байт стаффинга: ", conversationPacket)
                stuffedPacket = self.packet.byteStuffing()
                self.logWindow.addLog("Пакет после байт стаффинга: ", stuffedPacket)
                self.logWindow.addLog("", "")
                self.serSender1.write(stuffedPacket)
        else:
            for char in text:
                self.packet.packageFormation((self.secondPair * 2) - 2, char)
                conversationPacket = self.packet.conversationPackageToBytes()
                self.logWindow.addLog("Пакет до байт стаффинга: ", conversationPacket)
                stuffedPacket = self.packet.byteStuffing()
                self.logWindow.addLog("Пакет после байт стаффинга: ", stuffedPacket)
                self.logWindow.addLog("", "")
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

    def __init__(self, logWindow):
        self.firstPair = None
        self.secondPair = None
        self.counter = 0
        self.logWindow = logWindow
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