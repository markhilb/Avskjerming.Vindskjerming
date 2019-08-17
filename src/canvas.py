import tkinter
from tkinter import messagebox
from tkinter.simpledialog import askstring
from decimal import Decimal
from items import Wallmount, Post, Glass, LengthBar
from config import CANVAS_LEFT_START, POST_WIDTH, POST_LAST_WIDTH, WALLMOUNT_WIDTH

class Canvas(tkinter.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="red", highlightthickness=0)
        self.items = []
        self.current_width = Decimal("0")
        self.current_xpos = CANVAS_LEFT_START
        self.length_bar = LengthBar(self)

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
        if len(self.items) is not 0:
            if not isinstance(self.items[len(self.items) - 1], Glass):
                return False
        if self.current_width + WALLMOUNT_WIDTH >= total_width:
            if not self.cut_glass(total_width, (self.current_width + WALLMOUNT_WIDTH) - total_width):
                return False
        wallmount = Wallmount(self, self.current_xpos, height)
        self.items.append(wallmount)
        self.update()
        return True

    def add_post(self, total_width, height):
        if len(self.items) is not 0:
            if not isinstance(self.items[len(self.items) - 1], Glass):
                return False
        if self.current_width + POST_LAST_WIDTH >= total_width:
            if not self.cut_glass(total_width, (self.current_width + POST_LAST_WIDTH) - total_width):
                return False
        post = Post(self, self.current_xpos, height, True)
        self.items.append(post)
        self.update()
        return True

    def add_glass(self, total_width, width, height):
        if len(self.items) is 0 or self.current_width >= total_width:
            return False
        if isinstance(self.items[len(self.items) - 1], Post):
            if len(self.items) is not 1:
                self.items[len(self.items) - 1].is_last = False
                self.update()
        elif isinstance(self.items[len(self.items) - 1], Glass):
            return False
        if self.current_width + width > total_width:
            width = total_width - self.current_width 
        glass = Glass(self, total_width, self.current_xpos, width, height)
        self.items.append(glass)
        self.update()
        return True


    def cut_glass(self, total_width, width):
        if len(self.items) is 0:
            return False
        glass = self.items.pop()
        if glass.width <= width:
            self.items.append(glass)
            return False
        self.update()
        new_glass = Glass(self, total_width, self.current_xpos, glass.width - width, glass.height)
        self.items.append(new_glass)
        glass.delete()
        self.update()
        return True

    def update(self):
        self.current_width = Decimal("0")
        self.current_xpos = CANVAS_LEFT_START
        for item in self.items:
            self.current_width += item.width
            self.current_xpos += item.display_width
        self.length_bar.update(self.current_width, self.current_xpos)

    def clear(self):
        for item in self.items:
            item.delete()
        self.items.clear()
        self.current_width = Decimal("0")
        self.current_xpos = CANVAS_LEFT_START
        self.length_bar.update(self.current_width, self.current_xpos)

    def undo(self):
        if len(self.items) is not 0:
            item = self.items.pop()
            item.delete()
        if len(self.items) is not 0 and isinstance(self.items[len(self.items) - 1], Post):
            self.items[len(self.items) - 1].is_last = True
        self.update()

    def edit_glass(self, id, total_width, width):
        for i, item in enumerate(self.items):
            if item.id is id:
                second_half = self.items[i+1:]
                self.items = self.items[:i+1]
                old_glass = self.items.pop()
                old_glass.delete()
                self.update()
                self.add_glass(total_width, width, old_glass.height)
                if width >= old_glass.width:
                    for thing in second_half:
                        if isinstance(thing, Wallmount):
                            self.add_wallmount(total_width, thing.height-1)
                        elif isinstance(thing, Post):
                            self.add_post(total_width, thing.height-1)
                        else:
                            self.add_glass(total_width, thing.width, thing.height)
                        thing.delete()
                else:
                    pass

                return True
        return False


    def move_items(self, idx, total_width):
        self.current_width = Decimal("0")
        self.current_xpos = CANVAS_LEFT_START
        for i in range(idx):
            self.current_width += self.items[i].width
            self.current_xpos += self.items[i].display_width
        for i in range(idx, len(self.items)):
            item = self.items[i]
            item.delete()
            if isinstance(item, Wallmount):
                new_item = Wallmount(self, self.current_xpos, item.height)
            elif isinstance(item, Post):
                new_item = Post(self, self.current_xpos, item.height, item.is_last)
            else:
                new_item = Glass(self, total_width, self.current_xpos, item.width, item.height)
            self.items[i] = new_item
            self.current_width += new_item.width
            self.current_xpos += new_item.display_width
        
    def delete_glass(self, id, total_width):
        for i, item in enumerate(self.items):
            if item.id is id:
                item.delete()
                self.items.remove(item)
                if len(self.items) > i:
                    next_item = self.items[i]
                    next_item.delete()
                    self.items.remove(next_item)
                    self.move_items(i, total_width)
                self.update()
                return True
        return False