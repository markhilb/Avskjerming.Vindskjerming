import tkinter
import tkinter.messagebox
# https://www.geeksforgeeks.org/python-gui-tkinter/

GLASS_TOP = 220
GLASS_BOTTOM = 300
GLASS_TEXT_TOP = 190


class Main():
    def __init__(self, master):
        self.currentWidth = 0
        self.veggfesteWidth = 10
        self.glassWidth = 60
        self.stolpeWidth = 15
        self.canvasItems = []


        # ------------ Top Frame ---------------

        self.topFrame = tkinter.Frame(master, bg="white")
        self.topFrame.pack(side="top", fill="x")

        self.regretButton = tkinter.Button(self.topFrame, text="Angre", command=self.regret)
        self.regretButton.pack(side="left", padx=50)

        self.topContainer = tkinter.Frame(self.topFrame)
        self.topContainer.pack(side="top", pady=10)

        self.totalLengthLabel = tkinter.Label(self.topContainer, text="Total lengde:")
        self.totalLengthLabel.pack(side="left")

        self.totalLengthEntry = tkinter.Entry(self.topContainer)
        self.totalLengthEntry.pack(side="left")
        self.totalLengthEntry.insert(0, 0)


        # ------------ Middle Frame ---------------


        self.canvas = tkinter.Canvas(master, bg="lightgray")
        self.canvas.pack(side="top", fill="both", expand=1, padx=50)

        self.lengthBarLeft = self.canvas.create_rectangle(0, 320, 2, 340, fill="black")
        self.lengthBarRight = self.canvas.create_rectangle(self.currentWidth - 1, 320, self.currentWidth, 340, fill="black")
        self.lengthBar = self.canvas.create_rectangle(0, 329, self.currentWidth, 330, fill="black")
        self.lengthBarLabel = self.canvas.create_text(0, 350, text="")


        # ------------ Bottom Frame ---------------


        self.bottomFrame = tkinter.Frame(master, bg="white")
        self.bottomFrame.pack(side="bottom", fill="both", expand=0)

        self.bottomContainer = tkinter.Frame(self.bottomFrame, bg="white")
        self.bottomContainer.pack(pady=50)

        self.veggfeste = tkinter.Button(self.bottomContainer, text="Veggfeste", command=self.addVeggfeste)
        self.glass = tkinter.Button(self.bottomContainer, text="Glass", command=self.addGlass)
        self.glassEntry = tkinter.Entry(self.bottomContainer)
        self.stolpe = tkinter.Button(self.bottomContainer, text="Stolpe", command=self.addStolpe)
        self.veggfeste.pack(side="left", padx=10)
        self.glass.pack(side="left", padx=10)
        self.glassEntry.pack(side="left")
        self.glassEntry.insert(0, self.glassWidth)
        self.stolpe.pack(side="left", padx=10)


    def checkTotalLength(self):
        if self.totalLengthEntry.get() is '0':
            tkinter.messagebox.showinfo("Warning", "Legg til en total lengde først!")
            return False
        try:
            float(self.totalLengthEntry.get())
        except ValueError:
            tkinter.messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            return False
        return True

    def addVeggfeste(self):
        if not self.checkTotalLength():
            return
        tmp = self.canvas.create_rectangle(self.currentWidth, 200, self.currentWidth + self.veggfesteWidth, 300, fill="gray")
        self.currentWidth += self.veggfesteWidth
        self.canvasItems.append((tmp, self.veggfesteWidth, -1))
        self.updateLengthBar()

    def addGlass(self):
        if not self.checkTotalLength():
            return
        try:
            self.glassWidth = float(self.glassEntry.get())
        except ValueError:
            tkinter.messagebox.showinfo("Warning", "Bruk punktum ikke komma!")
            return
        self.checkIfTooLong()
        tmp = self.canvas.create_rectangle(self.currentWidth, GLASS_TOP, self.currentWidth + self.glassWidth, GLASS_BOTTOM, fill="blue")
        label = self.canvas.create_text(self.currentWidth + (self.glassWidth / 2), GLASS_TEXT_TOP, text=self.glassWidth)
        self.currentWidth += self.glassWidth
        self.canvasItems.append((tmp, self.glassWidth, label))
        self.updateLengthBar()

    def addStolpe(self):
        if not self.checkTotalLength():
            return
        if not self.cutLastGlass(self.stolpeWidth):
            tmp = self.canvas.create_rectangle(self.currentWidth, 200, self.currentWidth + self.stolpeWidth, 300, fill="black") 
            self.currentWidth += self.stolpeWidth
            self.canvasItems.append((tmp, self.stolpeWidth, -1))
        else:
            #
            # Todo: if currentWidth + stopleWidth > totalLength
            #           Cut glass
            #
            tmp = self.canvas.create_rectangle(float(self.totalLengthEntry.get()), 200, float(self.totalLengthEntry.get()) - self.stolpeWidth, 300, fill="black") 
            self.canvasItems.append((tmp, self.stolpeWidth, -1))
        self.updateLengthBar()

    def regret(self):
        item = self.canvasItems.pop()
        if item[2] > 0:
            self.canvas.delete(item[2])
        self.canvas.delete(item[0])
        self.currentWidth -= item[1]
        self.updateLengthBar()

    def updateLengthBar(self):
        self.canvas.delete(self.lengthBar)
        self.canvas.delete(self.lengthBarRight)
        self.canvas.delete(self.lengthBarLabel)
        self.lengthBarRight = self.canvas.create_rectangle(self.currentWidth - 1, 320, self.currentWidth, 340, fill="black")
        self.lengthBar = self.canvas.create_rectangle(0, 329, self.currentWidth, 331, fill="black")
        self.lengthBarLabel = self.canvas.create_text(self.currentWidth / 2, 350, text=self.currentWidth)

    def checkIfTooLong(self):
        if self.currentWidth + self.glassWidth > float(self.totalLengthEntry.get()):
            self.glassWidth = float(self.totalLengthEntry.get()) - self.currentWidth

    def cutLastGlass(self, len):
        if self.currentWidth + len > float(self.totalLengthEntry.get()):
            glass = self.canvasItems.pop()
            self.canvas.delete(glass[0])
            self.canvas.delete(glass[2])
            newGlassWidth = (float(self.totalLengthEntry.get()) - len) - (self.currentWidth - glass[1])
            newGlass = self.canvas.create_rectangle(self.currentWidth - glass[1], GLASS_TOP, float(self.totalLengthEntry.get()) - len, GLASS_BOTTOM, fill="blue")
            newLabel = self.canvas.create_text((self.currentWidth - glass[1] + (newGlassWidth / 2)), GLASS_TEXT_TOP, text=newGlassWidth)
            self.canvasItems.append((newGlass, newGlassWidth, newLabel))
            return True
        else:
            return False


root = tkinter.Tk(screenName="screenname", baseName="basename", className="classname", useTk=1)
root.geometry("1000x600")
root.configure(bg="white")

main = Main(root)

root.mainloop()