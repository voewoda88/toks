import tkinter as tk
from comports import ComPort

class UserWindow:
    def outputInfoFromComPort(self):
        outputText = self.comPort.comPortReiciving()
        self.output.configure(state="normal")
        self.output.insert(tk.END, outputText)
        self.output.configure(state="disabled")


    def sendButtonEvent(self):
        text = self.entry.get()
        self.comPort.comPortTexting(text)
        self.outputInfoFromComPort()


    def __init__(self):
        self.comPort = ComPort()

        self.window = tk.Tk()
        self.window.title("Окно пользователя 1")
        self.window.geometry("400x300")
        self.window.resizable(False, False)

        self.container = tk.Frame(self.window)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry = tk.Entry(self.container)
        self.entry.pack(pady=(0, 5), anchor="w", fill="x")

        self.button = tk.Button(self.container, text="Отправить", command=self.sendButtonEvent)
        self.button.pack(pady=(0, 5), anchor="w")

        self.output = tk.Text(self.container)
        self.output.configure(state="disabled")
        self.output.pack()

        self.window.mainloop()
