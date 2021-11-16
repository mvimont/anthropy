import tkinter as tk
from backend.pilesort import Pilesort

from frames import HomePage

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('AnthroPy')
        self.geometry('500x500')
        self.pilesort = Pilesort()
        self._frame = None
        self.switch_frame(HomePage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()