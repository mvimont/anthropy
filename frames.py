import logging
from tkinter import ttk
import tkinter as tk

from backend.pilesort import Pilesort

frame_logger = logging.getLogger("FrameLogger")

class HomePage(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Welcome to AnthroPy", font=('Helvetica', 18, "bold")).grid(pady=5)
        tk.Button(self, text="Create new freelist",
                  command=lambda: container.switch_frame(FreeList)).grid(pady=10)

class FreeList(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Create a freelist", font=('Helvetica', 18, "bold")).grid(pady=10)
        self.current_items = tk.Label(self, text=f"Current Items: {container.pilesort.freelist if len(container.pilesort.freelist) > 0 else None}")
        self.current_items.grid(row=1, pady=10)
        self.entry = tk.Text(self, undo=True, height=1, width=20)
        self.entry.grid(pady=10)
        tk.Button(self, text="Add entry to freelist",
                  command=lambda: self.add_new_item(container)).grid(pady=10)
        tk.Button(self, text="Start Pilesort",
                  command=lambda: self.start_pilesort(container)).grid(pady=10)
    
    def add_new_item(self, container):
        new_item = self.entry.get('1.0', tk.END).strip('\n')
        container.pilesort.add_freelist_item(new_item)
        self.entry.delete('1.0', tk.END)
        self.current_items.destroy()
        self.current_items = tk.Label(self, text=f"Current Items: {container.pilesort.freelist}")
        self.current_items.grid(row=1, pady=10)
    
    def start_pilesort(self, container):
        container.pilesort.finalize_freelist()
        container.switch_frame(PilesortFrame)

class PilesortFrame(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Pilesort Grouping", font=('Helvetica', 18, "bold")).grid(columnspan=4, pady=5)
        tk.Label(self, text=f"Original freelist: {container.pilesort.freelist}").grid(columnspan=4, pady=2)
        get_match=None
        self.item_box = tk.LabelFrame(self, text="Items")
        self.item_box.grid(row=2)
        for item in list(container.pilesort.freelist):
            tk.Checkbutton(self.item_box, variable=get_match, text=item).grid(pady=2, sticky='w')
        self.grouping_box = tk.LabelFrame(self, text="Groupings")
        self.grouping_box.grid(row=2, column=4)
        for group in container.pilesort.groupings:
            tk.Checkbutton(self.grouping_box, variable=get_match, text=group).grid(pady=2, stick='w')
        tk.Button(self, text="Show results",
                  command=lambda: container.switch_frame(ResultsPage)).grid(row=8, columnspan=4, pady=50)

    def generate_item_box(self, container):
        item_box = tk.LabelFrame(self, text="Items")
        item_box.grid(row=2)
        for item in list(container.pilesort.freelist):
            tk.Checkbutton(self.item_box, variable=get_match, text=item).grid(pady=2, sticky='w')
    
    def submit_pair(self, container):
        selection = [self.item_box] + [self.grouping_box]
        if len(selection) != 2:
            frame_logger.error("Invalid select, only two selections allowed. %d chosen", len(selection))
            return
        container.pilesort.add_freelist_item_to_grouping(selection[1], selection[0])
        self.item_box.destroy()
        self.grouping_box.destroy()

class ResultsPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Distance Matrix", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Home",
                  command=lambda: master.switch_frame(HomePage)).pack()