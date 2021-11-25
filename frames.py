import logging
from tkinter import IntVar, ttk
import tkinter as tk
from pandastable import Table

frame_logger = logging.getLogger("FrameLogger")

class HomePage(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Welcome to AnthroPy", font=('Helvetica', 18, "bold")).place(relheight=0.1, relwidth=1, rely=0.25)
        tk.Button(self, text="Create new freelist",
                  command=lambda: container.switch_frame(FreeList)).place(relheight=0.1, relwidth=0.80, relx=0.1, rely=0.5)
        

class FreeList(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Create a freelist", font=('Helvetica', 18, "bold")).place(relheight=0.1, relwidth=1, rely=0.1)
        self.current_items = tk.Label(self, text=f"Current Items: {container.pilesort.freelist if len(container.pilesort.freelist) > 0 else None}")
        self.current_items.place(relheight=0.1, relwidth=1, rely=0.2)
        self.entry = tk.Text(self, undo=True)
        self.entry.place(relheight=0.06, relwidth=0.3, rely=0.5, relx=0.35)
        self.add_item_button = tk.Button(self, text="Add entry to freelist",
                  command=lambda: self.add_new_item(container))
        self.add_item_button.place(relheight=0.1, relwidth=0.3, rely=0.6, relx=0.35)
        self.pilesort_button = tk.Button(self, text="Start Pilesort", state="disabled",
                  command=lambda: self.start_pilesort(container))
        self.pilesort_button.place(relheight=0.1, relwidth=0.3, rely=0.9, relx=0.35)
    
    def add_new_item(self, container):
        new_item = self.entry.get('1.0', tk.END).strip('\n')
        container.pilesort.add_freelist_item(new_item)
        self.entry.delete('1.0', tk.END)
        self.current_items.destroy()
        self.current_items = tk.Label(self, text=f"Current Items: {container.pilesort.freelist}")
        self.current_items.place(relheight=0.1, relwidth=1, rely=0.2)

        self.pilesort_button.destroy()
        self.pilesort_button = tk.Button(self, text="Start Pilesort",
                  command=lambda: self.start_pilesort(container))
        self.pilesort_button.place(relheight=0.1, relwidth=0.3, rely=0.9, relx=0.35)      
        
    def start_pilesort(self, container):
        container.pilesort.finalize_freelist()
        container.switch_frame(PilesortFrame)

class PilesortFrame(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Pilesort Grouping", font=('Helvetica', 18, "bold")).place(relheight=0.1, relwidth=1, rely=0.1)
        tk.Label(self, text=f"Original freelist: {container.pilesort.freelist}").place(relheight=0.1, relwidth=1, rely=0.2)
        self.generate_item_box(container)
        self.generate_group_box(container)
        self.group_button = tk.Button(self, text="Group selected pair",
                  command=lambda: self.submit_pair(container))
        self.group_button.place(relheight=0.1, relwidth=0.3, rely=0.9, relx=0.35)   

    def generate_item_box(self, container):
        self.item_box = tk.LabelFrame(self, text="Items")
        self.item_box.place(relwidth=0.45, relheight=0.5, relx=0.04, rely=0.4)
        get_match = None
        y_flt = 0.00
        x_flt = 0.05
        self.item_box.check_vars = {}
        for item in list(container.pilesort.freelist):
            value = item
            if not self.item_box.check_vars.get(item):
                self.item_box.check_vars[item] = IntVar()
            tk.Checkbutton(self.item_box, variable=self.item_box.check_vars[item], text=item).place(relheight=0.1, relx=x_flt, rely=y_flt, anchor='nw')
            if y_flt < 1.0:
                y_flt += 0.1
            else:
                y_flt = 0.00
                x_flt += 0.5

    def generate_group_box(self, container):
        self.group_box = tk.LabelFrame(self, text="Groups")
        self.group_box.place(relwidth=0.45, relheight=0.5, relx=0.5, rely=0.4)
        self.group_box.check_vars = {}
        y_flt = 0.00
        x_flt = 0.05
        for group in list(container.pilesort.groupings):
            value = group
            if not self.group_box.check_vars.get(group):
                self.group_box.check_vars[group] = IntVar()
            tk.Checkbutton(self.group_box, variable=self.group_box.check_vars[group], text=group).place(relheight=0.1, relx=x_flt, rely=y_flt, anchor='nw')
            if y_flt < 1.0:
                y_flt += 0.1
            else:
                y_flt = 0.00
                x_flt += 0.5

    def submit_pair(self, container):
        selected_items = [k for k, v in self.item_box.check_vars.items() if v.get() == 1] 
        selected_groups = [k for k, v in self.group_box.check_vars.items() if v.get() == 1] 
        selection = list(set(selected_items + selected_groups))
        if len(selection) != 2:
            frame_logger.error("Invalid select, only two selections allowed. %d chosen", len(selection))
            return
        submitted_select = []
        if len(selected_items) == 1:
            submitted_select.insert(0, selected_items[0])
        elif len(selected_items) == 2:
            submitted_select = selected_items
        if len(selected_groups)  == 1:
            submitted_select.insert(1, selected_groups[0])
        elif len(selected_groups) == 2:
            submitted_select = selected_groups

        container.pilesort.add_freelist_item_to_grouping(submitted_select[1], submitted_select[0])
        self.item_box.destroy()
        self.group_box.destroy()
        if len(container.pilesort.groupings) == 1 and len(container.pilesort.freelist) == 0:
            container.switch_frame(ResultsPage)
        else:
            self.generate_item_box(container)
            self.generate_group_box(container)

class ResultsPage(tk.Frame):
    def __init__(self, container):
        tk.Frame.__init__(self, container)
        tk.Label(self, text="Distance Matrix", font=('Helvetica', 18, "bold")).place(relheight=0.1, relwidth=1, rely=0.1)
        df = container.pilesort.dist_matrix
        df.insert(0, '', (list(df.index)))
        self.table = Table(self, dataframe=container.pilesort.dist_matrix,
                                showtoolbar=True, showstatusbar=True)
        self.table.show()
