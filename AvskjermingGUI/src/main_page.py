import tkinter
from tkinter import messagebox
from decimal import Decimal, InvalidOperation
from canvas import Canvas
from items import Wallmount, Post, Glass, GlassPolygon
from config import DROPDOWN_WIDTH


class MainPage(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.config(bg="white")

        total_width_frame = tkinter.Frame(self, bg="white")
        top_frame = tkinter.Frame(self, bg="white")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(4, weight=1)
        self.canvas = Canvas(self)
        bottom_frame = tkinter.Frame(self, bg="white")


        total_width_frame.pack(side="top", fill="x")
        total_width_container = tkinter.Frame(total_width_frame, bg="white")
        total_width_container.pack(side="top")

        total_width_label = tkinter.Label(total_width_container, text="Total lengde: ", bg="white")
        total_width_label.pack(side="left", pady=20)

        self.total_width = tkinter.StringVar()
        self.total_width_entry = tkinter.Entry(total_width_container, text=self.total_width, bg="white")
        self.total_width_entry.pack(side="left")


        top_frame.pack(side="top", fill="x")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        top_frame_left_container = tkinter.Frame(top_frame, bg="white")
        top_frame_left_container.grid(row=0, column=0, sticky="w")
        self.reset_button = tkinter.Button(top_frame_left_container, text="Reset", command=lambda: [self.canvas.clear(), self.update_weight()])
        self.reset_button.pack(side="left", padx=10)
        self.undo_button = tkinter.Button(top_frame_left_container, text="Angre", command=lambda: [self.canvas.undo(), self.update_weight()])
        self.undo_button.pack(side="left")

        self.auto_left_item_sv = tkinter.StringVar()
        self.auto_left_item_sv.set("Veggskinne")
        self.auto_left_item_drop_down = tkinter.OptionMenu(top_frame, self.auto_left_item_sv, *["Veggskinne", "Stolpe"])
        self.auto_left_item_drop_down.grid(row=0, column=1, padx=10)
        self.auto_left_item_drop_down.config(width=DROPDOWN_WIDTH)

        auto_glass_container = tkinter.Frame(top_frame, bg="white")
        auto_glass_container.grid(row=0, column=2, padx=10)
        glass_width_label = tkinter.Label(auto_glass_container, text="Global bredde: ", bg="white")
        glass_width_label.grid(row=0, column=0)
        glass_height_label = tkinter.Label(auto_glass_container, text="Global høyde: ", bg="white")
        glass_height_label.grid(row=1, column=0)
        self.auto_glass_width_sv = tkinter.StringVar()
        self.auto_glass_width_entry = tkinter.Entry(auto_glass_container, text=self.auto_glass_width_sv)
        self.auto_glass_width_entry.grid(row=0, column=1)
        self.auto_glass_width_entry.insert(0, 60)
        self.auto_glass_height_sv = tkinter.StringVar()
        self.auto_glass_height_entry = tkinter.Entry(auto_glass_container, text=self.auto_glass_height_sv)
        self.auto_glass_height_entry.grid(row=1, column=1)
        self.auto_glass_height_entry.insert(0, 60)

        self.auto_right_item_sv = tkinter.StringVar()
        self.auto_right_item_sv.set("Stolpe")
        self.auto_right_item_drop_down = tkinter.OptionMenu(top_frame, self.auto_right_item_sv, *["Veggskinne", "Stolpe"])
        self.auto_right_item_drop_down.grid(row=0, column=3, padx=10)
        self.auto_right_item_drop_down.config(width=DROPDOWN_WIDTH)

        self.total_weight_label = tkinter.Label(top_frame, text="Total vekt: 0 kg", bg="white")
        self.total_weight_label.grid(row=0, column=4, padx=20, sticky="e")


        self.canvas.pack(side="top", fill="both", expand=1)


        bottom_frame.pack(side="top", fill="x")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(5, weight=1)

        self.wallmount_button = tkinter.Button(bottom_frame, text="Veggskinne", command=lambda: self.add_item(Wallmount))
        self.wallmount_button.grid(row=0, column=1, pady=50, padx=10)
        self.post_button = tkinter.Button(bottom_frame, text="Stolpe", command=lambda: self.add_item(Post))
        self.post_button.grid(row=0, column=2, padx=10)
        self.glass_button = tkinter.Button(bottom_frame, text="Glass", command=lambda: self.add_item(Glass))
        self.glass_button.grid(row=0, column=3, padx=10)

        glass_container = tkinter.Frame(bottom_frame, bg="white")
        glass_container.grid(row=0, column=4, padx=10)
        glass_width_label = tkinter.Label(glass_container, text="Individuell bredde: ", bg="white")
        glass_width_label.grid(row=0, column=0)
        glass_height_label = tkinter.Label(glass_container, text="Individuell høyde: ", bg="white")
        glass_height_label.grid(row=1, column=0)
        self.glass_width_entry = tkinter.Entry(glass_container)
        self.glass_width_entry.grid(row=0, column=1)
        self.glass_width_entry.insert(0, 60)
        self.glass_height_entry = tkinter.Entry(glass_container)
        self.glass_height_entry.grid(row=1, column=1)
        self.glass_height_entry.insert(0, 60)

        self.polygon_button = tkinter.Button(bottom_frame, text="Skrå glass", command=lambda: self.add_item(GlassPolygon))
        self.polygon_button.grid(row=0, column=5, padx=10, sticky="e")
        self.polygon_entry = tkinter.Entry(bottom_frame)
        self.polygon_entry.insert(0, 20)
        self.polygon_entry.grid(row=0, column=6, padx=10, sticky="e")

        self.total_width.trace("w", lambda name, index, mode: self.auto_calculate())
        self.auto_left_item_sv.trace("w", lambda name, index, mode: self.auto_calculate())
        self.auto_glass_width_sv.trace("w", lambda name, index, mode: self.auto_calculate())
        self.auto_glass_height_sv.trace("w", lambda name, index, mode: self.auto_calculate())
        self.auto_right_item_sv.trace("w", lambda name, index, mode: self.auto_calculate())


    def auto_calculate(self):
        try:
            if self.total_width.get() == ""                or \
               float(self.total_width.get()) < 10          or \
               self.auto_glass_width_sv.get() == ""        or \
               float(self.auto_glass_width_sv.get()) < 10  or \
               self.auto_glass_height_sv.get() == ""         or \
               float(self.auto_glass_height_sv.get()) <= 0:
                self.canvas.clear()
                return
            if Decimal(self.total_width.get()) > 10000:
                messagebox.showinfo("Warning", "Total lengde er for stor!")
                self.canvas.clear()
                self.total_width.set(self.total_width.get()[:-1])
                return
        except SyntaxError:
            self.canvas.clear()
            self.total_width.set(self.total_width.get()[:-1])
            return
        except ValueError:
            if(self.total_width.get().find(",") != -1):
                messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            self.canvas.clear()
            self.total_width.set(self.total_width.get()[:-1])
            return

        left_item = Wallmount if self.auto_left_item_sv.get() == "Veggskinne" else Post
        right_item = Wallmount if self.auto_right_item_sv.get() == "Veggskinne" else Post
        self.canvas.auto_calculate(Decimal(self.total_width.get()),                  \
                                   left_item,                               \
                                   Decimal(self.auto_glass_width_sv.get()), \
                                   Decimal(self.auto_glass_height_sv.get()),  \
                                   right_item)
        self.update_weight()

    def add_item(self, item):
        try:
            if self.total_width.get() == ""                or \
               float(self.total_width.get()) < 10          or \
               self.glass_width_entry.get() == ""          or \
               float(self.glass_width_entry.get()) <= 0    or \
               self.glass_height_entry.get() == ""         or \
               float(self.glass_height_entry.get()) <= 0:
                return
            if Decimal(self.total_width.get()) > 10000:
                messagebox.showinfo("Warning", "Total lengde er for stor!")
                self.canvas.clear()
                self.total_width.set(self.total_width.get()[:-1])
                return
        except SyntaxError:
            self.total_width.set(self.total_width.get()[:-1])
            return
        except ValueError:
            if(self.total_width.get().find(",") != -1):
                messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            self.total_width.set(self.total_width.get()[:-1])
            return

        if item is GlassPolygon:
            try:
                if self.polygon_entry.get() == "" or \
                   float(self.polygon_entry.get()) < 0:
                    messagebox.showinfo("Warning", "Ugyldig skrå høyde!")
                    return False
            except SyntaxError:
                    messagebox.showinfo("Warning", "Ugyldig skrå høyde!")
                    return False
            except ValueError:
                if(self.total_width.get().find(",") != -1):
                    messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
                else:
                    messagebox.showinfo("Warning", "Ugyldig skrå høyde!")
                return False
            self.canvas.add_glass(Decimal(self.glass_width_entry.get()), Decimal(self.glass_height_entry.get()), Decimal(self.polygon_entry.get()))
        if item is Wallmount:
            self.canvas.add_wallmount(Decimal(self.glass_height_entry.get()))
        elif item is Post:
            self.canvas.add_post(Decimal(self.glass_height_entry.get()))
        else:
            self.canvas.add_glass(Decimal(self.glass_width_entry.get()), Decimal(self.glass_height_entry.get()))

        self.update_weight()

    def get_current_widt(self):
        try:
            if self.glass_width_entry.get() == "" or \
               float(self.glass_width_entry.get()) <= 0:
                messagebox.showinfo("Warning", "Ugyldig glass bredde!")
                return False
        except SyntaxError:
                messagebox.showinfo("Warning", "Ugyldig glass bredde!")
                return False
        except ValueError:
            if(self.total_width.get().find(",") != -1):
                messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            else:
                messagebox.showinfo("Warning", "Ugyldig glass bredde!")
            return False
        return Decimal(self.glass_width_entry.get())

    def get_total_length(self):
        try:
            if self.total_width.get() == "" or \
               float(self.total_width.get()) <= 0:
                messagebox.showinfo("Warning", "Ugyldig total lengde!")
                return False
        except SyntaxError:
                messagebox.showinfo("Warning", "Ugyldig total lengde!")
                return False
        except ValueError:
            if(self.total_width.get().find(",") != -1):
                messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            else:
                messagebox.showinfo("Warning", "Ugyldig total lengde!")
            return False
        return Decimal(self.total_width.get())

    def update_weight(self):
        weight = self.canvas.get_weight()
        weight_kg = (round(weight[0] / 1000), round(weight[1] / 1000))

        self.total_weight_label.configure(text="Vekt: " + str(weight_kg[0]) + " kg\n+ innpakning: " + str(weight_kg[1]) + " kg\nTotal: " + str(weight_kg[0] + weight_kg[1]) + " kg")
