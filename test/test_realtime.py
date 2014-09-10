import unittest
import subprocess
import os
import sys

from testRealtime import TestRealtime

if __name__ == '__main__':
    realtime = unittest.TestLoader().loadTestsFromTestCase(TestRealtime)
    allTests = unittest.TestSuite()
    allTests.addTest(realtime)
    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)
