import tkinter
from config import *


class TopFrame:
    def __init__(self, master, undo_func):
        self.master = master
        self.main_frame = tkinter.Frame(self.master, bg="white")
        self.main_frame.pack(side="top", fill="x")

        self.undo_button = tkinter.Button(self.main_frame, text="Angre", command=undo_func)
        self.undo_button.pack(side="left", padx=PAD_X)

        self.total_width_container = tkinter.Frame(self.main_frame)
        self.total_width_container.pack(side="top", pady=10)

        self.total_width_label = tkinter.Label(self.total_width_container, text="Total lengde:")
        self.total_width_entry = tkinter.Entry(self.total_width_container)
        self.total_width_label.pack(side="left")
        self.total_width_entry.pack(side="left")
        self.total_width_entry.insert(0, 0)

        self.current_weight_label = tkinter.Label(self.main_frame, text ="Vekt: 0 kg")
        self.current_weight_label.pack(side="right", padx=PAD_X, pady=20)

    @property
    def total_width(self):
        total_width = self.total_width_entry.get()
        if total_width is "" or float(total_width) <= 0:
            tkinter.messagebox.showinfo("Warning", "Den totale lengden kan ikke være 0/tom!")
            return False
        return Decimal(str(total_width))