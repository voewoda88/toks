import serial
import random
import globalVariables
import time
from packet import Packet
from packetController import PacketController

class ComPort:
    def portEmploymentEmulation(self, number):
        if random.randint(0, 1) == 0:
            if number == 0:
                self.serSender1.close()
            else:
                self.serSender2.close()

    def convertBytesToBites(self, packet):
        byteData = packet.getPacket()
        binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in byteData)

        return binaryData

    def dataGeneration(self, text):
        buffer = []
        numberOfTries = 0
        packet = None
        for char in text:
            for i in range(4):
                packet = Packet(ord('z') + 1, 0, (self.firstPair * 2) - 2, ord(char),
                                self.packetController.crc8([ord(char)]))
                self.logWindow.addLog("Сформированный пакет: " + self.convertBytesToBites(packet) + "\n")

                time.sleep(random.uniform(0, 0.1))
                packet._data = self.packetController.randomBitChange(packet.data)

                if globalVariables.collisionDetected == True:
                    time.sleep(random.uniform(0, 0.1))
                    numberOfTries += 1
                    self.logWindow.addLog("Произошла коллизия\n")
                    self.logWindow.addLog("Попытка номер " + str(numberOfTries) + "\n")
                    self.logWindow.addLog("Пакет с коллизией: " + self.convertBytesToBites(packet) + "\n")
                    time.sleep(random.uniform(0, pow(2, numberOfTries)))
                else:
                    break
            if numberOfTries == 4:
                self.logWindow.addLog("Количество попыток на исправление коллизии исчерпано\nПакет был передан с коллизией\n")
                numberOfTries = 0

            stuffedPacket = self.packetController.byteStuffing(packet.getPacket())
            buffer.append(stuffedPacket)

        return buffer

    def addDataToLogs(self, buffer):
        for data in buffer:
            binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in data)
            self.logWindow.addLog("Отправленный пакет: " + binaryData + "\n")


    def comPortReiciving(self, number):
        data = ""
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
                if globalVariables.collisionDetected == True:
                    self.logWindow.addLog("Полученный пакет содержит коллизию\n" + "Содержимое пакета: " + binaryData + "\n")
                    self.logWindow.addLog("Пакет направлен на исправление\n")
                receivedPacket._data = self.packetController.dataErrorCorrection(receivedPacket.data, receivedPacket.fcs)
                data += receivedPacket.data
                self.logWindow.addLog("Полученный пакет: " + binaryData + "\n")

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
                if globalVariables.collisionDetected == True:
                    self.logWindow.addLog(
                        "Полученный пакет содержит коллизию\n" + "Содержимое пакета: " + binaryData + "\n")
                    self.logWindow.addLog("Пакет направлен на исправление\n")
                receivedPacket._data = self.packetController.dataErrorCorrection(receivedPacket.data, receivedPacket.fcs)
                data += receivedPacket.data
                self.logWindow.addLog("Полученный пакет: " + binaryData + "\n")

        return data

    def comPortTexting(self, number, text):
        sendBytes = 0
        self.counter += 1
        self.logWindow.addLog("\nГруппа пакетов: " + str(self.counter) + "\n\n")
        if number == 0:
            buffer = self.dataGeneration(text)
            combinedBytes = b''.join(buffer)
            self.portEmploymentEmulation(number)
            while True:
                try:
                    sendBytes += self.serSender1.write(combinedBytes)
                    break
                except serial.SerialException as e:
                    self.logWindow.addLog("COM" + str((self.firstPair * 2) - 2) + " занят\n")
                    self.logWindow.addLog("Попытка отправить данные не удалась\n")
                    self.openComPortPair1(globalVariables.parity)
            self.addDataToLogs(buffer)

        else:
            buffer = self.dataGeneration(text)
            combinedBytes = b''.join(buffer)
            self.portEmploymentEmulation(number)
            while True:
                try:
                    sendBytes += self.serSender2.write(combinedBytes)
                    break
                except serial.SerialException as e:
                    self.logWindow.addLog("COM" + str((self.secondPair * 2) - 2) + " занят\n")
                    self.logWindow.addLog("Попытка отправить данные не удалась\n")
                    self.openComPortPair2(globalVariables.parity)
            self.addDataToLogs(buffer)

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