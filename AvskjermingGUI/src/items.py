import tkinter
from decimal import Decimal
from popups import EditGlassPopup, EditPostOrWallmountPopup
from config import CANVAS_BASELINE, CANVAS_LEFT_START, GLASS_BASELINE, WALLMOUNT_WIDTH, POST_WIDTH, POST_LAST_WIDTH, POST_BASE_WIDTH, POST_BASE_HEIGHT, \
                   LENGTH_BAR_SIDES_TOP, LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_BOTTOM, LENGTH_BAR_TOP, LENGTH_BAR_BOTTOM, LENGTH_BAR_LABEL_TOP, \
                   WALLMOUNT_DISPLAY_WIDTH, POST_DISPLAY_WIDTH, POST_BASE_DISPLAY_WIDTH, POST_BASE_DISPLAY_HEIGHT, WALLMOUNT_PACKAGING, POST_PACKAGING,\
                   WALLMOUNT_WEIGHT_MULTIPLYER, POST_WEIGHT_MULTIPLYER, POST_MOUNT_WEIGHT, GLASS_WEIGHT_MULTIPLYER, GLASS_PACKAGING, LENGTH_BAR_SIDES_HEIGHT,\
                   LEFT_HEIGHT_BAR_START, RIGHT_HEIGHT_BAR_OFFSET, RIGHT_HEIGHT_LABEL_OFFSET


class Wallmount:
    def __init__(self, canvas, xpos, height):
        self.canvas = canvas
        self.xpos = xpos
        self.width = WALLMOUNT_WIDTH
        self.display_width = WALLMOUNT_DISPLAY_WIDTH
        self.height = height
        self.display_height = height + 5
        self.color = "gray"

        self.id = canvas.create_rectangle(
            self.xpos,
            CANVAS_BASELINE - self.display_height,
            self.xpos + self.display_width,
            CANVAS_BASELINE,
            fill=self.color
        )

        canvas.tag_bind(
            self.id,
            "<Button-1>",
            lambda *args: EditPostOrWallmountPopup(canvas, self.id, self.height)
        )


    def delete(self):
        self.canvas.delete(self.id)


    @property
    def weight(self):
        return self.height * WALLMOUNT_WEIGHT_MULTIPLYER, WALLMOUNT_PACKAGING


class Post:
    def __init__(self, canvas, xpos, height, is_last):
        self.canvas = canvas
        self.xpos = xpos
        self.display_width = POST_DISPLAY_WIDTH
        self.height = height
        self.display_height = height + 5
        self.is_last = is_last
        self.color = "black"

        self.id = canvas.create_rectangle(
            self.xpos,
            CANVAS_BASELINE - self.display_height,
            self.xpos + self.display_width,
            CANVAS_BASELINE,
            fill=self.color
        )

        self.base = canvas.create_rectangle(
            self.xpos - POST_BASE_DISPLAY_WIDTH,
            CANVAS_BASELINE - POST_BASE_DISPLAY_HEIGHT,
            self.xpos + self.display_width + POST_BASE_DISPLAY_WIDTH,
            CANVAS_BASELINE,
            fill=self.color
        )

        canvas.tag_bind(
            self.id,
            "<Button-1>",
            lambda *args: EditPostOrWallmountPopup(canvas, self.id, self.height)
        )


    @property
    def width(self):
        return (POST_LAST_WIDTH if self.is_last else POST_WIDTH)


    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.base)


    @property
    def weight(self):
        return (self.height * POST_WEIGHT_MULTIPLYER) + POST_MOUNT_WEIGHT, POST_PACKAGING


class Glass:
    def __init__(self, canvas, xpos, width, height):
        self.canvas = canvas
        self.xpos = xpos
        self.display_width = width
        self.width = width
        self.display_height = height
        self.height = height
        self.color = "blue"

        self.id = canvas.create_rectangle(
            self.xpos,
            GLASS_BASELINE - self.display_height,
            self.xpos + self.display_width,
            GLASS_BASELINE,
            fill=self.color
        )

        self.label = canvas.create_text(
            self.xpos + (self.display_width / 2),
            GLASS_BASELINE - self.display_height - 30,
            text=f"{self.width}x{self.height}"
        )

        canvas.tag_bind(
            self.id,
            "<Button-1>",
            lambda *args: EditGlassPopup(canvas, self.id, self.width, self.height)
        )


    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.label)


    @property
    def weight(self):
        return self.width * self.height * GLASS_WEIGHT_MULTIPLYER, GLASS_PACKAGING


class GlassPolygon(Glass):
    def __init__(self, canvas, xpos, width, height, second_height):
        self.canvas = canvas
        self.xpos = xpos
        self.display_width = width
        self.width = width
        self.display_height = height
        self.second_display_height = second_height
        self.height = height
        self.second_height = second_height
        self.color = "blue"

        self.id = canvas.create_polygon([
                self.xpos,\
                GLASS_BASELINE - self.display_height,\
                self.xpos,\
                GLASS_BASELINE,\
                self.xpos + self.display_width,\
                GLASS_BASELINE,\
                self.xpos + self.display_width,\
                GLASS_BASELINE - self.second_display_height
            ],
            fill=self.color
        )

        self.label = canvas.create_text(
            self.xpos + (self.display_width / 2),
            GLASS_BASELINE - self.display_height - 30,
            text=self.width
        )


    @property
    def weight(self):
        area = (self.width * self.height) - ((self.width * (self.height - self.second_height)) / 2)
        return area * GLASS_WEIGHT_MULTIPLYER, GLASS_PACKAGING


class LengthBar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.left = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.right = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.bar = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.label = self.canvas.create_text(0, 0, text="")


    def update(self, current_width, xpos, base_xpos):
        self.canvas.delete(self.bar)
        self.canvas.delete(self.left)
        self.canvas.delete(self.right)
        self.canvas.delete(self.label)
        if current_width > 0:
            self.left = self.canvas.create_rectangle(
                base_xpos,
                LENGTH_BAR_SIDES_TOP,
                base_xpos + LENGTH_BAR_THICKNESS,
                LENGTH_BAR_SIDES_BOTTOM, fill="black"
            )

            self.bar = self.canvas.create_rectangle(
                base_xpos,
                LENGTH_BAR_TOP,
                xpos,
                LENGTH_BAR_BOTTOM,
                fill="black"
            )

            self.right = self.canvas.create_rectangle(
                xpos - LENGTH_BAR_THICKNESS,
                LENGTH_BAR_SIDES_TOP,
                xpos,
                LENGTH_BAR_SIDES_BOTTOM,
                fill="black"
            )

            self.label = self.canvas.create_text(
                (xpos  + base_xpos) / 2,
                LENGTH_BAR_LABEL_TOP,
                text=current_width
            )

