import tkinter
import re
from tkinter import messagebox, ttk
from decimal import Decimal, InvalidOperation
from canvas import Canvas
from items import Wallmount, Post, Glass, GlassPolygon
from config import DROPDOWN_WIDTH


class MainPage(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(bg="white")
        self.canvas = Canvas(self)

        # Top label
        automatic_calculation_label = tkinter.Label(
            self, text="Automatisk utregning", font=("", 20), bg="white"
        )

        automatic_calculation_label.pack(side="top", fill="x", pady=10)

        # Frame containing the total width entries
        total_width_frame = tkinter.Frame(self, bg="white")
        total_width_frame.grid_columnconfigure(0, weight=1)
        total_width_frame.grid_columnconfigure(3, weight=1)
        total_width_frame.pack(side="top", fill="x", pady=10)

        # The left total width entry
        total_width_l_label = tkinter.Label(
            total_width_frame, text="Total lengde venstre: ", bg="white"
        )

        total_width_l_label.grid(row=0, column=1, padx=10, sticky="w")
        self.total_width_l = tkinter.StringVar()
        total_width_l_entry = tkinter.Entry(
            total_width_frame, text=self.total_width_l, bg="white"
        )

        total_width_l_entry.grid(row=1, column=1, padx=10, sticky="w")

        # The rigth total width entry
        total_width_r_label = tkinter.Label(
            total_width_frame, text="Total lengde høyre:", bg="white"
        )

        total_width_r_label.grid(row=0, column=2, padx=10, sticky="w")
        self.total_width_r = tkinter.StringVar()
        total_width_r_entry = tkinter.Entry(
            total_width_frame, text=self.total_width_r, bg="white"
        )

        total_width_r_entry.grid(row=1, column=2, padx=10, sticky="w")

        # Frame containing top row of buttons and inputs
        top_frame = tkinter.Frame(self, bg="white")
        top_frame.grid_columnconfigure(2, weight=1)
        top_frame.grid_columnconfigure(5, weight=1)
        top_frame.pack(side="top", fill="x")

        # Reset button
        self.reset_button = tkinter.Button(
            top_frame, text="Reset",
            command=lambda: [self.canvas.clear(), self.update_packaging_list()]
        )

        self.reset_button.grid(row=0, column=0, sticky="n")

        # Undo button
        self.undo_button = tkinter.Button(
            top_frame, text="Angre",
            command=lambda: [self.canvas.undo(), self.update_packaging_list()]
        )

        self.undo_button.grid(row=0, column=1, sticky="n")

        # Dropdown for wallmoun/post on left side
        self.auto_left_item_dropdown = tkinter.StringVar()
        self.auto_left_item_dropdown.set("Veggskinne")
        auto_left_item_dropdown_menu = tkinter.OptionMenu(
            top_frame, self.auto_left_item_dropdown, *["Veggskinne", "Stolpe"]
        )

        auto_left_item_dropdown_menu.grid(row=0, column=2, padx=40, sticky="ne")
        auto_left_item_dropdown_menu.config(width=DROPDOWN_WIDTH)

        # Frame for glass size entries
        auto_glass_frame = tkinter.Frame(top_frame, bg="white")
        auto_glass_frame.grid(row=0, column=3, padx=10, sticky="n")

        # Labels for glass size entries
        glass_width_label = tkinter.Label(auto_glass_frame, text="Global bredde: ", bg="white")
        glass_width_label.grid(row=0, column=0)
        glass_height_label = tkinter.Label(auto_glass_frame, text="Global høyde: ", bg="white")
        glass_height_label.grid(row=1, column=0)

        # Entry for glass width for automatic calculation
        self.auto_glass_width = tkinter.StringVar()
        auto_glass_width_entry = tkinter.Entry(auto_glass_frame, text=self.auto_glass_width)
        auto_glass_width_entry.grid(row=0, column=1)
        auto_glass_width_entry.insert(0, 60)

        # Entry for glass height for automatic calculation
        self.auto_glass_height = tkinter.StringVar()
        auto_glass_height_entry = tkinter.Entry(auto_glass_frame, text=self.auto_glass_height)
        auto_glass_height_entry.grid(row=1, column=1)
        auto_glass_height_entry.insert(0, 60)

        # Dropdown for wallmoun/post on right side
        self.auto_right_item_dropdown = tkinter.StringVar()
        self.auto_right_item_dropdown.set("Stolpe")
        auto_right_item_dropdown_menu = tkinter.OptionMenu(
            top_frame, self.auto_right_item_dropdown, *["Veggskinne", "Stolpe"]
        )

        auto_right_item_dropdown_menu.grid(row=0, column=4, padx=40, sticky="nw")
        auto_right_item_dropdown_menu.config(width=DROPDOWN_WIDTH)

        # Frame for the packaging list
        self.packaging_frame = tkinter.Frame(top_frame, bg="white")
        self.packaging_frame.grid(row=0, column=5, padx=20, sticky="e")

        # Create a table for the packaging list
        self.packaging_table = ttk.Treeview(self.packaging_frame, height=1)
        self.packaging_table["columns"] = ("#1", "#2")
        self.packaging_table.column("#0", width=100, anchor="center")
        self.packaging_table.column("#1", width=100, anchor="center")
        self.packaging_table.column("#2", width=100, anchor="center")
        self.packaging_table.heading("#0", text="Type", anchor="center")
        self.packaging_table.heading("#1", text="Størrelse", anchor="center")
        self.packaging_table.heading("#2", text="Antall", anchor="center")
        self.packaging_table.pack(side="top", fill="x")

        # Place the canvas in middle
        self.canvas.pack(side="top", fill="both", expand=1)

        # Label for manual buttons/entries section
        automatic_calculation_label = tkinter.Label(
            self, text="Manuel utregning", font=("", 20), bg="white"
        )

        automatic_calculation_label.pack(side="top", fill="x", pady=10)

        # Bottom frame for manual buttons/inputs
        bottom_frame = tkinter.Frame(self, bg="white")
        bottom_frame.pack(side="top", fill="x", pady=20)
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(6, weight=1)

        # Button for adding wallmount
        self.wallmount_button = tkinter.Button(
            bottom_frame, text="Veggskinne", command=lambda: self.add_item(Wallmount)
        )

        self.wallmount_button.grid(row=0, column=1, padx=10, sticky="e")

        # Button for adding post
        self.post_button = tkinter.Button(
            bottom_frame, text="Stolpe", command=lambda: self.add_item(Post)
        )

        self.post_button.grid(row=0, column=2, padx=10)

        # Button for adding glass
        self.glass_button = tkinter.Button(
            bottom_frame, text="Glass", command=lambda: self.add_item(Glass)
        )

        self.glass_button.grid(row=0, column=3, padx=10)


        # Labels for glass size entries
        glass_width_label = tkinter.Label(
            bottom_frame, text="Individuell bredde: ", bg="white"
        )

        glass_width_label.grid(row=0, column=4)
        glass_height_label = tkinter.Label(
            bottom_frame, text="Individuell høyde: ", bg="white"
        )

        glass_height_label.grid(row=1, column=4)

        # Entry for glass width
        self.manual_glass_width = tkinter.StringVar()
        glass_width_entry = tkinter.Entry(bottom_frame, text=self.manual_glass_width)
        glass_width_entry.grid(row=0, column=5)
        glass_width_entry.insert(0, 60)

        # Entry for glass height
        self.manual_glass_height = tkinter.StringVar()
        glass_height_entry = tkinter.Entry(bottom_frame, text=self.manual_glass_height)
        glass_height_entry.grid(row=1, column=5, sticky="n")
        glass_height_entry.insert(0, 60)

        # Button for adding polygon glass
        self.polygon_button = tkinter.Button(
            bottom_frame, text="Skrå glass", command=lambda: self.add_item(GlassPolygon)
        )

        self.polygon_button.grid(row=0, column=6, padx=10, sticky="e")

        # Entry for height of polygon glass
        self.polygon_glass_height = tkinter.StringVar()
        polygon_entry = tkinter.Entry(bottom_frame, text=self.polygon_glass_height)
        polygon_entry.insert(0, 20)
        polygon_entry.grid(row=0, column=7, padx=10)

        # Add eventlisteners to every entry in the
        # automatic section to call auto_calculate
        setattr(
            self.total_width_l,
            "trace_id",
            self.total_width_l.trace_add(
                "write", lambda n, i, m: self.auto_calculate()
            )
        )

        setattr(
            self.total_width_r,
            "trace_id",
            self.total_width_r.trace_add(
                "write", lambda n, i, m: self.auto_calculate()
            )
        )

        setattr(
            self.auto_glass_width,
            "trace_id",
            self.auto_glass_width.trace_add(
                "write", lambda n, i, m: self.auto_calculate()
            )
        )

        setattr(
            self.auto_glass_height,
            "trace_id",
            self.auto_glass_height.trace_add(
                "write", lambda n, i, m: self.auto_calculate()
            )
        )

        setattr(
            self.auto_left_item_dropdown,
            "trace_id",
            self.auto_left_item_dropdown.trace_add(
                "write", lambda n, i, m: self.auto_calculate()
            )
        )

        setattr(
            self.auto_right_item_dropdown,
            "trace_id",
            self.auto_right_item_dropdown.trace_add(
                "write", lambda n, i, m: self.auto_calculate()
            )
        )


    def validate_and_get_entry(self, entry, less_than_value=0, greater_than_value=10000):
        """
        Validates the value in the given entry.
        Returns Decimal object of value if it passes,
        returns False otherwise
        If entry contains non-numbers, these are removed.
        Commas are also replaced with periods.
        """


        # Remove all non-numbers from entry_val, and replace comma with period
        entry_val = re.sub("[^0-9,\.]", "", entry.get()).replace(",", ".")

        # Need to remove trace before entry.set, or it will be activated
        if getattr(entry, "trace_id", False):
            entry.trace_vdelete("w", entry.trace_id)
            entry.set(entry_val)
            entry.trace_id = entry.trace_add("write", lambda n, i, m: self.auto_calculate())
        else:
            entry.set(entry_val)

        if entry_val == "":
            return False

        try:
            value = Decimal(entry_val)
            if value < less_than_value or value > greater_than_value:
                return False

            return value
        except:
            return  False


    def get_auto_glass_width(self):
        return self.validate_and_get_entry(self.auto_glass_width)


    def get_auto_glass_height(self):
        return self.validate_and_get_entry(self.auto_glass_height)


    def get_total_length_l(self):
        return self.validate_and_get_entry(self.total_width_l)


    def get_total_length_r(self):
        return self.validate_and_get_entry(self.total_width_r)


    def get_left_item(self):
        return Wallmount if self.auto_left_item_dropdown.get() == "Veggskinne" else Post


    def get_right_item(self):
        return Wallmount if self.auto_right_item_dropdown.get() == "Veggskinne" else Post


    def auto_calculate(self):
        # This is not in the if test because it can be empty
        total_width_l = self.validate_and_get_entry(self.total_width_l)
        total_width_r = self.validate_and_get_entry(self.total_width_r)
        if not (total_width_l := self.validate_and_get_entry(self.total_width_l)) or \
                not (glass_width := self.validate_and_get_entry(self.auto_glass_width)) or \
                not (height := self.validate_and_get_entry(self.auto_glass_height)):
            self.canvas.clear()
            return

        self.canvas.auto_calculate(total_width_l, total_width_r, glass_width, height)
        self.update_packaging_list()


    def add_item(self, item):
        # This is not in the if test because it can be empty
        total_width_r = self.validate_and_get_entry(self.total_width_r)
        if not (total_width_l := self.validate_and_get_entry(self.total_width_l)) or \
                not (glass_width := self.validate_and_get_entry(self.manual_glass_width)) or \
                not (height := self.validate_and_get_entry(self.manual_glass_height)):
            return

        if item is GlassPolygon:
            if not (polygon_height := self.validate_and_get_entry(self.polygon_glass_height)):
                return

            self.canvas.add_glass(
                total_width_l, total_width_r, glass_width, height, polygon_height
            )
        elif item is Wallmount:
            self.canvas.add_wallmount(total_width_l, total_width_r, height)
        elif item is Post:
            self.canvas.add_post(total_width_l, total_width_r, height)
        else:
            self.canvas.add_glass(total_width_l, total_width_r, glass_width, height)

        self.update_packaging_list()


    def update_packaging_list(self):
        pl = self.canvas.get_packaging_list()
        weight = round(pl.pop("Weight") / 1000)

        # Clear the table before adding the items list
        self.packaging_table.delete(*self.packaging_table.get_children())

        # Add the items to the table
        for type, rows in pl.items():
            first = True
            for size, num in rows.items():
                if first:
                    self.packaging_table.insert("", "end", text=type, values=(size, num))
                    first = False
                else:
                    self.packaging_table.insert("", "end", values=(size, num))

        self.packaging_table.insert("", "end", text="Vekt", values=("", f"{weight} kg"))

        # Reset the height of the table to fit all rows
        self.packaging_table.configure(height=len(self.packaging_table.get_children()))

