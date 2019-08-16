import tkinter
from tkinter import messagebox
from decimal import Decimal
from items import Wallmount, Post, Glass
from config import CANVAS_LEFT_START, POST_WIDTH, POST_LAST_WIDTH, WALLMOUNT_WIDTH

class Canvas(tkinter.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="red", highlightthickness=0)
        self.items = []
        self.current_width = Decimal("0")
        self.current_xpos = CANVAS_LEFT_START

    def auto_calculate(self, total_width, left, width, height, right):
        self.clear()
        if left is Post:
            if not self.add_post(total_width, height):
                return
        else:
            if not self.add_wallmount(total_width, height):
                return
        
        total_width_minus_edges = (total_width - self.current_width - (POST_WIDTH if right is Post else WALLMOUNT_WIDTH))
        num =  total_width_minus_edges / (Decimal(width) + POST_WIDTH)
        # check_num = num * Decimal(width) + POST_WIDTH 
        # if check_num > total_width_minus_edges - POST_WIDTH and check_num < total_width_minus_edges + POST_WIDTH:
        #     messagebox.showinfo("Warning", "Denne kombinasjonen går ikke opp!\nVelg en annen bredde på glassene!")
        #     return
        
        for _ in range(int(num)):
            self.add_glass(total_width, width, height)
            self.add_post(total_width, height)
        self.add_glass(total_width, width, height)

        if right is Post:
            if not self.add_post(total_width, height):
                self.clear()
                return
        else:
            if not self.add_wallmount(total_width, height):
                self.clear()
                return
            
    def add_wallmount(self, total_width, height):
        if self.current_width + WALLMOUNT_WIDTH > total_width:
            if not self.cut_glass(WALLMOUNT_WIDTH):
                return False
        wallmount = Wallmount(self, self.current_xpos, height)
        self.add_item(wallmount)
        return True

    def add_post(self, total_width, height):
        if self.current_width + POST_LAST_WIDTH > total_width:
            if not self.cut_glass(POST_LAST_WIDTH):
                return False
        post = Post(self, self.current_xpos, height, True)
        self.add_item(post)
        return True

    def add_glass(self, total_width, width, height):
        if self.current_width + width > total_width:
            width = total_width - self.current_width
        if width <= 0:
            return False
        glass = Glass(self, self.current_xpos, width, height)
        self.add_item(glass)
        return True

    def cut_glass(self, width):
        item = self.items.pop()
        if not isinstance(item, Glass):
            self.items.append(item)
            return False
        self.current_width -= item.width
        new_glass = Glass(self, self.current_xpos, item.width - width, item.height)
        self.add_item(new_glass)
        item.delete()
        return True

    def add_item(self, item):
        # las_item = self.items[len(sele)]
        self.items.append(item)
        self.current_width += item.width
        self.current_xpos += item.width

    def clear(self):
        for item in self.items:
            item.delete()
        self.current_width = Decimal("0")
        self.current_xpos = CANVAS_LEFT_START