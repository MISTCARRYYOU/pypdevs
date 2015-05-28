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

"""
Experiment file showing the invocation of the three benchmark models.

Each benchmark has several parameters. Some of these are passed as model
parameters, while some are currently hardcoded.

* Queue
  - number of models
  - random/fixed time advance
  - internal transition computation load
  - external transition computation load
  - size of the exchanged event
* High Interconnect
  - number of models
  - random/fixed time advance
  - internal transition computation load
  - external transition computation load
  - size of the exchanged event
* PHOLD
  - random/fixed time advance
  - models per LP
  - number of LPs
  - number of threads/nodes
  - remote fraction of events
  - internal transition computation load
  - size of the exchanged event

Example results are included for the following configurations:
Queue: results_Queue.eps
  - [3-300] models
  - random time advance
  - no computational load (0ms)
  - event containing 1 float

High Interconnect: results_HighInterconnect.eps
  - [3-300] models
  - random time advance
  - no computational load (0ms)
  - event containing 1 float

PHOLD (speedup): results_PHOLD_speedup.eps
  - random time advance
  - 10 models per LP
  - [1-50] LPs
  - [1-50] nodes (1 LP/node)
  - 10% remote events
  - equivalent of 25ms computation
  - event containing 1 float

PHOLD (remote fraction): results_PHOLD_remotes.eps
  - random time advance
  - 10 models per LP
  - 20 LPs
  - 20 nodes (1 LP/node)
  - [10%-100%] remote events
  - equivalent of 25ms computation
  - event containing 1 float

"""

### Global imports
from pypdevs.simulator import Simulator

### Queue
import QueueModel

QueueModel.is_random = True
m = QueueModel.Queue(10)
sim = Simulator(m)
sim.setTerminationTime(1)
sim.simulate()


### High Interconnect
import HighInterconnect
from HighInterconnect import HighInterconnect as HighInterconnectModel

HighInterconnect.is_random = True
m = HighInterconnectModel(10)
sim = Simulator(m)
sim.setTerminationTime(1)
sim.simulate()


### PHOLD
import PHOLD
from PHOLD import PHOLD as PHOLDModel

m = PHOLDModel(1, 10, 0, 0.1)
sim = Simulator(m)
sim.setTerminationTime(1000)
sim.simulate()
