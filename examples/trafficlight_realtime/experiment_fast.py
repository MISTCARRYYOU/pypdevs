from pypdevs.simulator import Simulator
from trafficLightModel import *
model = TrafficLight(name="trafficLight")

sim = Simulator(model)
sim.setVerbose(None)
sim.simulate()
