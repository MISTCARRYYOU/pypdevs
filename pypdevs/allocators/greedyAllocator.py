# Copyright 2014 Modelling, Simulation and Design Lab (MSDL) at 
# McGill University and the University of Antwerp (http://msdl.cs.mcgill.ca/)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import defaultdict

class GreedyAllocator(object):
    """
    Allocate all models in a greedy manner: make the most heavy link local and extend from there on until an average load is reached.
    """
    def allocate(self, models, edges, nrnodes, totalActivities):
        """
        Calculate allocations for the nodes, using the information provided.

        :param models: the models to allocte
        :param edges: the edges between the models
        :param nrnodes: the number of nodes to allocate over. Simply an upper bound!
        :param totalActivities: activity tracking information from each model
        :returns: allocation that was found
        """
        # Run over all edges to create the nodes and link in their edges
        nodes = {}
        remainingEdges = set()
        toAlloc = set()
        for source in edges:
            for destination in edges[source]:
                # A connection from 'source' to 'destination'
                edge = edges[source][destination]
                nodes.setdefault(source, []).append((edge, destination))
                nodes.setdefault(destination, []).append((edge, source))
                remainingEdges.add((edge, source, destination))
                toAlloc.add(destination)
            toAlloc.add(source)
        # OK, nodes are constructed

        # Allocate 1 node too much for spilling
        nrnodes += 1

        # Find average activity (our target)
        avgActivity = sum([totalActivities[i] for i in totalActivities])/nrnodes

        # Get the strongest edge
        allocNode = 0
        nodeLoad = []
        allocation = {}
        allocation_rev = defaultdict(set)
        while allocNode < (nrnodes - 1):
            while remainingEdges:
                maxEdge = max(remainingEdges)
                remainingEdges.remove(maxEdge)
                edgeWeight, source, destination = maxEdge
                if source in toAlloc and destination in toAlloc:
                    break
            else:
                break
            activity_source = totalActivities[source.model_id]
            activity_destination = totalActivities[destination.model_id]
            nodeLoad.append(activity_source + activity_destination)
            allocation[source.model_id] = allocNode
            allocation[destination.model_id] = allocNode
            allocation_rev[allocNode].add(source)
            allocation_rev[allocNode].add(destination)
            toAlloc.remove(source)
            toAlloc.remove(destination)
            while nodeLoad[allocNode] < averageActivity:
                edgeSearch = []
                for edge in remainingEdges:
                    if ((edge[1] in allocation_rev[allocNode] and
                         edge[2] in toAlloc) or
                        (edge[2] in allocation_rev[allocNode] and
                         edge[1] in toAlloc)):
                        edgeSearch.append(edge)
                if not edgeSearch:
                    break
                # Allocate some more nodes
                maxEdge = max(edgeSearch)
                remainingEdges.remove(maxEdge)
                edgeWeight, source, destination = maxEdge
                # Ok, this is an unbound connection, so add it
                if source in toAlloc:
                    toAlloc.remove(source)
                    allocation[source.model_id] = allocNode
                    allocation_rev[allocNode].add(source.model_id)
                    nodeLoad[allocNode] += totalActivities[source.model_id]
                if destination in toAlloc:
                    toAlloc.remove(destination)
                    allocation[destination.model_id] = allocNode
                    allocation_rev[allocNode].add(destination.model_id)
                    nodeLoad[allocNode] += totalActivities[destination.model_id]
            allocNode += 1

        # All unassigned nodes are for the spill node
        # Undo our spilling node
        while toAlloc:
            changes = False
            n = list(toAlloc)
            for model in n:
                options = set()
                for oport in model.OPorts:
                    for oline, _ in oport.routingOutLine:
                        location = oline.hostDEVS.location
                        if oline.hostDEVS.location is not None:
                            options.add((nodeLoad[location], location))
                for iport in model.IPorts:
                    for iline in oport.routingInLine:
                        location = iline.hostDEVS.location
                        if iline.hostDEVS.location is not None:
                            options.add((nodeLoad[location], location))
                if not options:
                    continue
                # Get the best option
                _, loc = min(options)
                nodeLoad[loc] += totalActivities[model.model_id]
                allocation[model.model_id] = loc
                allocation_rev[loc].add(model.model_id)
                toAlloc.remove(model)
            if not changes:
                # An iteration without changes, means that we loop forever
                for m in toAlloc:
                    # Force an allocation to 0
                    allocation[m.model_id] = 0
                    # allocation_rev doesn't need to be updated
                break
        return allocation

    def getTerminationTime(self):
        """
        Returns the time it takes for the allocator to make an 'educated guess' of the advised allocation.
        This time will not be used exactly, but as soon as the GVT passes over it. While this is not exactly 
        necessary, it avoids the overhead of putting such a test in frequently used code.

        :returns: float -- the time at which to perform the allocations (and save them)
        """
        return 10.0
