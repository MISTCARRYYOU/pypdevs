from threading import Event, Thread, Lock
import time

class ThreadingPython(object):
    """
    Simple Python threads subsystem
    """
    def __init__(self):
        """
        Constructor
        """
        self.evt = Event()
        self.evtLock = Lock()

    def wait(self, delay, func):
        """
        Wait for the specified time, or faster if interrupted

        :param delay: time to wait
        :param func: the function to call
        """
        #NOTE this call has a granularity of 5ms in Python <= 2.7.x in the worst case, so beware!
        #     the granularity seems to be much better in Python >= 3.x
        p = Thread(target=ThreadingPython.callFunc, args=[self, delay, func])
        p.daemon = True
        p.start()

    def interrupt(self):
        """
        Interrupt the waiting thread
        """
        with self.evtLock:
            self.evt.set()

    def callFunc(self, delay, func):
        """
        Function to call on a seperate thread: will block for the specified time and call the function afterwards
        """
        with self.evtLock:
            self.evt.wait(delay)
            func()
            self.evt.clear()
