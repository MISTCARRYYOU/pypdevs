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

class ProcessorState:
        def __init__(self, seed):
                self.event1_counter = inf
                self.event1 = None
                self.queue = []
                self.seed = seed

class Processor(AtomicDEVS):
        def __init__(self, name, seed):
                AtomicDEVS.__init__(self, name)
                self.recv_event1 = self.addInPort("in_event1")
                self.send_event1 = self.addOutPort("out_event1")
                self.state = ProcessorState(seed)
                
        def timeAdvance(self):
                return self.state.event1_counter

        def intTransition(self):
                self.state.event1_counter -= self.timeAdvance()
                if self.state.event1_counter == 0 and len(self.state.queue) == 0:
                    self.state.event1_counter = inf
                    self.state.event1 = None
                else:
                    self.state.event1_counter, self.state.seed = getRandom(self.state.seed)
                    self.state.event1 = self.state.queue.pop()
                return self.state

        def extTransition(self, inputs):
                self.state.event1_counter -= self.elapsed
                for ev in inputs[self.recv_event1]:
                    if self.state.event1 is None:
                        self.state.event1 = ev
                        self.state.event1_counter, self.state.seed = getRandom(self.state.seed)
                    else:
                        self.state.queue.append(ev)
                return self.state

        def outputFnc(self):
                return {self.send_event1: [self.state.event1]}

class Generator(AtomicDEVS):
        def __init__(self):
                AtomicDEVS.__init__(self, "Generator")
                self.state = "gen_event1"
                self.send_event1 = self.addOutPort("out_event1")
                
        def timeAdvance(self):
                return 1.0

        def intTransition(self):
                return self.state

        def outputFnc(self):
                return {self.send_event1: [Event(1)]}

class Queue(CoupledDEVS):
        def __init__(self, width):
                CoupledDEVS.__init__(self, "Queue")
                self.generator = self.addSubModel(Generator())
                prev = self.generator
                seeds = [i * 1000 for i in range(width)]
                for i in range(width):
                    m = self.addSubModel(Processor("Processor%i" % i, seeds[i]))
                    self.connectPorts(prev.send_event1, m.recv_event1)
                    prev = m

if __name__ == "__main__":
    import sys
    global is_random
    is_random = (sys.argv[2][0] == "1")
    m = Queue(int(sys.argv[1]))
    sim = Simulator(m)
    sim.setTerminationTime(500.0)
    sim.simulate()
