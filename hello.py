#!/usr/bin/python3
import tkinter
from tkinter import *

class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], toSelect=0):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            if toSelect == 0:
                chk.select()
            chk.pack(side=LEFT)
            self.vars.append(var)
    def state(self):
        return map((lambda var: var.get()), self.vars)

if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.geometry("1500x500")

    #Sets
    setLabel = Label(root, text="Sets")
    setLabel.place(x=10, y=10)
    setCheckBar = Checkbar(root, ["DOM","HA1","HA2","HA3","E02","RIX","M19","GRN","RNA","WAR","M20","ELD","THB","IKO","M21"])
    setCheckBar.place(x=10, y=30)
    setCheckBar.config(relief=GROOVE, bd=2)

    #Mana Colors
    manaLabel = Label(root, text="Mana Colors")
    manaLabel.place(x=10, y=60)
    manaFrame = Frame(root)
    manaFrame.pack()
    manaFrame.place(x=10, y=80)
    noColor = Checkbar(manaFrame, ["Colorless"])
    noColor.pack()
    monoColor = Checkbar(manaFrame, ["R", "W", "G", "U", "B"])
    monoColor.pack()
    dualColor = Checkbar(manaFrame, ["RW", "RG", "RU", "RB", "WG", "WU", "WB", "GU", "GB", "UB"])
    dualColor.pack()
    triColor = Checkbar(manaFrame, ["RGB", "WGU", "BRU", "GWR", "UWB", "URW", "RWB", "BGU", "RUG", "WGB"])
    triColor.pack()
    quadColor = Checkbar(manaFrame, ["RGBU", "RGBW", "RGWU", "WBUG", "WRBU"], toSelect=1)
    quadColor.pack()
    allColor = Checkbar(manaFrame, ["WRBUG"], toSelect=1)
    allColor.pack()
    manaFrame.config(relief=GROOVE, bd=2)
  
    #Normal Cards
    normalCard = Label(root, text="Normal Card Rarities")
    normalCard.place(x=10, y=230)
    normalFrame = Frame(root)
    normalFrame.pack()
    normalFrame.place(x=10, y=250)
    Label(normalFrame, text="Common").grid(row=0)
    Label(normalFrame, text="Uncommon").grid(row=1)
    Label(normalFrame, text="Rare").grid(row=2)
    Label(normalFrame, text="Mythic").grid(row=3)
    normalC = Entry(normalFrame)
    normalUC = Entry(normalFrame)
    normalR = Entry(normalFrame)
    normalM = Entry(normalFrame)
    normalC.insert(10, ".15")
    normalUC.insert(10, ".75")
    normalR.insert(10, ".10")
    normalM.insert(10, ".00")
    normalC.grid(row=0, column=1)
    normalUC.grid(row=1, column=1)
    normalR.grid(row=2, column=1)
    normalM.grid(row=3, column=1)
    normalFrame.config(relief=GROOVE, bd=2)

    #commander Cards
    commanderCard = Label(root, text="commander Card Rarities")
    commanderCard.place(x=10, y=230)
    commanderFrame = Frame(root)
    commanderFrame.pack()
    commanderFrame.place(x=10, y=250)
    Label(commanderFrame, text="Common").grid(row=0)
    Label(commanderFrame, text="Uncommon").grid(row=1)
    Label(commanderFrame, text="Rare").grid(row=2)
    Label(commanderFrame, text="Mythic").grid(row=3)
    commanderC = Entry(commanderFrame)
    commanderUC = Entry(commanderFrame)
    commanderR = Entry(commanderFrame)
    commanderM = Entry(commanderFrame)
    commanderC.insert(10, ".15")
    commanderUC.insert(10, ".75")
    commanderR.insert(10, ".10")
    commanderM.insert(10, ".00")
    commanderC.grid(row=0, column=1)
    commanderUC.grid(row=1, column=1)
    commanderR.grid(row=2, column=1)
    commanderM.grid(row=3, column=1)
    commanderFrame.config(relief=GROOVE, bd=2)

        #land Cards
    landCard = Label(root, text="land Card Rarities")
    landCard.place(x=10, y=230)
    landFrame = Frame(root)
    landFrame.pack()
    landFrame.place(x=10, y=250)
    Label(landFrame, text="Common").grid(row=0)
    Label(landFrame, text="Uncommon").grid(row=1)
    Label(landFrame, text="Rare").grid(row=2)
    Label(landFrame, text="Mythic").grid(row=3)
    landC = Entry(landFrame)
    landUC = Entry(landFrame)
    landR = Entry(landFrame)
    landM = Entry(landFrame)
    landC.insert(10, ".15")
    landUC.insert(10, ".75")
    landR.insert(10, ".10")
    landM.insert(10, ".00")
    landC.grid(row=0, column=1)
    landUC.grid(row=1, column=1)
    landR.grid(row=2, column=1)
    landM.grid(row=3, column=1)
    landFrame.config(relief=GROOVE, bd=2)

    def allstates():
        retValue = [list(setCheckBar.state()), list(noColor.state()) + list(monoColor.state()) + list(dualColor.state()) + list(triColor.state()) + list(quadColor.state()) + list(allColor.state()), [normalC.get(), normalUC.get(), normalR.get(), normalM.get()]]
        print(retValue)
    Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
    Button(root, text='Peek', command=allstates).pack(side=RIGHT)
    
    root.mainloop()
