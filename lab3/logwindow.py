import tkinter as tk

class LogWindow:
    def __init__(self):
        self.window = None
        self.container = None
        self.output = None

    def addLog(self, text):
        self.output.configure(state="normal")
        for i in range(len(text)):
            self.output.insert(tk.END, text[i])
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