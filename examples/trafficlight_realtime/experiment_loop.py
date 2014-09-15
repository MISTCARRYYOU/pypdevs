from pypdevs.simulator import Simulator
from trafficLightModel import *
model = TrafficLight(name="trafficLight")

refs = {"INTERRUPT": model.INTERRUPT}
sim = Simulator(model)
sim.setRealTime(True)
sim.setRealTimeInputFile(None)
sim.setRealTimePorts(refs)
sim.setVerbose(None)
sim.setRealTimePlatformGameLoop()
sim.simulate()

import time
while 1:
    before = time.time()
    sim.realtime_loop_call()
    time.sleep(0.1 - (before - time.time()))
    print("Current state: " + str(model.state.get()))
