import random
import globalVariables
import time

class PacketController:
    def crc8(self, data):
        crc = 0xFF
        polynomial = 0x31

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc <<= 1

        return crc & 0xFF

    def randomBitChange(self, byte):
        if random.randint(0, 0) == 0:
            bitIndex = random.randint(0, 7)
            bitMask = 1 << bitIndex
            modifiedByte = byte ^ bitMask
            globalVariables.collisionDetected = True
        else:
            globalVariables.collisionDetected = False
            modifiedByte = byte

        return modifiedByte

    def dataErrorCorrection(self, data, oldFcs):
        newFcs = self.crc8([data])
        if newFcs == oldFcs:
            return chr(data)
        else:
            for i in range(0, 255):
                if oldFcs == self.crc8([i]):
                    return chr(i)

    def byteStuffing(self, data):
        stuffedData = []
        for byte in data:
            if byte == 0x7E:
                globalVariables.byteStaffingFlag = True
                stuffedData.extend([0x7D, 0x5E])
            elif byte == 0x7D:
                globalVariables.byteStaffingFlag = True
                stuffedData.extend([0x7D, 0x5D])
            else:
                stuffedData.append(byte)
        return bytes(stuffedData)

    @staticmethod
    def byteDestuffing(data):
        destuffedData = []
        i = 0
        while i < len(data):
            if data[i] == 0x7D:
                if data[i + 1] == 0x5E:
                    destuffedData.append(0x7E)
                    i += 2
                elif data[i + 1] == 0x5D:
                    destuffedData.append(0x7D)
                    i += 2
                else:
                    i += 1
            else:
                destuffedData.append(data[i])
                i += 1
        return destuffedData