import tkinter, collections
import tkinter.messagebox

PAD_X = 50


CANVAS_BASELINE = 300

GLASS_WEIGHT_MULTIPLYER = 0.5
WALLMOUNT_WEIGHT_MULTIPLYER = 0.2
POST_WEIGHT_MULTIPLYER = 0.3

WALLMOUNT_WIDTH = 10
POST_LAST_WIDTH = 15
POST_WIDTH = 15
POST_BASE_WIDTH = 4
POST_BASE_HEIGHT = 3

GLASS_BASELINE = CANVAS_BASELINE - POST_BASE_HEIGHT

LENGTH_BAR_SIDES_TOP = 320
LENGTH_BAR_SIDES_HEIGHT = 10
LENGTH_BAR_THICKNESS = 1
LENGTH_BAR_SIDES_BOTTOM = LENGTH_BAR_SIDES_TOP + LENGTH_BAR_SIDES_HEIGHT
LENGTH_BAR_TOP = LENGTH_BAR_SIDES_TOP + (LENGTH_BAR_SIDES_HEIGHT / 2)
LENGTH_BAR_BOTTOM = LENGTH_BAR_TOP + LENGTH_BAR_THICKNESS
LENGT_BAR_LABEL_TOP = LENGTH_BAR_SIDES_TOP + LENGTH_BAR_SIDES_HEIGHT + 5


def to_float(num):
    try:
        num = float(num)
    except ValueError:
        tkinter.messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
        return False
    return True

class Item:
    WALLMOUNT = 0
    POST = 1
    GLASS = 2



class Wallmount:
    def __init__(self, canvas, xpos, height, is_last, is_first):
        self.canvas = canvas
        self.is_first = is_first
        self.is_last = is_last
        self.width = WALLMOUNT_WIDTH
        self.id = canvas.create_rectangle(xpos, CANVAS_BASELINE - height, xpos + self.width, CANVAS_BASELINE, fill="gray")
        self.xpos = xpos
        self.height = height
        self.weight = self.width * self.height  * WALLMOUNT_WEIGHT_MULTIPLYER

    def delete(self):
        self.canvas.delete(self.id)


class Post:
    def __init__(self, canvas, xpos, height, is_last, is_first):
        self.canvas = canvas
        self.is_first = is_first
        self.is_last = is_last
        self._width = POST_WIDTH
        if is_first:
            self.xpos = xpos + POST_BASE_WIDTH
        else:
            self.xpos = xpos
        self.id = canvas.create_rectangle(self.xpos, CANVAS_BASELINE - height, self.xpos + self._width, CANVAS_BASELINE, fill="black")
        self.height = height
        self.weight = self._width * self.height  * POST_WEIGHT_MULTIPLYER
        self.base_width = self._width + (POST_BASE_WIDTH * 2)

        self.base = canvas.create_rectangle(self.xpos - POST_BASE_WIDTH,                    \
                                            CANVAS_BASELINE - POST_BASE_HEIGHT,       \
                                            self.xpos + POST_BASE_WIDTH + POST_WIDTH, \
                                            CANVAS_BASELINE, fill="black")

    @property
    def width(self):
        if self.is_last or self.is_first:
            return self._width + POST_BASE_WIDTH
        return self._width

    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.base)


class Glass:
    def __init__(self, canvas, xpos, width, height, is_last, is_first):
        self.canvas = canvas
        self.is_first = is_first
        self.is_last = is_last
        self.id = canvas.create_rectangle(xpos, GLASS_BASELINE - height, xpos + width, GLASS_BASELINE, fill="blue")
        self.xpos = xpos
        self.width = width
        self.height = height
        self.weight = self.width * self.height  * GLASS_WEIGHT_MULTIPLYER
        self.label = canvas.create_text(xpos + (width / 2), GLASS_BASELINE - height - 30, text=width)

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
    

    def update(self, current_width):
        self.canvas.delete(self.bar)
        self.canvas.delete(self.left)
        self.canvas.delete(self.right)
        self.canvas.delete(self.label)
        if current_width > 0:
            self.left = self.canvas.create_rectangle(1, LENGTH_BAR_SIDES_TOP, LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_BOTTOM, fill="black")
            self.bar = self.canvas.create_rectangle(0, LENGTH_BAR_TOP, current_width, LENGTH_BAR_BOTTOM, fill="black")
            self.right = self.canvas.create_rectangle(current_width - LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_TOP, current_width, LENGTH_BAR_SIDES_BOTTOM, fill="black")
            self.label = self.canvas.create_text(current_width / 2, LENGT_BAR_LABEL_TOP, text=current_width)


class Main:
    def __init__(self, master):
        self.master = master
        self.current_width = 0
        self.current_weight = 0
        self.canvas_items = []
        self.total_width = 0

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
        wallmount = Wallmount(self.canvas, self.current_width, float(self.wallmount_height_entry.get()), True, is_first)
        self.canvas_items.append(wallmount)
        return True

    def add_post(self, is_first):
        if self.current_width + POST_WIDTH > self.total_width:
            if not self.cut_glass(POST_WIDTH):
                return False
        post = Post(self.canvas, self.current_width, float(self.post_height_entry.get()), True, is_first)
        self.canvas_items.append(post)
        return True

    def add_glass(self, is_first):
        glass_width = float(self.glass_width_entry.get())
        if glass_width + self.current_width > self.total_width:
            glass_width = self.total_width - self.current_width
        glass = Glass(self.canvas, self.current_width, glass_width, float(self.glass_height_entry.get()), True, is_first)
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
        new_width = self.total_width - width - self.current_width
        new_glass = Glass(self.canvas, self.current_width, new_width, glass.height, False, False)
        self.canvas_items.append(new_glass)
        self.update()
        return True

    def assert_user_input(self):
        try:
            if float(self.glass_height_entry.get()) <= 0:
                tkinter.messagebox.showinfo("Warning", "Glass høyden må være større enn 0!")
            elif float(self.glass_width_entry.get()) <= 0:
                tkinter.messagebox.showinfo("Warning", "Glass bredden må være større enn 0!")
            elif float(self.wallmount_height_entry.get()) <= 0:
                tkinter.messagebox.showinfo("Warning", "Veggfeste høyden må være større enn 0!")
            elif float(self.post_height_entry.get()) <= 0:
                tkinter.messagebox.showinfo("Warning", "Stolpe høyden må være større enn 0!")
            elif float(self.total_width_entry.get()) <= 0:
                tkinter.messagebox.showinfo("Warning", "Den totale lengden må være større enn 0!")
            else:
                self.total_width = float(self.total_width_entry.get())
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
        self.current_width = 0
        self.current_weight = 0
        for item in self.canvas_items:
            self.current_width += item.width
            self.current_weight += item.weight
        self.current_weight_label.configure(text="Vekt: " + str(self.current_weight) + " kg")
        self.length_bar.update(self.current_width)


if __name__ == "__main__":
    root = tkinter.Tk(screenName="screenname", baseName="basename", className="Avskjerming", useTk=1)
    root.geometry("1000x600")
    root.configure(bg="white")
    main = Main(root)
    root.mainloop()