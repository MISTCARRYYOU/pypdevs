def tkMainThreadPoller(tk, queue):
    """
    The polling function to register with Tk at the start. This will do the actual scheduling in Tk.

    :param tk: the Tk instance to use
    :param queue: the queue to check
    """
    global tkRunningID
    while 1:
        try:
            time, func = queue.popleft()
            tkRunningID = tk.after(time, func)
        except TypeError:
            # Was an invalidation call
            try:
                if tkRunningID is not None:
                    tk.after_cancel(tkRunningID)
            except IndexError:
                # Nothing to cancel
                pass
            tkRunningID = None
        except IndexError:
            break
    tk.after(10, tkMainThreadPoller, tk, queue)

class ThreadingTkInter(object):
    """
    Tk Inter subsystem for realtime simulation
    """
    def __init__(self, tk):
        """
        Constructor

        :param queue: the queue object that is also used by the main thread to put events on the main Tk object
        """
        self.runningID = None
        self.lastInfinity = False
        import collections
        queue = collections.deque()
        self.queue = queue
        tk.after(10, tkMainThreadPoller, tk, queue)

    def unlock(self):
        """
        Unlock the waiting thread
        """
        # Don't get it normally, as it would seem like a method call
        getattr(self, "func")()

    def wait(self, time, func):
        """
        Wait for the specified time, or faster if interrupted

        :param time: time to wait
        :param func: the function to call
        """
        if time == float('inf'):
            self.lastInfinity = True
        else:
            self.lastInfinity = False
            self.func = func
            self.queue.append((int(time*1000), self.unlock))

    def interrupt(self):
        """
        Interrupt the waiting thread
        """
        if not self.lastInfinity:
            self.queue.append(None)
        self.unlock()
