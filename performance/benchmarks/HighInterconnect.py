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

inf = float('inf')
seed = 1

def getRandom():
    if is_random:
        global seed
        seed = (1664525 * seed + 1013904223) % 4294967296
        v = float(int(float(seed)/4294967296 * 1000)) / 1000
        return v
    else:
        return 1.0

class Event:
        def __init__(self, eventSize):
                self.eventSize = eventSize

        def copy(self):
            return Event(self.eventSize)

class Generator(AtomicDEVS):
        def __init__(self):
                AtomicDEVS.__init__(self, "Generator")
                self.state = getRandom()
                self.send_event = self.addOutPort("out_event")
                self.recv_event = self.addInPort("in_event")
                
        def timeAdvance(self):
                return self.state

        def extTransition(self, inputs):
                return self.state - self.elapsed

        def intTransition(self):
                return getRandom()

        def outputFnc(self):
                return {self.send_event: [Event(1)]}

class HighInterconnect(CoupledDEVS):
        def __init__(self, width):
                CoupledDEVS.__init__(self, "HighInterconnect")
                l = []
                for i in range(width):
                    l.append(self.addSubModel(Generator()))
                for i in l:
                    for j in l:
                        if i != j:
                            self.connectPorts(i.send_event, j.recv_event)

if __name__ == "__main__":
    import sys
    global is_random
    is_random = (sys.argv[2][0] == "1")
    m = HighInterconnect(int(sys.argv[1]))
    from pypdevs.schedulers.schedulerChibiList import SchedulerChibiList as Sched
    sim = Simulator(m, Sched)
    sim.setTerminationTime(500.0)
    sim.simulate()
