import unittest
import subprocess
import os
import sys

from testMPI import TestMPI

if __name__ == '__main__':
    import mpi4py
    mpi = unittest.TestLoader().loadTestsFromTestCase(TestMPI)

    allTests = unittest.TestSuite()
    allTests.addTest(mpi)

    unittest.TextTestRunner(verbosity=2, failfast=True).run(allTests)
