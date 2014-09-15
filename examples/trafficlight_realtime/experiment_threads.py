from pypdevs.simulator import Simulator
from trafficLightModel import *
model = TrafficLight(name="trafficLight")

refs = {"INTERRUPT": model.INTERRUPT}
sim = Simulator(model)
sim.setRealTime(True)
sim.setRealTimeInputFile(None)
sim.setRealTimePorts(refs)
sim.setVerbose(None)
sim.setRealTimePlatformThreads()
sim.simulate()

# If we get here, simulation will also end, as the sleep calls are daemon threads
#  (otherwise, they would make the simulation unkillable)

while 1:
    sim.realtime_interrupt(raw_input())
