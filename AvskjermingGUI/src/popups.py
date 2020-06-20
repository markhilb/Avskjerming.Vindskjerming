import tkinter
import re
from tkinter import messagebox
from decimal import Decimal


class EditGlassPopup(tkinter.Tk):
    def __init__(self, canvas, glass_id, current_width, current_height):
        self.canvas = canvas
        self.glass_id = glass_id
        super().__init__()
        self.config(bg="white")
        self.wm_title("Rediger glass")

        # Frame for width/height entries
        entries_frame = tkinter.Frame(self, bg="white")
        entries_frame.pack(side="top", padx=20, pady=20)

        # Label for new width entry
        label = tkinter.Label(entries_frame, text="Ny bredde:", bg="white")
        label.grid(row=0, column=0)

        # Entry for new width
        self.width_entry = tkinter.Entry(entries_frame)
        self.width_entry.insert(0, current_width)
        self.width_entry.grid(row=0, column=1)

        # Label for new height height
        label = tkinter.Label(entries_frame, text="Ny høyde:", bg="white")
        label.grid(row=1, column=0)

        # Entry for new height
        self.height_entry = tkinter.Entry(entries_frame)
        self.height_entry.insert(0, current_height)
        self.height_entry.grid(row=1, column=1)

        # Frame for buttons
        buttons_frame = tkinter.Frame(self, bg="white")
        buttons_frame.pack(side="top", padx=20, pady=20)

        # Buttons for various actions
        ok = tkinter.Button(buttons_frame, text="Ok", command=self.edit_glass, bg="white")
        cancel = tkinter.Button(buttons_frame, text="Avbryt", command=self.destroy, bg="white")
        delete_button = tkinter.Button(buttons_frame, text="Slett", command=self.delete, bg="white")
        ok.grid(row=0, column=0, padx=10)
        cancel.grid(row=0, column=1, padx=10)
        delete_button.grid(row=0, column=2, padx=10)


    def validate_and_get_entry(self, entry):
        # Remove all non-numbers from entry_val, and replace comma with period
        entry_val = re.sub("[^0-9,\.]", "", entry.get()).replace(",", ".")
        entry.delete(0, "end")
        entry.insert(0, entry_val)
        if entry_val == "":
            return False

        try:
            value = Decimal(entry_val)
            if value < 0:
                return False

            return value
        except:
            return  False


    def edit_glass(self):
        if (new_width := self.validate_and_get_entry(self.width_entry)) and \
                (new_height := self.validate_and_get_entry(self.height_entry)):
            self.canvas.edit_glass(self.glass_id, new_width, new_height)
            self.destroy()


    def delete(self):
        self.canvas.delete_glass(self.glass_id)
        self.destroy()


class EditPostOrWallmountPopup(tkinter.Tk):
    def __init__(self, canvas, item_id, current_height):
        self.canvas = canvas
        self.item_id = item_id
        super().__init__()
        self.config(bg="white")
        self.wm_title("Rediger glass")

        # Frame for width/height entries
        entries_frame = tkinter.Frame(self, bg="white")
        entries_frame.pack(side="top", padx=20, pady=20)

        # Label for new height entry
        label = tkinter.Label(entries_frame, text="Ny høyde:", bg="white")
        label.grid(row=0, column=0)

        # Entry for new height
        self.height_entry = tkinter.Entry(entries_frame)
        self.height_entry.insert(0, current_height)
        self.height_entry.grid(row=0, column=1)

        # Frame for buttons
        buttons_frame = tkinter.Frame(self, bg="white")
        buttons_frame.pack(side="top", padx=20, pady=20)

        # Buttons for various actions
        ok = tkinter.Button(
            buttons_frame, text="Ok", command=self.edit_item, bg="white"
        )

        cancel = tkinter.Button(buttons_frame, text="Avbryt", command=self.destroy, bg="white")
        delete_button = tkinter.Button(buttons_frame, text="Slett", command=self.delete, bg="white")
        ok.grid(row=0, column=0, padx=10)
        cancel.grid(row=0, column=1, padx=10)
        delete_button.grid(row=0, column=2, padx=10)


    def validate_and_get_entry(self, entry):
        # Remove all non-numbers from entry_val, and replace comma with period
        entry_val = re.sub("[^0-9,\.]", "", entry.get()).replace(",", ".")
        entry.delete(0, "end")
        entry.insert(0, entry_val)
        if entry_val == "":
            return False

        try:
            value = Decimal(entry_val)
            if value < 0:
                return False

            return value
        except:
            return  False


    def edit_item(self):
        if (new_height := self.validate_and_get_entry(self.height_entry)):
            self.canvas.edit_post_or_wallmount(self.item_id, new_height)
            self.destroy()


    def delete(self):
        self.canvas.delete_post_or_wallmount(self.item_id)
        self.destroy()

