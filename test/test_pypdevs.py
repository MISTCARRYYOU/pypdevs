import unittest
import subprocess
import os
import sys

from testMessageScheduler import TestMessageScheduler
from testScheduler import TestScheduler
from testActions import TestActions
from testHelpers import TestHelpers
from testGVT import TestGVT
from testWait import TestWait
from testExceptions import TestExceptions
from testMPI import TestMPI
from testLocal import TestLocal
from testRealtime import TestRealtime
from testTermination import TestTermination
from testTestUtils import TestTestUtils
from testLogger import TestLogger

if __name__ == '__main__':
    # Do general setup of all servers
    runMPI = True
    try:
        import mpi4py
    except ImportError:
        runMPI = False

    realtime = False if len(sys.argv) == 1 else bool(sys.argv[1])

    # Run the tests
    if runMPI:
        mpi = unittest.TestLoader().loadTestsFromTestCase(TestMPI)
    local = unittest.TestLoader().loadTestsFromTestCase(TestLocal)
    actions = unittest.TestLoader().loadTestsFromTestCase(TestActions)
    termination = unittest.TestLoader().loadTestsFromTestCase(TestTermination)
    gvt = unittest.TestLoader().loadTestsFromTestCase(TestGVT)
    exceptions = unittest.TestLoader().loadTestsFromTestCase(TestExceptions)
    wait = unittest.TestLoader().loadTestsFromTestCase(TestWait)
    helpers = unittest.TestLoader().loadTestsFromTestCase(TestHelpers)
    scheduler = unittest.TestLoader().loadTestsFromTestCase(TestScheduler)
    mscheduler = unittest.TestLoader().loadTestsFromTestCase(TestMessageScheduler)
    testutils = unittest.TestLoader().loadTestsFromTestCase(TestTestUtils)
    logger = unittest.TestLoader().loadTestsFromTestCase(TestLogger)
    if realtime:
        realtime = unittest.TestLoader().loadTestsFromTestCase(TestRealtime)

    allTests = unittest.TestSuite()
    allTests.addTest(testutils)
    allTests.addTest(actions)
    allTests.addTest(helpers)
    allTests.addTest(gvt)
    allTests.addTest(termination)
    allTests.addTest(exceptions)
    allTests.addTest(wait)
    allTests.addTest(scheduler)
    allTests.addTest(logger)
    allTests.addTest(local)
    if realtime:
        allTests.addTest(realtime)
    if runMPI:
        allTests.addTest(mpi)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)

    if not runMPI:
        print("SKIPPED parallel tests: mpi4py not found")
    if not realtime:
        print("SKIPPED realtime tests: run with argument 'True' to run them (takes some time!)")
