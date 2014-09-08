import time
from threading import Lock

class ThreadingGameLoop(object):
    """
    Game loop subsystem for realtime simulation. Time will only progress when a *step* call is made.
    """
    def __init__(self):
        """
        Constructor
        """
        self.nextEvent = float('inf')

    def step(self):
        """
        Perform a step in the simulation. Actual processing is done in a seperate thread.
        """
        if time.time() >= self.nextEvent:
            self.nextEvent = float('inf')
            getattr(self, "func")()
        
    def wait(self, delay, func):
        """
        Wait for the specified time, or faster if interrupted

        :param time: time to wait
        :param func: the function to call
        """
        self.func = func
        self.nextEvent = time.time() + delay
    
    def interrupt(self):
        """
        Interrupt the waiting thread
        """
        self.nextEvent = 0
