import tkinter
from decimal import Decimal
from config import PAD_X
from canvas_items import LengthBar

class MiddleFrame:
    def __init__(self, master):
        self.master = master
        self.canvas = tkinter.Canvas(self.master, bg="lightgray")
        self.canvas.pack(side="top", fill="both", expand=1, padx=PAD_X)
        
        self.current_canvas_width = Decimal('0')
        self.canvas_items = []

        self.length_bar = LengthBar(self.canvas)