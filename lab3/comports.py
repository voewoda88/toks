import serial
import random
import globalVariables
from packet import Packet
from packetController import PacketController

class ComPort:
    def comPortReiciving(self, number):
        data = ""
        position = 2
        if number == 0:
            while True:
                if globalVariables.byteStaffingFlag == True:
                    receivedData = self.serReciever2.read(6)
                    globalVariables.byteStaffingFlag = False
                else:
                    receivedData = self.serReciever2.read(5)
                if not receivedData:
                    break
                destuffingPacket = self.packetController.byteDestuffing(receivedData)
                receivedPacket = Packet(destuffingPacket[0], destuffingPacket[1], destuffingPacket[2],
                                        destuffingPacket[3], destuffingPacket[4])
                byteData = receivedPacket.getPacket()
                binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in byteData)
                self.log.insert(position, "Принятый пакет: " + binaryData + "\n\n")
                position += 2
                data += self.packetController.dataErrorCorrection(receivedPacket.data, receivedPacket.fcs)

        else:
            while True:
                if globalVariables.byteStaffingFlag == True:
                    receivedData = self.serReciever1.read(6)
                    globalVariables.byteStaffingFlag = False
                else:
                    receivedData = self.serReciever1.read(5)
                if not receivedData:
                    break
                destuffingPacket = self.packetController.byteDestuffing(receivedData)
                receivedPacket = Packet(destuffingPacket[0], destuffingPacket[1], destuffingPacket[2],
                                        destuffingPacket[3], destuffingPacket[4])
                byteData = receivedPacket.getPacket()
                binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in byteData)
                self.log.insert(position, "Принятый пакет: " + binaryData + "\n\n")
                position += 2
                data += self.packetController.dataErrorCorrection(receivedPacket.data, receivedPacket.fcs)

        self.logWindow.addLog(self.log)
        self.log.clear()
        return data

    def comPortTexting(self, number, text):
        sendBytes = 0
        self.counter += 1
        self.log.append("Группа пакетов " + str(self.counter) + "\n\n")
        if number == 0:
            for char in text:
                packet = Packet(ord('z') + 1, 0, (self.firstPair * 2) - 2, ord(char),
                                self.packetController.crc8([ord(char)]))
                byteData = packet.getPacket()
                binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in byteData)
                self.log.append("Отправленный пакет: " + binaryData + "\n")
                packet._data = self.packetController.randomBitChange(packet.data)
                stuffedPacket = self.packetController.byteStuffing(packet.getPacket())
                sendBytes += self.serSender1.write(stuffedPacket)
        else:
            for char in text:
                packet = Packet(ord('z') + 1, 0, (self.secondPair * 2) - 2, ord(char),
                                self.packetController.crc8([ord(char)]))
                byteData = packet.getPacket()
                binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in byteData)
                self.log.append("Отправленный пакет: " + binaryData + "\n")
                packet._data = self.packetController.randomBitChange(packet.data)
                stuffedPacket = self.packetController.byteStuffing(packet.getPacket())
                sendBytes += self.serSender2.write(stuffedPacket)

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

    def __init__(self, logWindow):
        self.firstPair = None
        self.secondPair = None
        self.counter = 0
        self.packetController = PacketController()
        self.log = []
        self.logWindow = logWindow

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