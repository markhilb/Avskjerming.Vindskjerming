import tkinter
from tkinter import messagebox
from decimal import Decimal

class EditGlassPopup(tkinter.Tk):
    def __init__(self, parent, glass_id):
        self.parent = parent
        self.glass_id = glass_id
        super().__init__()
        self.config(bg="white")
        self.wm_title("Rediger glass")
        self.label = tkinter.Label(self, text="Ny bredde:", bg="white")
        self.label.pack(side="top", pady=10)
        self.entry = tkinter.Entry(self)
        self.entry.pack(side="top", pady=10)
        self.ok = tkinter.Button(self, text="Ok", command=self.edit_glass, bg="white")
        self.cancel = tkinter.Button(self, text="Avbryt", command=self.destroy, bg="white")
        self.delete = tkinter.Button(self, text="Slett", command=self.delete, bg="white")
        self.ok.pack(side="left", padx=10, pady=10)
        self.cancel.pack(side="left", padx=10, pady=10)
        self.delete.pack(side="left", padx=10, pady=10)

    def edit_glass(self):
        try:
            if self.entry.get() is "" or \
               float(self.entry.get()) <= 0:
                return
            if Decimal(self.entry.get()) > 10000000:
                return
        except SyntaxError:
            return
        except ValueError:
            if(self.entry.get().find(",") is not -1):
                messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            return
        self.parent.edit_glass(self.glass_id, Decimal(self.entry.get()))
        self.destroy()
    
    def delete(self):
        self.parent.delete_glass(self.glass_id)
        self.destroy()