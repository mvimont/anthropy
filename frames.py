from tkinter import ttk
import tkinter as tk

from backend.pilesort import Pilesort

class HomePage(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Welcome to AnthroPy", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Create new freelist",
                  command=lambda: container.switch_frame(FreeList)).pack(side="bottom")

class FreeList(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Create a freelist", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        self.entry = tk.Text(self, undo=True, height=1, width=20)
        self.entry.pack()
        tk.Button(self, text="Add entry to freelist",
                  command=lambda: self.add_new_item(container)).pack()
        self.current_items = tk.Label(self, text=f"Current Items: {container.pilesort.freelist if len(container.pilesort.freelist) > 0 else None}")
        self.current_items.pack()
        tk.Button(self, text="Start Pilesort",
                  command=lambda: container.switch_frame(Pilesort)).pack(side="bottom")
    
    def add_new_item(self, container):
        new_item = self.entry.get('1.0', tk.END).strip('\n')
        container.pilesort.add_freelist_item(new_item)
        self.entry.delete('1.0', tk.END)
        self.current_items.destroy()
        self.current_items = tk.Label(self, text=f"Current Items: {container.pilesort.freelist}")
        self.current_items.pack()

class Pilesort(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Pilesort Grouping", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Show results",
                  command=lambda: container.switch_frame(ResultsPage)).pack()

class ResultsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Distance Matrix", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Home",
                  command=lambda: master.switch_frame(HomePage)).pack()