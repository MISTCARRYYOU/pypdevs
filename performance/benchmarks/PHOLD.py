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
import os.path
import random

import pypdevs
from pypdevs.DEVS import AtomicDEVS, CoupledDEVS

class PHOLDModelState(object):
    def __init__(self):
        self.event = []

    def copy(self):
        a = PHOLDModelState()
        a.event = [list(b) for b in self.event]
        return a

    def __eq__(self, other):
        return other.event == self.event

def getProcTime(event):
    random.seed(event)
    return random.random()

def getNextDestination(event, nodenum, local, remote, percentageremotes):
    random.seed(event)
    if random.random() > percentageremotes or len(remote) == 0:
        return local[int(random.uniform(0, len(local)))]
    else:
        return remote[int(random.uniform(0, len(remote)))]

def getRand(event):
    # For determinism with a global random number generator
    # This only works because each node runs its own Python interpreter
    random.seed(event)
    return int(random.uniform(0, 60000))

class HeavyPHOLDProcessor(AtomicDEVS):
    def __init__(self, name, iterations, totalAtomics, modelnumber, local, remote, percentageremotes):
        AtomicDEVS.__init__(self, name)
        self.inport = self.addInPort("inport")
        self.percentageremotes = percentageremotes
        self.outports = []
        self.totalAtomics = totalAtomics
        self.modelnumber = modelnumber
        for i in xrange(totalAtomics):
            self.outports.append(self.addOutPort("outport_" + str(i)))
        self.state = PHOLDModelState()
        ev = modelnumber
        self.state.event = [[ev, getProcTime(ev)]]
        self.iterations = iterations
        self.local = local
        self.remote = remote
        
    def timeAdvance(self):
        if len(self.state.event) > 0:
            return self.state.event[0][1]
        else:
            return float('inf')

    def confTransition(self, inputs):
        if len(self.state.event) > 1:
            self.state.event = self.state.event[1:]
        else:
            self.state.event = []
        for i in inputs[self.inport]:
            self.state.event.append([i, getProcTime(i)])
            for _ in xrange(self.iterations):
                pass
        return self.state
        
    def intTransition(self):
        self.state.event = self.state.event[1:]
        return self.state

    def extTransition(self, inputs):
        if len(self.state.event) > 0:
            self.state.event[0][1] -= self.elapsed
        for i in inputs[self.inport]:
            self.state.event.append([i, getProcTime(i)])
            # Just keep ourself busy for some time
            for _ in xrange(self.iterations):
                pass
        return self.state

    def outputFnc(self):
        if len(self.state.event) > 0:
            i = self.state.event[0]
            return {self.outports[getNextDestination(i[0], self.modelnumber, self.local, self.remote, self.percentageremotes)]: [getRand(i[0])]}
        else:
            return {}

class PHOLD(CoupledDEVS):
    def __init__(self, nodes, atomicsPerNode, iterations, percentageremotes):
        CoupledDEVS.__init__(self, "PHOLD")
        self.processors = []
        have = 0
        destinations = []
        cntr = 0
        totalAtomics = nodes * atomicsPerNode
        procs = []
        for node in range(nodes):
            procs.append([])
            for i in range(atomicsPerNode):
                procs[-1].append(atomicsPerNode*node+i)
        cntr = 0
        global distributed
        for e, i in enumerate(procs):
            allnoi = []
            for e2, j in enumerate(procs):
                if e2 != e:
                    allnoi.extend(j)
            for j in i:
                inoj = list(i)
                inoj.remove(j)
                self.processors.append(self.addSubModel(HeavyPHOLDProcessor("Processor_%d" % cntr, iterations, totalAtomics, cntr, inoj, allnoi, percentageremotes), e if distributed else 0))
                cntr += 1

        # All nodes created, now create all connections
        for i in range(len(self.processors)):
            for j in range(len(self.processors)):
                if i == j:
                    continue
                self.connectPorts(self.processors[i].OPorts[j], self.processors[j].inport)

try:
    from mpi4py import MPI
    distributed = MPI.COMM_WORLD.Get_size() > 1
except:
    distributed = False
