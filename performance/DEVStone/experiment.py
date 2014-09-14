import sys
import random

schedulers = ["setSchedulerSortedList", "setSchedulerActivityHeap", "setSchedulerMinimalList", "setSchedulerHeapSet", "setSchedulerPolymorphic"]

if len(sys.argv) != 4:
    print("Expected parameters: scheduler size randomta")
    sys.exit(1)

scheduler = sys.argv[1]
if scheduler not in schedulers:
    print("Expected scheduler in " + str(schedulers))
    sys.exit(1)

size = int(sys.argv[2])
randomta = True if sys.argv[3].lower() in ["true", "1", "yes"] else False
from pypdevs.simulator import Simulator

from model import DEVStone
random.seed(1)
model = DEVStone(3, size, randomta)
sim = Simulator(model)
sim.setMessageCopy('none')
getattr(sim, scheduler)()
sim.setTerminationTime(1000)
sim.simulate()
