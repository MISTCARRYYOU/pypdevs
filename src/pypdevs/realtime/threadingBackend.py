import threading

class ThreadingBackend(object):
    """
    Wrapper around the actual threading backend. It will also handle interrupts and the passing of them to the calling thread.
    """
    def __init__(self, subsystem, args):
        """
        Constructor

        :param subsystem: string specifying the subsystem to use: python, tkinter or loop
        :param args: all additional arguments that should be passed to the subsystem's constructor (must be a list)
        """
        self.interruptedValue = None
        self.valueLock = threading.Lock()
        if subsystem == "python":
            from pypdevs.realtime.threadingPython import ThreadingPython
            self.subsystem = ThreadingPython(*args)
        elif subsystem == "tkinter":
            from pypdevs.realtime.threadingTkInter import ThreadingTkInter
            self.subsystem = ThreadingTkInter(*args)
        elif subsystem == "loop":
            from pypdevs.realtime.threadingGameLoop import ThreadingGameLoop
            self.subsystem = ThreadingGameLoop(*args)
        else:
            raise Exception("Realtime subsystem not found: " + str(subsystem))

    def wait(self, time, func):
        """
        A non-blocking call, which will call the *func* parameter after *time* seconds. It will use the provided backend to do this.

        :param time: time to wait in seconds, a float is possible
        :param func: the function to call after the time has passed
        """
        self.subsystem.wait(time, func)

    def interrupt(self, value):
        """
        Interrupt a running wait call.

        :param value: the value that interrupts
        """
        with self.valueLock:
            self.interruptedValue = value
            self.subsystem.interrupt()

    def setInterrupt(self, value):
        """
        Sets the value of the interrupt. This should not be used manually and is only required to prevent the asynchronous combo generator from making *interrrupt()* calls.
        
        :param value: value with which the interrupt variable should be set
        """
        with self.valueLock:
            if self.interruptedValue is None:
                self.interruptedValue = value
                return True
            else:
                # The interrupt was already set, indicating a collision!
                return False

    def getInterrupt(self):
        """
        Return the value of the interrupt and clear it internally.

        :returns: the interrupt
        """
        with self.valueLock:
            val = self.interruptedValue
            self.interruptedValue = None
        return val

    def step(self):
        """
        Perform a step in the backend; only supported for the game loop backend.
        """
        self.subsystem.step()
