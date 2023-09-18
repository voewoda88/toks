import serial

class ComPort:
    def comPortReiciving(self):
        receivedData = self.serReciever.readline()
        receivedData.decode('utf-8')
        print(receivedData)
        return receivedData

    def comPortTexting(self, text):
        self.serSender.write(text.encode())

    def __init__(self):
        self.serialPortSender = '/dev/tnt0'
        self.serialPortReciever = '/dev/tnt1'

        self.serSender = serial.Serial(self.serialPortSender, baudrate=9600, timeout=1)
        self.serReciever = serial.Serial(self.serialPortReciever, baudrate=9600, timeout=1)

    def __del__(self):
        self.serSender.close()
        self.serReciever.close()