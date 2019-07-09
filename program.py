import tkinter
# https://www.geeksforgeeks.org/python-gui-tkinter/

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

        self.okButton = tkinter.Button(self.topContainer, text="ok", command=self.printStuff)
        self.okButton.pack(side="left")


        # ------------ Middle Frame ---------------


        self.canvas = tkinter.Canvas(master, bg="lightgray")
        self.canvas.pack(side="top", fill="both", expand=1, padx=50)


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


    def printStuff(self):
        print(self.totalLengthEntry.get())
        self.totalLengthEntry.delete(0, "end")
        self.totalLengthEntry.insert(0, 100)
        print(self.totalLengthEntry.get())

    def addVeggfeste(self):
        tmp = self.canvas.create_rectangle(self.currentWidth, 200, self.currentWidth + self.veggfesteWidth, 300, fill="gray")
        self.currentWidth += self.veggfesteWidth
        self.canvasItems.append((tmp, self.veggfesteWidth))

    def addGlass(self):
        self.glassWidth = int(self.glassEntry.get())
        # self.glassEntry.insert(0, self.glassWidth)

        tmp = self.canvas.create_rectangle(self.currentWidth, 220, self.currentWidth + self.glassWidth, 300, fill="blue")
        self.currentWidth += self.glassWidth
        self.canvasItems.append((tmp, self.glassWidth))

    def addStolpe(self):
        tmp = self.canvas.create_rectangle(self.currentWidth, 200, self.currentWidth + self.stolpeWidth, 300, fill="black") 
        self.currentWidth += self.stolpeWidth
        self.canvasItems.append((tmp, self.stolpeWidth))

    def regret(self):
        item = self.canvasItems.pop()
        self.canvas.delete(item[0])
        self.currentWidth -= item[1]




root = tkinter.Tk(screenName="screenname", baseName="basename", className="classname", useTk=1)
root.geometry("1000x600")
root.configure(bg="white")

main = Main(root)

root.mainloop()