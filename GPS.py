
class GPS():

    def __init__(self, graph):
        self.graph = graph

    def findPath(self, origin, destination):

        # If orgin or dest the same return 0
        if origin == destination:
            return [origin], 0.0
        
        # creating cost and parent graphs
        costGraph = {}
        parentGraph = {}

        for neighbor, distance in self.graph[origin].items():
            costGraph[neighbor] = distance
            parentGraph[neighbor] = origin
        
        # Initial Values for destination
        #costGraph[destination] = 
        #parentGraph[destination] = None
        
        processedNodes = []

        # Going through graph and mapping lowest cost
        # weights
        currentCheapestNode = self.cheapestCurrentNode(costGraph, processedNodes)

        while currentCheapestNode is not None:

            costToCurrentNode = costGraph[currentCheapestNode]
            
            for neighborOfCheapestNode in self.graph[currentCheapestNode]:

                if neighborOfCheapestNode != origin:

                    costToNeighbor = self.graph[currentCheapestNode][neighborOfCheapestNode]
                    testCostToNeighbor = costToCurrentNode + costToNeighbor
                    savedCostToNeighbor = None

                    # Node may not be in cost graph because its not
                    # directly connected to parent
                    try:
                        savedCostToNeighbor = costGraph[neighborOfCheapestNode]
                    except Exception:
                        savedCostToNeighbor = float("inf")

                    # Cheaper path discovered, updating cost to neigbor
                    # Updating parent to cheaper parent
                    if testCostToNeighbor < savedCostToNeighbor:
                        costGraph[neighborOfCheapestNode] = testCostToNeighbor
                        parentGraph[neighborOfCheapestNode] = currentCheapestNode

            processedNodes.append(currentCheapestNode)
            currentCheapestNode = self.cheapestCurrentNode(costGraph, processedNodes)

        # After mappings are done, return cheapest path
        cheapestPath = [destination]
        originalDestination = destination
        while True:

            try:
                cheapestPath.insert(0, parentGraph[destination])
                destination = parentGraph[destination]
            except Exception as e:
                break
        
        if costGraph[originalDestination] == float("inf"):
            print(origin, destination)
            raise ValueError("No path found!")
        
        return cheapestPath, costGraph[originalDestination]


    def cheapestCurrentNode(self, costGraph, processedNodes):

        currentLowestCostNode = float("inf")
        nameCurrentLowestNode = None

        for node in costGraph:

            if costGraph[node] < currentLowestCostNode and node not in processedNodes:
                currentLowestCostNode = costGraph[node]
                nameCurrentLowestNode = node

        return nameCurrentLowestNode
    