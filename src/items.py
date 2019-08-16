import tkinter
from config import CANVAS_BASELINE, GLASS_BASELINE, WALLMOUNT_WIDTH, POST_WIDTH, POST_LAST_WIDTH, POST_BASE_WIDTH, POST_BASE_HEIGHT


class Wallmount:
    def __init__(self, canvas, xpos, height):
        self.canvas = canvas
        self.xpos = xpos
        self.width = WALLMOUNT_WIDTH
        self.height = height + 1
        self.color = "gray"

        self.id = canvas.create_rectangle(self.xpos, CANVAS_BASELINE - self.height, self.xpos + self.width, CANVAS_BASELINE, fill=self.color)

    def delete(self):
        self.canvas.delete(self.id)


class Post:
    def __init__(self, canvas, xpos, height, is_first_or_last):
        self.canvas = canvas
        self.xpos = xpos
        self.height = height + 1
        self.is_first_or_last = is_first_or_last
        self.color = "black"

        self.id = canvas.create_rectangle(self.xpos, CANVAS_BASELINE - self.height, self.xpos + POST_WIDTH, CANVAS_BASELINE, fill=self.color)

        self.base = canvas.create_rectangle(self.xpos - POST_BASE_WIDTH, CANVAS_BASELINE - POST_BASE_HEIGHT, self.xpos + POST_WIDTH + POST_BASE_WIDTH, CANVAS_BASELINE, fill=self.color)

    @property
    def width(self):
        return (POST_LAST_WIDTH if self.is_first_or_last else POST_WIDTH) 

    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.base)


class Glass:
    def __init__(self, canvas, xpos, width, height):
        self.canvas = canvas
        self.xpos = xpos
        self.width = width
        self.height = height
        self.color = "blue"

        self.id = canvas.create_rectangle(self.xpos, GLASS_BASELINE - self.height, self.xpos + self.width, GLASS_BASELINE, fill=self.color)

        self.label = self.canvas.create_text(self.xpos + (self.width / 2), GLASS_BASELINE - self.height - 30, text=self.width)

    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.label)
    