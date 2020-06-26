import tkinter
from config import TITLE
from main_page import MainPage

class Main(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1500x1000")
        self.config(bg="white")
        self.wm_title(TITLE)

        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frame in [MainPage]:
            f = Frame(container, self)
            self.frames[Frame] = f
            f.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, page):
        self.frames[page].tkraise()


if __name__ == "__main__":
    app = Main()
    app.mainloop()
