import tkinter
from config import *

class Item:
    WALLMOUNT = 0
    POST = 1
    GLASS = 2



class Wallmount:
    def __init__(self, canvas, xpos, height, canvas_xpos, is_last, is_first):
        self.canvas = canvas
        self.is_last = is_last
        self.is_first = is_first
        self.width = WALLMOUNT_WIDTH
        self.xpos = xpos
        self.height = height
        self.canvas_xpos = canvas_xpos
        self.canvas_width = self.width * WALLMOUNT_SCALE
        self.weight = self.width * self.height  * WALLMOUNT_WEIGHT_MULTIPLYER
        self.id = canvas.create_rectangle(self.canvas_xpos, CANVAS_BASELINE - self.height, self.canvas_xpos + self.canvas_width, CANVAS_BASELINE, fill="gray")

    def delete(self):
        self.canvas.delete(self.id)


class Post:
    def __init__(self, canvas, xpos, height, canvas_xpos, is_last, is_first):
        self.canvas = canvas
        self.is_last = is_last
        self.is_first = is_first
        self._width = POST_WIDTH
        if is_first:
            self.xpos = xpos + POST_BASE_WIDTH
            self.canvas_xpos = canvas_xpos + POST_BASE_WIDTH
        else:
            self.xpos = xpos
            self.canvas_xpos = canvas_xpos
        self.height = height
        self._canvas_width = self.width * POST_SCALE
        self.weight = self._width * self.height  * POST_WEIGHT_MULTIPLYER
        self.id = canvas.create_rectangle(self.canvas_xpos, CANVAS_BASELINE - self.height, self.canvas_xpos + self._canvas_width, CANVAS_BASELINE, fill="black")
        self.canvas_base_width = (POST_BASE_WIDTH * POST_SCALE)
        self.base = canvas.create_rectangle(self.canvas_xpos - self.canvas_base_width,                      \
                                            CANVAS_BASELINE - POST_BASE_HEIGHT,                      \
                                            self.canvas_xpos + self.canvas_base_width + self._canvas_width, \
                                            CANVAS_BASELINE, fill="black")

    @property
    def width(self):
        if self.is_last or self.is_first:
            return self._width + POST_BASE_WIDTH
        return self._width

    @property
    def canvas_width(self):
        if self.is_last or self.is_first:
            return self._canvas_width + self.canvas_base_width
        return self._canvas_width

    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.base)


class Glass:
    def __init__(self, canvas, xpos, width, height, canvas_xpos, is_last, is_first):
        self.canvas = canvas
        self.is_last = is_last
        self.is_first = is_first
        self.xpos = xpos
        self.width = width
        self.height = height
        self.canvas_xpos = canvas_xpos
        self.canvas_width = self.width * GLASS_SCALE
        self.weight = self.width * self.height  * GLASS_WEIGHT_MULTIPLYER
        self.id = canvas.create_rectangle(self.canvas_xpos, GLASS_BASELINE - self.height, self.canvas_xpos + self.canvas_width, GLASS_BASELINE, fill="blue")
        self.label = canvas.create_text(self.canvas_xpos + (self.canvas_width / 2), GLASS_BASELINE - self.height - 30, text=width)

    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.label)


class LengthBar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.left = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.right = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.bar = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.label = self.canvas.create_text(0, 0, text="")
    

    def update(self, current_width, canvas_width):
        self.canvas.delete(self.bar)
        self.canvas.delete(self.left)
        self.canvas.delete(self.right)
        self.canvas.delete(self.label)
        if canvas_width > 0:
            self.left = self.canvas.create_rectangle(1, LENGTH_BAR_SIDES_TOP, LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_BOTTOM, fill="black")
            self.bar = self.canvas.create_rectangle(0, LENGTH_BAR_TOP, canvas_width, LENGTH_BAR_BOTTOM, fill="black")
            self.right = self.canvas.create_rectangle(canvas_width - LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_TOP, canvas_width, LENGTH_BAR_SIDES_BOTTOM, fill="black")
            self.label = self.canvas.create_text(canvas_width / 2, LENGT_BAR_LABEL_TOP, text=current_width)
