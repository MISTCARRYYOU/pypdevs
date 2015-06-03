# Copyright 2014 Modelling, Simulation and Design Lab (MSDL) at 
# McGill University and the University of Antwerp (http://msdl.cs.mcgill.ca/)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from pypdevs.DEVS import AtomicDEVS, CoupledDEVS
from pypdevs.simulator import Simulator

inf = float('inf')

def getRandom(seed):
    if is_random:
        # Compute a new seed
        seed = (1664525 * seed + 1013904223) % 4294967296
        v = float(int(float(seed)/4294967296 * 1000)) / 1000
        return v, seed
    else:
        return 1.0, seed

class Event:
        def __init__(self, eventSize):
                self.eventSize = eventSize

        def copy(self):
            return Event(self.eventSize)

class Generator(AtomicDEVS):
        def __init__(self, seed):
                AtomicDEVS.__init__(self, "Generator")
                # State is now a tuple of the time to wait, and the seed to use next
                self.state = getRandom(seed)
                self.send_event = self.addOutPort("out_event")
                self.recv_event = self.addInPort("in_event")
                
        def timeAdvance(self):
                return self.state[0]

        def extTransition(self, inputs):
                # Decrease the time, but keep the seed the same
                return (self.state[0] - self.elapsed, self.state[1])

        def intTransition(self):
                # Get a new time to wait, but also a new seed
                return getRandom(self.state[1])

        def outputFnc(self):
                return {self.send_event: [Event(1)]}

class HighInterconnect(CoupledDEVS):
        def __init__(self, width):
                CoupledDEVS.__init__(self, "HighInterconnect")
                l = []
                # Give each generator a different seed to start with, otherwise it wouldn't be random
                seeds = [i * 1000 for i in range(width)]
                for i in range(width):
                    l.append(self.addSubModel(Generator(seeds[i])))
                for i in l:
                    for j in l:
                        if i != j:
                            self.connectPorts(i.send_event, j.recv_event)

if __name__ == "__main__":
    import sys
    global is_random
    is_random = (sys.argv[2][0] == "1")
    m = HighInterconnect(int(sys.argv[1]))
    sim = Simulator(m)
    sim.setTerminationTime(500.0)
    sim.simulate()
