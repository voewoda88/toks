import tkinter as tk
import serial
from comports import ComPort
import globalVariables

class UserWindow:
    def comPortChoice(self):
        if self.number == 0:
            self.comPort.openComPortPair1(globalVariables.parity)
        else:
            self.comPort.openComPortPair2(globalVariables.parity)

    def outputInfoFromComPort(self):
        outputText = self.comPort.comPortReiciving(self.number)
        self.output.configure(state="normal")
        self.output.delete('1.0', 'end')
        self.output.insert(tk.END, outputText)
        self.output.configure(state="disabled")

    def sendButtonEvent(self):
        self.comPortChoice()
        text = self.entry.get()
        if text:
            self.sendBytes = self.comPort.comPortTexting(self.number, text)
            self.sendBytesLabel.config(text="Количество переданных байт: " + str(self.sendBytes))
            self.otherObject.outputInfoFromComPort()

    def clearButtonEvent(self):
        text = self.entry.get()
        if text:
            self.entry.delete(0, tk.END)

    def radioButtonEvent(self):
        match self.choice:
            case 1:
                globalVariables.parity = serial.PARITY_NONE
            case 2:
                globalVariables.parity = serial.PARITY_EVEN
            case 3:
                globalVariables.parity = serial.PARITY_ODD

    def validateAlphanumeric(self, text):
        if text.replace(" ", "").isalnum() and text.isascii():
            return True
        else:
            return False

    def setOtherObject(self, otherObject):
        self.otherObject = otherObject

    def createWindow(self):
        if self.number == 0:
            string = "COM" + str((self.comPort.firstPair * 2) - 2) + "->COM" + str((self.comPort.firstPair * 2) - 1)
        else:
            string = "COM" + str((self.comPort.secondPair * 2) - 2) + "->COM" + str((self.comPort.secondPair * 2) - 1)

        self.window = tk.Tk()
        self.window.title(string)
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Parity", menu=menu)

        self.choice = tk.IntVar(value=1)

        menu.add_radiobutton(label="None", variable=self.choice, value=1, command=self.radioButtonEvent)
        menu.add_radiobutton(label="Even", variable=self.choice, value=2, command=self.radioButtonEvent)
        menu.add_radiobutton(label="Odd", variable=self.choice, value=3, command=self.radioButtonEvent)

        self.container = tk.Frame(self.window)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry = tk.Entry(self.container)
        self.entry.pack(pady=(0, 5), anchor="w", fill="x")

        validate = (self.window.register(self.validateAlphanumeric), "%P")
        self.entry.config(validate="key", validatecommand=validate)

        self.button = tk.Button(self.container, text="Отправить", command=self.sendButtonEvent)
        self.button.pack(pady=(0, 5), anchor="w")

        self.clearButton = tk.Button(self.container, text="Очистить", command=self.clearButtonEvent)
        self.clearButton.pack(pady=(0, 5), anchor="w")

        self.sendBytesLabel = tk.Label(self.container, text="Количество переданных байт: 0")
        self.sendBytesLabel.pack(pady=(0, 5), padx=10, anchor="w")

        self.output = tk.Text(self.container)
        self.output.configure(state="disabled")
        self.output.pack()

        self.window.mainloop()

    def __init__(self, number, comPort: ComPort):
        self.comPort = comPort
        self.number = number
        self.otherObject = None
        globalVariables.parity = serial.PARITY_NONE
        self.sendBytes = 0

        self.window = None
        self.container = None
        self.entry = None
        self.button = None
        self.clearButton = None
        self.output = None
