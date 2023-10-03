import threading

from userwindow import UserWindow
from comports import ComPort
from logwindow import LogWindow

class Main:
    def __init__(self):
        self.logWindow = LogWindow()
        self.comPorts = ComPort(self.logWindow)
        self.userWindow1 = None
        self.userWindow2 = None

    def run(self):
        self.userWindow1 = UserWindow(0, self.comPorts)
        self.userWindow2 = UserWindow(1, self.comPorts)

        self.userWindow1.setOtherObject(self.userWindow2)
        self.userWindow2.setOtherObject(self.userWindow1)

        thread1 = threading.Thread(target=self.userWindow1.createWindow)
        thread2 = threading.Thread(target=self.userWindow2.createWindow)
        thread3 = threading.Thread(target=self.logWindow.createLogWindow)

        thread1.start()
        thread2.start()
        thread3.start()

if __name__ == '__main__':
    main = Main()
    main.run()
