import tkinter
import tkinter.messagebox

PAD_X = 50


CANVAS_BASELINE = 300

GLASS_WEIGHT_MULTIPLYER = 0.5
WALLMOUNT_WEIGHT_MULTIPLYER = 0.2
POST_WEIGHT_MULTIPLYER = 0.3

WALLMOUNT_WIDTH = 10
POST_LAST_WIDTH = 15
POST_WIDTH = 15

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


class Glass:
    def __init__(self, canvas, xpos, width, height):
        self.id = canvas.create_rectangle(xpos, CANVAS_BASELINE - height, xpos + width, CANVAS_BASELINE, fill="blue")
        self.xpos = xpos
        self.width = width
        self.height = height
        self.weight = self.width * self.height  * GLASS_WEIGHT_MULTIPLYER
        self.label = canvas.create_text(xpos + (width / 2), CANVAS_BASELINE - height - 30, text=width)

class Wallmount:
    def __init__(self, canvas, xpos, height):
        self.width = WALLMOUNT_WIDTH
        self.id = canvas.create_rectangle(xpos, CANVAS_BASELINE - height, xpos + self.width, CANVAS_BASELINE, fill="gray")
        self.xpos = xpos
        self.height = height
        self.weight = self.width * self.height  * WALLMOUNT_WEIGHT_MULTIPLYER

class Post:
    def __init__(self, canvas, xpos, height, is_last=0):
        if is_last:
            self.width = POST_LAST_WIDTH
        else:
            self.width = POST_WIDTH
        self.id = canvas.create_rectangle(xpos, CANVAS_BASELINE - height, xpos + self.width, CANVAS_BASELINE, fill="black")
        self.xpos = xpos
        self.height = height
        self.weight = self.width * self.height  * POST_WEIGHT_MULTIPLYER

class LengthBar:
    def __init__(self, canvas):
        self.canvas = canvas
        self.left = self.canvas.create_rectangle(1, LENGTH_BAR_SIDES_TOP, LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_BOTTOM, fill="black")
        self.right = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.bar = self.canvas.create_rectangle(0, 0, 0, 0, fill="black")
        self.label = self.canvas.create_text(0, 0, text="")

    def update(self, current_width):
        self.canvas.delete(self.bar)
        self.canvas.delete(self.right)
        self.canvas.delete(self.label)
        self.bar = self.canvas.create_rectangle(0, LENGTH_BAR_TOP, current_width, LENGTH_BAR_BOTTOM, fill="black")
        self.right = self.canvas.create_rectangle(current_width - LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_TOP, current_width, LENGTH_BAR_SIDES_BOTTOM, fill="black")
        self.label = self.canvas.create_text(current_width / 2, LENGT_BAR_LABEL_TOP, text=current_width)


class Main:
    def __init__(self, master):
        self.master = master
        self.current_width = 0
        self.current_weight = 0
        self.canvas_items = []

        # ------------ Top Frame ---------------

        self.top_frame = tkinter.Frame(self.master, bg="white")
        self.top_frame.pack(side="top", fill="x")

        self.undo_button = tkinter.Button(self.top_frame, text="Angre", command=self.undo)
        self.undo_button.pack(side="left", padx=PAD_X)

        self.top_container = tkinter.Frame(self.top_frame)
        self.top_container.pack(side="top", pady=10)

        self.total_length_label = tkinter.Label(self.top_container, text="Total lengde:")
        self.total_length_entry = tkinter.Entry(self.top_container)
        self.total_length_label.pack(side="left")
        self.total_length_entry.pack(side="left")
        self.total_length_entry.insert(0, 0)

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

        self.add_wallmount_button = tkinter.Button(self.bottom_container, text="Veggfeste", command=self.add_wallmount)
        self.wallmount_height_entry = tkinter.Entry(self.bottom_container)
        self.add_wallmount_button.pack(side="left", padx=10)
        self.wallmount_height_entry.pack(side="left", padx=10)
        self.wallmount_height_entry.insert(0, 65)
       
        self.add_post_button = tkinter.Button(self.bottom_container, text="Stolpe", command=self.add_post)
        self.post_height_entry = tkinter.Entry(self.bottom_container)
        self.add_post_button.pack(side="left", padx=10)
        self.post_height_entry.pack(side="left", padx=10)
        self.post_height_entry.insert(0, 65)
       
        self.add_glass_button = tkinter.Button(self.bottom_container, text="Glass", command=self.add_glass)
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


    def add_wallmount(self):
        if not to_float(self.wallmount_height_entry.get()) or \
           not to_float(self.total_length_entry.get()):
            return
        if self.current_width + WALLMOUNT_WIDTH > float(self.total_length_entry.get()):
            if not self.cut_glass(WALLMOUNT_WIDTH):
                return
        wallmount = Wallmount(self.canvas, self.current_width, float(self.wallmount_height_entry.get()))
        self.canvas_items.append(wallmount)
        self.current_width += wallmount.width
        self.length_bar.update(self.current_width)
        self.update_current_weight(wallmount.weight)

    def add_glass(self):
        if not to_float(self.glass_height_entry.get()) or \
           not to_float(self.glass_width_entry.get())  or \
           not to_float(self.total_length_entry.get()):
            return

        glass_width = float(self.glass_width_entry.get())
        if glass_width + self.current_width > float(self.total_length_entry.get()):
            glass_width = float(self.total_length_entry.get()) - self.current_width
        
        glass = Glass(self.canvas, self.current_width, glass_width, float(self.glass_height_entry.get()))
        self.canvas_items.append(glass)
        self.current_width += glass_width
        self.length_bar.update(self.current_width)
        self.update_current_weight(glass.weight)

    def add_post(self):
        if not to_float(self.post_height_entry.get()) or \
           not to_float(self.total_length_entry.get()):
            return
        
        if self.current_width + POST_WIDTH > float(self.total_length_entry.get()):
            if not self.cut_glass(POST_WIDTH):
                return
        post = Post(self.canvas, self.current_width, float(self.post_height_entry.get()))
        self.canvas_items.append(post)
        self.current_width += post.width
        self.length_bar.update(self.current_width)
        self.update_current_weight(post.weight)

    def undo(self):
        item = self.canvas_items.pop()
        self.canvas.delete(item.id)
        if isinstance(item, Glass):
            self.canvas.delete(item.label)
        self.current_width -= item.width
        self.length_bar.update(self.current_width)
        self.update_current_weight(-item.weight)

    def update_current_weight(self, weight):
        self.current_weight += weight
        self.current_weight_label.configure(text="Vekt: "+str(self.current_weight)+" kg")

    def cut_glass(self, width):
        try:
            glass = self.canvas_items.pop()
        except:
            return False
        if not isinstance(glass, Glass):
            tkinter.messagebox.showinfo("Warning", "Kan ikke legge til stolpe/veggfeste fordi forrige element er ikke et glass!")
            return False
        self.canvas.delete(glass.id)
        self.canvas.delete(glass.label)
        self.current_width -= glass.width
        self.current_weight -= glass.weight
        new_width = float(self.total_length_entry.get()) - width - self.current_width
        new_glass = Glass(self.canvas, self.current_width, new_width, glass.height)
        self.canvas_items.append(new_glass)
        self.current_width += new_glass.width
        self.length_bar.update(self.current_width)
        self.update_current_weight(new_glass.weight)
        return True



if __name__ == "__main__":
    root = tkinter.Tk(screenName="screenname", baseName="basename", className="Avskjerming", useTk=1)
    root.geometry("1000x600")
    root.configure(bg="white")
    main = Main(root)
    root.mainloop()