import tkinter as tk

class LogWindow:
    def __init__(self):
        self.window = None
        self.container = None
        self.output = None

    def addLog(self, text, byteData):
        binaryData = ' '.join(bin(byte)[2:].zfill(8) for byte in byteData)
        self.output.configure(state="normal")
        self.output.insert(tk.END, text + binaryData + '\n')
        self.output.configure(state="disabled")

    def createLogWindow(self):
        self.window = tk.Tk()
        self.window.title("Log Window")
        self.window.geometry("650x440")

        self.container = tk.Frame(self.window)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.output = tk.Text(self.container)
        self.output.configure(state="disabled")
        self.output.pack()

        self.window.mainloop()
