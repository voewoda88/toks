import struct


class Packet:
    def __init__(self, flag, destinationAddress, sourceAddress, data, fcs):
        self.flag = flag
        self.destinationAddress = destinationAddress
        self.sourceAddress = sourceAddress
        self.data = data
        self.fcs = fcs

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, value):
        self._flag = value

    @property
    def destinationAddress(self):
        return self._destinationAddress

    @destinationAddress.setter
    def destinationAddress(self, value):
        self._destinationAddress = value

    @property
    def sourceAddress(self):
        return self._sourceAddress

    @sourceAddress.setter
    def sourceAddress(self, value):
        self._sourceAddress = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def fcs(self):
        return self._fcs

    @fcs.setter
    def fcs(self, value):
        self._fcs = value

    def getPacket(self):
        data = struct.pack('!BBBBB', self.flag, self.destinationAddress, self.sourceAddress, self.data, self.fcs)
        return data
