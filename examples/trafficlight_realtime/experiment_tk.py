from pypdevs.simulator import Simulator

from Tkinter import *
from trafficLightModel import *

isBlinking = None

model = TrafficLight(name="trafficLight")
refs = {"INTERRUPT": model.INTERRUPT}
root = Tk()

sim = Simulator(model)
sim.setRealTime(True)
sim.setRealTimeInputFile(None)
sim.setRealTimePorts(refs)
sim.setVerbose(None)
sim.setRealTimePlatformTk(root)

def toManual():
    global isBlinking
    isBlinking = False
    sim.realtime_interrupt("INTERRUPT toManual")

def toAutonomous():
    global isBlinking
    isBlinking = None
    sim.realtime_interrupt("INTERRUPT toAutonomous")

size = 50
xbase = 10
ybase = 10

frame = Frame(root)
canvas = Canvas(frame)
canvas.create_oval(xbase, ybase, xbase+size, ybase+size, fill="black", tags="red_light")
canvas.create_oval(xbase, ybase+size, xbase+size, ybase+2*size, fill="black", tags="yellow_light")
canvas.create_oval(xbase, ybase+2*size, xbase+size, ybase+3*size, fill="black", tags="green_light")
canvas.pack()
frame.pack()

def updateLights():
    state = model.state.get()
    if state == "red":
        canvas.itemconfig("red_light", fill="red")
        canvas.itemconfig("yellow_light", fill="black")
        canvas.itemconfig("green_light", fill="black")
    elif state == "yellow":
        canvas.itemconfig("red_light", fill="black")
        canvas.itemconfig("yellow_light", fill="yellow")
        canvas.itemconfig("green_light", fill="black")
    elif state == "green":
        canvas.itemconfig("red_light", fill="black")
        canvas.itemconfig("yellow_light", fill="black")
        canvas.itemconfig("green_light", fill="green")
    elif state == "manual":
        canvas.itemconfig("red_light", fill="black")
        global isBlinking
        if isBlinking:
            canvas.itemconfig("yellow_light", fill="yellow")
            isBlinking = False
        else:
            canvas.itemconfig("yellow_light", fill="black")
            isBlinking = True
        canvas.itemconfig("green_light", fill="black")
    root.after(500,  updateLights)

b = Button(root, text="toManual", command=toManual)
b.pack()
c = Button(root, text="toAutonomous", command=toAutonomous)
c.pack()

root.after(100, updateLights)

sim.simulate()
root.mainloop()
