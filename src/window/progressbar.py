from tkinter import *
from tkinter.ttk import *


class ProgressBar:

    def __init__(self, max_value, title=""):
        self.progress_window = Tk()
        self.progress_window.title(title)
        self.progress_bar = Progressbar(self.progress_window, orient=HORIZONTAL, length=300)
        self.max_value = max_value
        self.percent = None
        self.percent_label = None
        self.init_progress()

    def init_progress(self):
        self.progress_bar.pack(padx=10, pady=10)
        self.percent = StringVar()
        self.percent_label = Label(self.progress_window, textvariable=self.percent).pack()

    def start(self):
        self.progress_window.mainloop()

    def increment_by(self, value):
        self.progress_bar['value'] += value
        self.percent.set(str(int(self.progress_bar['value'])) + "%")
        self.progress_window.update_idletasks()

    def destroy(self):
        self.progress_window.destroy()


