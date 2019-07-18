import tkinter, collections
import tkinter.messagebox
from decimal import Decimal
from canvas_items import Item, Wallmount, Post, Glass, LengthBar
from config import *


class Main:
    def __init__(self, master):
        self.master = master
        self.current_width = Decimal('0')
        self.current_weight = Decimal('0')
        self.total_width = Decimal('0')



