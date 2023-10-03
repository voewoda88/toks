class MyPacket:
    def __init__(self):
        self.flag = 0
        self.destinationAddress = 0
        self.sourceAddress = 0
        self.data = ''
        self.fcs = 0
        self.data = []

    def packageFormation(self, sourceAddress, data):
        self.flag = ord('z') + 1  # Флаг (1 байт)
        self.destinationAddress = 0  # Destination Address (1 байт)
        self.sourceAddress = sourceAddress  # Source Address (1 байт, номер ком-порта)
        self.data = data  # Data (1 байт, данные)
        self.dataBytes = self.data.encode('utf-8')
        self.fcs = 0  # FCS (1 байт, всегда нулевой)

    def conversationPackageToBytes(self):
        self.data = bytes([self.flag, self.destinationAddress, self.sourceAddress]) + self.dataBytes + bytes([self.fcs])

        return self.data

    def byteStuffing(self):
        stuffedData = []
        for byte in self.data:
            if byte == 0x7E:
                stuffedData.extend([0x7D, 0x5E])
            elif byte == 0x7D:
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
                    # Неверная последовательность символов байт-стаффинга, обработать по необходимости
                    i += 1
            else:
                destuffedData.append(data[i])
                i += 1
        return destuffedData
