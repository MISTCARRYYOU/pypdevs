import sys
import random

from pypdevs.simulator import Simulator
import time

if len(sys.argv) != 3:
    print("Expected parameters: scheduler size")
    sys.exit(1)

scheduler = sys.argv[1]
size = int(sys.argv[2])

from model import FireSpread
model = FireSpread(size, size)
sim = Simulator(model)
sim.setMessageCopy('none')
getattr(sim, scheduler)()
sim.setTerminationTime(150)
sim.simulate()
