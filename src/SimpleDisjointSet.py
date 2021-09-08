class SimpleDisjointSet(): #Simple Disjoint Set Data Structure
    
    def __init__(self, nodes):
        self.prev = {} #Keep track of parent of nodes
        for node in nodes:
            self.prev[node] = node
    
    def find(self, node): #Return root of Set
        if self.prev[node] == node: return node
        return self.find(self.prev[node])

    def union(self, nodeA, nodeB): #Combine the sets containing two nodes
        nodeA = self.find(nodeA)
        nodeB = self.find(nodeB)
        self.prev[nodeB] = nodeA