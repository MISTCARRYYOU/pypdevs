class Tracers(object):
    """
    Interface for all tracers
    """
    def __init__(self):
        """
        Constructor
        """
        self.tracers = []
        self.tracers_init = []
        self.uid = 0

    def registerTracer(self, tracer, server, recover):
        """
        Register a tracer, so that it will also receive all transitions.

        :param tracer: tuple of the form (file, classname, [args])
        :param server: the server object to be able to make remote calls
        :param recover: whether or not this is a recovered registration (used during checkpointing)
        """
        try:
            exec("from pypdevs.tracers.%s import %s" % tracer[0:2])
        except:
            exec("from %s import %s" % tracer[0:2])
        self.tracers.append(eval("%s(%i, server, *%s)" % (tracer[1], self.uid, tracer[2])))
        self.tracers_init.append(tracer)
        self.uid += 1
        self.tracers[-1].startTracer(recover)

    def hasTracers(self):
        """
        Checks whether or not there are any registered tracers

        :returns: bool
        """
        return len(self.tracers) > 0

    def getByID(self, uid):
        """
        Gets a tracer by its UID

        :param uid: the UID of the tracer to return
        :returns: tracer
        """
        return self.tracers[uid]

    def stopTracers(self):
        """
        Stop all registered tracers
        """
        for tracer in self.tracers:
            tracer.stopTracer()

    def tracesUser(self, time, aDEVS, variable, value):
        """
        Perform all tracing actions for a user imposed modification. This is NOT supported by default DEVS, so we don't require tracers to handle this either.

        :param time: the time at which the modification happend; this will be the termination time of the previous simulation run and **not** the time at which the timeAdvance was recomputed!
        :param aDEVS: the atomic DEVS model that was altered
        :param variable: the variable that was altered (as a string)
        :param value: the new value of the variable
        """
        for tracer in self.tracers:
            try:
                tracer.traceUser(time, aDEVS, variable, value)
            except AttributeError:
                # Some tracers choose to ignore this event
                pass

    def tracesInit(self, aDEVS, t):
        """
        Perform all tracing actions for an initialisation
        
        :param aDEVS: the model that was initialised
        :param t: the time at which the initialisation should be logged
        """
        for tracer in self.tracers:
            tracer.traceInit(aDEVS, t)

    def tracesInternal(self, aDEVS):
        """
        Perform all tracing actions for an internal transition
        
        :param aDEVS: the model that transitioned
        """
        for tracer in self.tracers:
            tracer.traceInternal(aDEVS)

    def tracesExternal(self, aDEVS):
        """
        Perform all tracing actions for an external transition
        
        :param aDEVS: the model that transitioned
        """
        for tracer in self.tracers:
            tracer.traceExternal(aDEVS)

    def tracesConfluent(self, aDEVS):
        """
        Perform all tracing actions for a confluent transition
        
        :param aDEVS: the model that transitioned
        """
        for tracer in self.tracers:
            tracer.traceConfluent(aDEVS)