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
from testLocal import TestLocal
from testTermination import TestTermination
from testTestUtils import TestTestUtils
from testLogger import TestLogger

if __name__ == '__main__':
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

    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)
