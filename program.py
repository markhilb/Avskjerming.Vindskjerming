import tkinter
import tkinter.messagebox
# https://www.geeksforgeeks.org/python-gui-tkinter/

GLASS_TOP = 220
GLASS_BOTTOM = 300
GLASS_TEXT_TOP = 190
GLASS_WEIGHT_MULTIPLYER = 0.5

VEGGFESTE_ID = -1
VEGGFESTE_TOP = 200
VEGGFESTE_BOTTOM = 300
VEGGFESTE_WEIGHT_MULTIPLYER = 0.2

STOLPE_ID = -2
STOLPE_TOP = 200
STOLPE_BOTTOM = 300
STOLPE_WEIGHT_MULTIPLYER = 0.3

TOTAL_WEIGHT_LABEL_LEFT = 500
TOTAL_WEIGHT_LABEL_TOP = 100

LENGTH_BAR_SIDES_TOP = 320
LENGTH_BAR_SIDES_HEIGHT = 10
LENGTH_BAR_THICKNESS = 2
LENGTH_BAR_SIDES_BOTTOM = LENGTH_BAR_SIDES_TOP + LENGTH_BAR_SIDES_HEIGHT
LENGTH_BAR_TOP = LENGTH_BAR_SIDES_TOP + (LENGTH_BAR_SIDES_HEIGHT / 2)
LENGTH_BAR_BOTTOM = LENGTH_BAR_TOP + LENGTH_BAR_THICKNESS
LENGT_BAR_LABEL_TOP = LENGTH_BAR_SIDES_TOP + LENGTH_BAR_SIDES_HEIGHT + 5



class Main():
    def __init__(self, master):
        self.currentWidth = 0
        self.veggfesteWidth = 10
        self.glassWidth = 60
        self.stolpeWidth = 15
        self.canvasItems = []
        self.totalWeight = 0


        # ------------ Top Frame ---------------

        self.topFrame = tkinter.Frame(master, bg="white")
        self.topFrame.pack(side="top", fill="x")

        self.regretButton = tkinter.Button(self.topFrame, text="Angre", command=self.undo)
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

        self.lengthBarLeft = self.canvas.create_rectangle(0, LENGTH_BAR_SIDES_TOP, LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_BOTTOM, fill="black")
        self.lengthBarRight = self.canvas.create_rectangle(self.currentWidth - LENGTH_BAR_THICKNESS, LENGTH_BAR_SIDES_TOP, self.currentWidth, LENGTH_BAR_SIDES_BOTTOM, fill="black")
        self.lengthBar = self.canvas.create_rectangle(0, LENGTH_BAR_TOP, self.currentWidth, LENGTH_BAR_BOTTOM, fill="black")
        self.lengthBarLabel = self.canvas.create_text(0, LENGT_BAR_LABEL_TOP, text="")

        self.totalWeightLabel = self.canvas.create_text(500, 100, text=0)


        # ------------ Bottom Frame ---------------


        self.bottomFrame = tkinter.Frame(master, bg="white")
        self.bottomFrame.pack(side="bottom", fill="both", expand=0)

        self.bottomContainer = tkinter.Frame(self.bottomFrame, bg="white")
        self.bottomContainer.pack(pady=50)

        self.veggfeste = tkinter.Button(self.bottomContainer, text="Veggfeste", command=self.addVeggfeste)
        self.stolpe = tkinter.Button(self.bottomContainer, text="Stolpe", command=self.addStolpe)
        self.glass = tkinter.Button(self.bottomContainer, text="Glass", command=self.addGlass)
        self.glassEntry = tkinter.Entry(self.bottomContainer)
        self.veggfeste.pack(side="left", padx=10)
        self.stolpe.pack(side="left", padx=10)
        self.glass.pack(side="left", padx=10)
        self.glassEntry.pack(side="left")
        self.glassEntry.insert(0, self.glassWidth)


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
        tmp = self.canvas.create_rectangle(self.currentWidth, VEGGFESTE_TOP, self.currentWidth + self.veggfesteWidth, VEGGFESTE_BOTTOM, fill="gray")
        self.currentWidth += self.veggfesteWidth
        self.canvasItems.append((tmp, self.veggfesteWidth, VEGGFESTE_ID))
        self.updateLengthBar()
        self.updateWeight(self.getVeggfesteWeight(10, 100))

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
        self.updateWeight(self.getGlassWeight(self.glassWidth, 80))

    def addStolpe(self):
        if not self.checkTotalLength():
            return
        if not self.cutLastGlass(self.stolpeWidth):
            tmp = self.canvas.create_rectangle(self.currentWidth, STOLPE_TOP, self.currentWidth + self.stolpeWidth, STOLPE_BOTTOM, fill="black") 
            self.currentWidth += self.stolpeWidth
            self.canvasItems.append((tmp, self.stolpeWidth, STOLPE_ID))
        else:
            #
            # Todo: if currentWidth + stopleWidth > totalLength
            #           Cut glass
            #
            tmp = self.canvas.create_rectangle(float(self.totalLengthEntry.get()), STOLPE_TOP, float(self.totalLengthEntry.get()) - self.stolpeWidth, STOLPE_BOTTOM, fill="black") 
            self.canvasItems.append((tmp, self.stolpeWidth, -1))
        self.updateLengthBar()
        self.updateWeight(self.getStolpeWeight(15, 100))

    def undo(self):
        item = self.canvasItems.pop()
        if item[2] > 0:
            self.canvas.delete(item[2])
            self.updateWeight(-self.getGlassWeight(item[1], 80))
        if item[2] is STOLPE_ID:
            self.updateWeight(-self.getStolpeWeight(item[1], 80))
        if item[2] is VEGGFESTE_ID:
            self.updateWeight(-self.getVeggfesteWeight(item[1], 80))

        self.canvas.delete(item[0])
        self.currentWidth -= item[1]
        self.updateLengthBar()

    def updateLengthBar(self):
        self.canvas.delete(self.lengthBar)
        self.canvas.delete(self.lengthBarRight)
        self.canvas.delete(self.lengthBarLabel)
        self.lengthBarRight = self.canvas.create_rectangle(self.currentWidth - 1, LENGTH_BAR_SIDES_TOP, self.currentWidth, LENGTH_BAR_SIDES_BOTTOM, fill="black")
        self.lengthBar = self.canvas.create_rectangle(0, LENGTH_BAR_TOP, self.currentWidth, LENGTH_BAR_BOTTOM, fill="black")
        self.lengthBarLabel = self.canvas.create_text(self.currentWidth / 2, LENGT_BAR_LABEL_TOP, text=self.currentWidth)

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
            self.currentWidth = float(self.totalLengthEntry.get())
            return True
        else:
            return False

    def updateWeight(self, weight):
        self.totalWeight += weight
        self.canvas.delete(self.totalWeightLabel)
        self.totalWeightLabel = self.canvas.create_text(TOTAL_WEIGHT_LABEL_LEFT, TOTAL_WEIGHT_LABEL_TOP, text=self.totalWeight)

    def getGlassWeight(self, width, height):
        return (width * height) * GLASS_WEIGHT_MULTIPLYER

    def getStolpeWeight(self, width, height):
        return (width * height) * STOLPE_WEIGHT_MULTIPLYER

    def getVeggfesteWeight(self, width, height):
        return (width * height) * VEGGFESTE_WEIGHT_MULTIPLYER

root = tkinter.Tk(screenName="screenname", baseName="basename", className="classname", useTk=1)
root.geometry("1000x600")
root.configure(bg="white")

main = Main(root)

root.mainloop()