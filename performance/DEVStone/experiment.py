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
import random

if len(sys.argv) != 4:
    print("Expected parameters: scheduler size randomta")
    sys.exit(1)

scheduler = sys.argv[1]
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
