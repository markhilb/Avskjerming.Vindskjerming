import tkinter, collections
import tkinter.messagebox
from decimal import Decimal


#
# @Todo: Add topbar "File Settings etc..."
#       Add functionality for saving canvas as image (for printing)
#       Possibly add scaling under "File" section...
#


PAD_X = 50

CANVAS_BASELINE = Decimal('300')

GLASS_WEIGHT_MULTIPLYER = Decimal('0.5')
WALLMOUNT_WEIGHT_MULTIPLYER = Decimal('0.2')
POST_WEIGHT_MULTIPLYER = Decimal('0.3')

WALLMOUNT_WIDTH = Decimal('0.5')
POST_WIDTH = Decimal('1.3')
POST_BASE_WIDTH = Decimal('2')
POST_BASE_HEIGHT = Decimal('2')
POST_LAST_WIDTH = POST_WIDTH + POST_BASE_WIDTH

GLASS_BASELINE = CANVAS_BASELINE - POST_BASE_HEIGHT

LENGTH_BAR_SIDES_TOP = Decimal('320')
LENGTH_BAR_SIDES_HEIGHT = Decimal('10')
LENGTH_BAR_THICKNESS = Decimal('1')
LENGTH_BAR_SIDES_BOTTOM = LENGTH_BAR_SIDES_TOP + LENGTH_BAR_SIDES_HEIGHT
LENGTH_BAR_TOP = LENGTH_BAR_SIDES_TOP + (LENGTH_BAR_SIDES_HEIGHT / 2)
LENGTH_BAR_BOTTOM = LENGTH_BAR_TOP + LENGTH_BAR_THICKNESS
LENGT_BAR_LABEL_TOP = LENGTH_BAR_SIDES_TOP + LENGTH_BAR_SIDES_HEIGHT + 5


class Item:
    WALLMOUNT = 0
    POST = 1
    GLASS = 2



class Wallmount:
    def __init__(self, canvas, xpos, height, canvas_xpos, scale, is_last, is_first):
        self.canvas = canvas
        self.scale = scale
        self.is_last = is_last
        self.is_first = is_first
        self.width = WALLMOUNT_WIDTH
        self.xpos = xpos
        self.height = height
        self.canvas_xpos = canvas_xpos
        self.canvas_width = self.width * self.scale
        self.weight = self.width * self.height  * WALLMOUNT_WEIGHT_MULTIPLYER
        self.id = canvas.create_rectangle(self.canvas_xpos, CANVAS_BASELINE - self.height, self.canvas_xpos + self.canvas_width, CANVAS_BASELINE, fill="gray")

    def delete(self):
        self.canvas.delete(self.id)


class Post:
    def __init__(self, canvas, xpos, height, canvas_xpos, scale, is_last, is_first):
        self.canvas = canvas
        self.scale = scale
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
        self._canvas_width = self.width * self.scale
        self.weight = self._width * self.height  * POST_WEIGHT_MULTIPLYER
        self.id = canvas.create_rectangle(self.canvas_xpos, CANVAS_BASELINE - self.height, self.canvas_xpos + self._canvas_width, CANVAS_BASELINE, fill="black")
        self.canvas_base_width = (POST_BASE_WIDTH * self.scale)
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
    def __init__(self, canvas, xpos, width, height, canvas_xpos, scale, is_last, is_first):
        self.canvas = canvas
        self.scale = scale
        self.is_last = is_last
        self.is_first = is_first
        self.xpos = xpos
        self.width = width
        self.height = height
        self.canvas_xpos = canvas_xpos
        self.canvas_width = self.width * self.scale
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


class Main:
    def __init__(self, master):
        self.master = master
        self.current_width = Decimal('0')
        self.current_canvas_width = Decimal('0')
        self.current_weight = Decimal('0')
        self.canvas_items = []
        self.total_width = Decimal('0')

        self.WALLMOUNT_SCALE = Decimal('6')
        self.POST_SCALE = Decimal('2')
        self.GLASS_SCALE = Decimal('1')

        # ------------ Toolbar -----------------

        self.toolbar = tkinter.Menu(self.master)
        self.master.config(menu=self.toolbar)

        self.toolbar_file = tkinter.Menu(self.toolbar)
        self.toolbar.add_cascade(label="Fil", menu=self.toolbar_file)
        self.toolbar_file.add_command(label="Lagre bilde")

        self.toolbar_scale = tkinter.Menu(self.toolbar)
        self.toolbar.add_cascade(label="Skaler", menu=self.toolbar_scale)
        self.toolbar_scale_wallmount = tkinter.Menu(self.toolbar_scale)
        self.toolbar_scale_post = tkinter.Menu(self.toolbar_scale)
        self.toolbar_scale_glass = tkinter.Menu(self.toolbar_scale)
        self.toolbar_scale.add_cascade(label="Skaler veggfeste", menu=self.toolbar_scale_wallmount)
        self.toolbar_scale.add_cascade(label="Skaler stolpe", menu=self.toolbar_scale_post)
        self.toolbar_scale.add_cascade(label="Skaler glass", menu=self.toolbar_scale_glass)

        for i in range(0, 100, 5):
            self.toolbar_scale_wallmount.add_command(label=str(i/10), command=lambda: self.set_scale(Item.WALLMOUNT, Decimal(str(i)) / 10))
            self.toolbar_scale_post.add_command(label=str(i/10), command=lambda: self.set_scale(Item.POST, Decimal(str(i)) / 10))
            self.toolbar_scale_glass.add_command(label=str(i/10), command=lambda: self.set_scale(Item.GLASS, Decimal(str(i)) / 10))

        # ------------ Top Frame ---------------

        self.top_frame = tkinter.Frame(self.master, bg="white")
        self.top_frame.pack(side="top", fill="x")

        self.undo_button = tkinter.Button(self.top_frame, text="Angre", command=self.undo)
        self.undo_button.pack(side="left", padx=PAD_X)

        self.top_container = tkinter.Frame(self.top_frame)
        self.top_container.pack(side="top", pady=10)

        self.total_width_label = tkinter.Label(self.top_container, text="Total lengde:")
        self.total_width_entry = tkinter.Entry(self.top_container)
        self.total_width_label.pack(side="left")
        self.total_width_entry.pack(side="left")
        self.total_width_entry.insert(0, self.total_width)

        self.current_weight_label = tkinter.Label(self.top_frame, text ="Vekt: 0 kg")
        self.current_weight_label.pack(side="right", padx=PAD_X, pady=20)


        # ------------ Middle Frame ---------------

        self.canvas = tkinter.Canvas(self.master, bg="lightgray")
        self.canvas.pack(side="top", fill="both", expand=1, padx=PAD_X)

        self.length_bar = LengthBar(self.canvas)

        # ------------ Bottom Frame ---------------

        self.bottom_frame = tkinter.Frame(master, bg="white")
        self.bottom_frame.pack(side="bottom", fill="both", expand=0)

        self.bottom_container = tkinter.Frame(self.bottom_frame, bg="white")
        self.bottom_container.pack(pady=50)

        self.add_wallmount_button = tkinter.Button(self.bottom_container, text="Veggfeste", command= lambda: self.button_pressed(Item.WALLMOUNT))
        self.wallmount_height_entry = tkinter.Entry(self.bottom_container)
        self.add_wallmount_button.pack(side="left", padx=10)
        self.wallmount_height_entry.pack(side="left", padx=10)
        self.wallmount_height_entry.insert(0, 65)
       
        self.add_post_button = tkinter.Button(self.bottom_container, text="Stolpe", command= lambda: self.button_pressed(Item.POST))
        self.post_height_entry = tkinter.Entry(self.bottom_container)
        self.add_post_button.pack(side="left", padx=10)
        self.post_height_entry.pack(side="left", padx=10)
        self.post_height_entry.insert(0, 65)
       
        self.add_glass_button = tkinter.Button(self.bottom_container, text="Glass", command= lambda: self.button_pressed(Item.GLASS))
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


    def button_pressed(self, item):
        if self.assert_user_input():
            if len(self.canvas_items) is 0:
                previous_last_item = collections.namedtuple('dummy_object', 'is_last')
                is_first = True 
            else:
                previous_last_item = self.canvas_items[len(self.canvas_items) - 1]
                is_first = False 
            previous_last_item.is_last = False
            self.update()
            if item is Item.WALLMOUNT:
                if not self.add_wallmount(is_first):
                    previous_last_item.is_last = True
            elif item is Item.POST:
                if not self.add_post(is_first):
                    previous_last_item.is_last = True
            elif item is Item.GLASS:
                if not self.add_glass(is_first):
                    previous_last_item.is_last = True
            self.update()

    def add_wallmount(self, is_first):
        if self.current_width + WALLMOUNT_WIDTH > self.total_width:
            if not self.cut_glass(WALLMOUNT_WIDTH):
                return False
        wallmount = Wallmount(self.canvas, self.current_width, Decimal(self.wallmount_height_entry.get()), self.current_canvas_width, self.WALLMOUNT_SCALE, True, is_first)
        self.canvas_items.append(wallmount)
        return True

    def add_post(self, is_first):
        if self.current_width + POST_WIDTH > self.total_width:
            if not self.cut_glass(POST_WIDTH + POST_BASE_WIDTH):
                return False
        post = Post(self.canvas, self.current_width, Decimal(self.post_height_entry.get()), self.current_canvas_width, self.POST_SCALE, True, is_first)
        self.canvas_items.append(post)
        return True

    def add_glass(self, is_first):
        glass_width = Decimal(self.glass_width_entry.get())
        if glass_width + self.current_width > self.total_width:
            glass_width = self.total_width - self.current_width
        glass = Glass(self.canvas, self.current_width, glass_width, Decimal(self.glass_height_entry.get()), self.current_canvas_width, self.GLASS_SCALE, True, is_first)
        self.canvas_items.append(glass)
        return True


    def cut_glass(self, width):
        glass = self.canvas_items.pop()
        try:
            pass
        except:
            return False
        if not isinstance(glass, Glass):
            tkinter.messagebox.showinfo("Warning", "Kan ikke legge til stolpe/veggfeste fordi forrige element er ikke et glass!")
            return False
        self.canvas.delete(glass.id)
        self.canvas.delete(glass.label)
        self.current_width -= glass.width
        self.current_weight -= glass.weight
        self.current_canvas_width -= glass.canvas_width
        new_width = self.total_width - width - self.current_width
        new_glass = Glass(self.canvas, self.current_width, new_width, glass.height, self.current_canvas_width, self.GLASS_SCALE, False, False)
        self.canvas_items.append(new_glass)
        self.update()
        return True

    def assert_user_input(self):
        try:
            glass_height = self.glass_height_entry.get()
            if glass_height is "" or float(glass_height) <= 0:
                tkinter.messagebox.showinfo("Warning", "Glass høyden kan ikke være 0/tom!")
            glass_width = self.glass_width_entry.get()
            if glass_width is "" or float(glass_width) <= 0:
                tkinter.messagebox.showinfo("Warning", "Glass bredden kan ikke være 0/tom!")
            wallmount_height = self.wallmount_height_entry.get()
            if wallmount_height is "" or float(wallmount_height) <= 0:
                tkinter.messagebox.showinfo("Warning", "Veggfeste høyden kan ikke være 0/tom!")
            post_height = self.post_height_entry.get()
            if post_height is "" or float(post_height) <= 0:
                tkinter.messagebox.showinfo("Warning", "Stolpe høyden kan ikke være 0/tom!")
            total_width = self.total_width_entry.get()
            if total_width is "" or float(total_width) <= 0:
                tkinter.messagebox.showinfo("Warning", "Den totale lengden kan ikke være 0/tom!")
            else:
                self.total_width = Decimal(total_width)
                return True
        except ValueError:
                tkinter.messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
        return False

    def undo(self):
        try:
            item = self.canvas_items.pop()
        except IndexError:
            return
        item.delete()
        if len(self.canvas_items) > 0:
            self.canvas_items[len(self.canvas_items) - 1].is_last = True
        self.update()

    def update(self):
        self.current_width = Decimal('0')
        self.current_weight = Decimal('0')
        self.current_canvas_width = Decimal('0')
        for item in self.canvas_items:
            self.current_width += item.width
            self.current_weight += item.weight
            self.current_canvas_width += item.canvas_width
        self.current_weight_label.configure(text="Vekt: " + str(self.current_weight) + " kg")
        self.length_bar.update(self.current_width, self.current_canvas_width)

    def set_scale(self, item, num):
        if item is Item.WALLMOUNT:
            self.WALLMOUNT_SCALE = num
        elif item is Item.POST:
            self.POST_SCALE = num
        elif item is Item.GLASS:
            self.GLASS_SCALE = num


if __name__ == "__main__":
    root = tkinter.Tk(screenName="screenname", baseName="basename", className="Avskjerming", useTk=1)
    root.geometry("1000x600")
    root.configure(bg="white")
    main = Main(root)
    root.mainloop()