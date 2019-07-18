import tkinter
from canvas_items import Item


class BottomFrame:
    def __init__(self, master, button_func):
        self.main_frame = tkinter.Frame(master, bg="white")
        self.main_frame.pack(side="bottom", fill="both", expand=0)

        self.bottom_container = tkinter.Frame(self.main_frame, bg="white")
        self.bottom_container.pack(pady=50)

        self.add_wallmount_button = tkinter.Button(self.bottom_container, text="Veggfeste", command= lambda: button_func(Item.WALLMOUNT))
        self.wallmount_height_entry = tkinter.Entry(self.bottom_container)
        self.add_wallmount_button.pack(side="left", padx=10)
        self.wallmount_height_entry.pack(side="left", padx=10)
        self.wallmount_height_entry.insert(0, 65)
       
        self.add_post_button = tkinter.Button(self.bottom_container, text="Stolpe", command= lambda: button_func(Item.POST))
        self.post_height_entry = tkinter.Entry(self.bottom_container)
        self.add_post_button.pack(side="left", padx=10)
        self.post_height_entry.pack(side="left", padx=10)
        self.post_height_entry.insert(0, 65)
       
        self.add_glass_button = tkinter.Button(self.bottom_container, text="Glass", command= lambda: button_func(Item.GLASS))
        self.add_glass_button.pack(side="left", padx=10)

        self.glass_entries_container = tkinter.Frame(self.bottom_container, bg="white")
        self.glass_entries_container.pack(side="left")

        self.glass_width_entry_container = tkinter.Frame(self.glass_entries_container, bg="white")
        self.glass_height_entry_container = tkinter.Frame(self.glass_entries_container, bg="white")
        self.glass_width_entry_container.pack(side="top")
        self.glass_height_entry_container.pack(side="top")
       
        self.glass_width_entry = tkinter.Entry(self.glass_width_entry_container)
        self.glass_width_entry_label = tkinter.Label(self.glass_width_entry_container, text="Bredde", bg="white")
        self.glass_height_entry = tkinter.Entry(self.glass_height_entry_container)
        self.glass_height_entry_label = tkinter.Label(self.glass_height_entry_container, text="Høyde", bg="white")
        
        self.glass_width_entry.pack(side="left")
        self.glass_width_entry_label.pack(side="left")
        self.glass_height_entry.pack(side="left")
        self.glass_height_entry_label.pack(side="left")
        self.glass_width_entry.insert(0, 60)
        self.glass_height_entry.insert(0, 60)