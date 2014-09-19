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

from testutils import *
from pypdevs.messageScheduler import MessageScheduler
from copy import deepcopy

class TestMessageScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = MessageScheduler()

    def tearDown(self):
        pass

    def test_mscheduler_schedule(self):
        self.assertTrue(len(self.scheduler.heap) == 0)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {})

        # Only [0] and [3] are important, so don't even bother 
        #  creating the rest
        msg = NetworkMessage((1, 1), {}, 12345, False, 0)

        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 1)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {})

        msg = deepcopy(msg)
        msg.uuid = 444
        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 2)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {})

        msg = deepcopy(msg)
        msg.uuid = 456
        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 3)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {})

    def test_mschedule_invalids(self):
        self.assertTrue(len(self.scheduler.heap) == 0)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {})

        # Only [0] and [3] are important, so don't even bother 
        #  creating the rest
        msg = NetworkMessage((1, 1), {}, 12345, False, 0)

        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 1)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {})

        msg = deepcopy(msg)
        msg.uuid = 1111
        self.scheduler.invalids = {1111: 1}
        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 1)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {1111: 0})

        msg = deepcopy(msg)
        msg.uuid = 1111
        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 2)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {1111: 0})

        msg = deepcopy(msg)
        msg.uuid = 234
        self.scheduler.invalids[234] = -2
        self.scheduler.schedule(msg)

        self.assertTrue(len(self.scheduler.heap) == 3)
        self.assertTrue(len(self.scheduler.processed) == 0)
        self.assertTrue(self.scheduler.invalids == {1111: 0, 234: -2})

    def test_mscheduler_unschedule(self):
        msg1 = NetworkMessage((3, 1), {}, 1, False, 0)
        msg2 = NetworkMessage((4, 1), {}, 2, False, 0)
        msg3 = NetworkMessage((5, 1), {}, 3, False, 0)
        self.scheduler.heap = [msg1, msg2, msg3]
        self.scheduler.processed = []

        self.scheduler.unschedule(msg2)

        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {2: 1})

        self.scheduler.unschedule(msg1)

        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {1: 1, 2: 1})

        msg4 = NetworkMessage((5, 1), {}, 4, False, 0)
        self.scheduler.unschedule(msg4)

        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {1: 1, 2: 1, 4: 1})

    def test_mscheduler_read_first(self):
        msg1 = NetworkMessage((3, 1), {}, 1, False, 0)
        msg2 = NetworkMessage((4, 1), {}, 2, False, 0)
        msg3 = NetworkMessage((5, 1), {}, 3, False, 0)
        self.scheduler.heap = [msg1, msg2, msg3]
        self.scheduler.processed = []

        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

        first = self.scheduler.readFirst()

        self.assertTrue(first == msg1)
        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

        first = self.scheduler.readFirst()

        self.assertTrue(first == msg1)
        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.invalids = {1: 1}
        first = self.scheduler.readFirst()

        self.assertTrue(first == msg2)
        self.assertTrue(self.scheduler.heap == [msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {1: 0})

    def test_mscheduler_removeFirst(self):
        msg1 = NetworkMessage((3, 1), {}, 1, False, 0)
        msg2 = NetworkMessage((4, 1), {}, 2, False, 0)
        msg3 = NetworkMessage((5, 1), {}, 3, False, 0)
        self.scheduler.heap = [msg1, msg2, msg3]
        self.scheduler.processed = []

        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.removeFirst()

        self.assertTrue(self.scheduler.heap == [msg2, msg3])
        self.assertTrue(self.scheduler.processed == [msg1])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.invalids = {2: 1}
        self.scheduler.removeFirst()

        self.assertTrue(self.scheduler.heap == [])
        self.assertTrue(self.scheduler.processed == [msg1, msg3])
        self.assertTrue(self.scheduler.invalids == {2: 0})

    def test_mscheduler_revert(self):
        msg1 = NetworkMessage((3, 1), {}, 1, False, 0)
        msg2 = NetworkMessage((4, 1), {}, 2, False, 0)
        msg3 = NetworkMessage((5, 1), {}, 3, False, 0)
        self.scheduler.heap = [msg3]
        self.scheduler.processed = [msg1, msg2]

        self.scheduler.revert((4, 1))

        self.assertTrue(self.scheduler.heap == [msg2, msg3])
        self.assertTrue(self.scheduler.processed == [msg1])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.revert((2, 1))

        self.assertTrue(self.scheduler.heap == [msg1, msg3, msg2])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.heap = []
        self.scheduler.processed = [msg1, msg2, msg3]

        self.scheduler.revert((2, 1))

        self.assertTrue(self.scheduler.heap == [msg1, msg2, msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

    def test_mscheduler_cleanup(self):
        msg1 = NetworkMessage((3, 1), {}, 1, False, 0)
        msg2 = NetworkMessage((4, 1), {}, 2, False, 0)
        msg3 = NetworkMessage((5, 1), {}, 3, False, 0)
        self.scheduler.heap = [msg3]
        self.scheduler.processed = [msg1, msg2]

        self.scheduler.cleanup((4, 1))

        self.assertTrue(self.scheduler.heap == [msg3])
        self.assertTrue(self.scheduler.processed == [msg2])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.cleanup((5, 1))

        self.assertTrue(self.scheduler.heap == [msg3])
        self.assertTrue(self.scheduler.processed == [])
        self.assertTrue(self.scheduler.invalids == {})

        self.scheduler.processed = [msg1, msg2]
        self.scheduler.invalids = {2: 1}
        self.scheduler.cleanup((4, 1))

        self.assertTrue(self.scheduler.heap == [msg3])
        self.assertTrue(self.scheduler.processed == [msg2])
        self.assertTrue(self.scheduler.invalids == {2: 1})
