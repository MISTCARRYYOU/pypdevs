import select
import sys
import threading
import time
from pypdevs.util import DEVSException

class AsynchronousComboGenerator(object):
    """
    The asynchronous combo generator: it generates events from file input
    The name no longer represents what it actually is, as previously it also generated input from stdin (denoting the 'combo').
    It does NOT use the default *interrupt()* calls for the threading backend, as this would require the generator to run
    on a different thread. The generator should be called at every iteration and its *getNextTime()* value should be taken into
    account by every *wait()* call.
    """
    def __init__(self, filename, backend):
        """
        Constructor.

        :param filename: the name of the input file to use for file input. None for no file input.
        :param backend: subsystem to use for threading

        .. note:: *filename* parameter should not be a file handle
        """
        self.backend = backend
        if filename is not None:
            self.infile = open(filename, 'r')
        else:
            self.infile = None
        self.nextScheduled = float('inf')
        self.file_event = None
        # Call this here already for time 0, to schedule the first event
        self.checkInterrupt(0)

    def checkInterrupt(self, currentTime):
        """
        Checks for whether an interrupt should happen at this time; if so, it also reschedules the next one.
        This method must be called before the internal interrupt is fetched, as otherwise it will not be taken into account.

        :param currentTime: the current simulation time to check for interrupts
        """
        if self.infile is not None:
            # First check for if the scheduled message happened
            if (self.nextScheduled - currentTime) <= 0:
                if self.backend.setInterrupt(self.file_event):
                    self.nextScheduled = float('inf')
                    self.file_event = None
 
            # Now check for the next one
            if self.nextScheduled == float('inf'):
                # We don't have a scheduled event, so fetch one
                line = self.infile.readline()
                if line == "":
                    self.infile.close()
                    self.infile = None
                else:
                    event = line.split(" ", 1)
                    if len(event) != 2:
                        raise DEVSException(
                            "Inproperly formatted input in file: %s" % event)
                    self.nextScheduled = float(event[0])
                    self.file_event = event[1][:-1]

    def getNextTime(self):
        """
        Return the time of the next event from this generator
        """
        return self.nextScheduled
