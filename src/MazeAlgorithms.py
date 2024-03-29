from random import shuffle, randint, choice
from SimpleDisjointSet import SimpleDisjointSet
from collections import deque

class MazeAlgorithmVisualizer():

    def __init__(self, grid_size = [10, 10], algorithm = "Random Kruskall"):

        self.grid_size = grid_size # (rows, cols)
        self.algorithm = algorithm 
        self.instructions = {}
    
    def runAlgorithm(self):
        if self.algorithm == "Random Kruskall": return self.randomKruskall()
        elif self.algorithm == "Random DFS": return self.randomizedDFS()
    
    def randomKruskall(self): #Return instructions for making maze pathway as well as location for entrance and exit of maze
        step = 0
        #Dimensions of maze must be (2n+1) by (2n+1), otherwise reformat grid as well
        if self.grid_size[0] % 2 != 1:
            self.grid_size[0] -= 1
        if self.grid_size[1] % 2 != 1:
            self.grid_size[1] -= 1
        #Create set of all edges to look over
        edges = []
        nodes = []
        for x in range(0, self.grid_size[0], 2):
            for y in range(0, self.grid_size[1], 2):
                nodes.append((x,y))
                if (x != self.grid_size[0] - 1):
                    edges.append(((x,y), (x+1,y), (x+2,y)))
                if (y != self.grid_size[1] - 1):
                    edges.append(((x,y), (x,y+1), (x,y+2)))
        shuffle(edges)
        #Create Disjoint Set
        ds = SimpleDisjointSet(nodes)
        nodes = []
        #Randomly go through all 3-edges paced 2 away from each other, if the two outer 
        # walls of edge are in same set, ignore, otherwise make all 3 path blocks grey
        for edge in edges:
            if ds.find(edge[0]) != ds.find(edge[2]):
                step += 1
                self.instructions[step] = {}
                ds.union(edge[0], edge[2]) 
                self.instructions[step][edge[0]] = "grey"
                self.instructions[step][edge[1]] = "grey"
                self.instructions[step][edge[2]] = "grey"
                nodes.append(edge[0])
                nodes.append(edge[2])
        #Choose a random entrance and exit
        shuffle(nodes)
        
        return self.instructions, nodes[0], nodes[1]
    
    def randomizedDFS(self):
        #Set correct grid boundaries
        if self.grid_size[0] % 2 != 1:
            self.grid_size[0] -= 1
        if self.grid_size[1] % 2 != 1:
            self.grid_size[1] -= 1
        #Initialize and set certain variables required for DFS algorithm
        startNode = (randint(0, self.grid_size[0]//2)*2, randint(0, self.grid_size[1]//2)*2)
        visited = set()
        visited.add(startNode)
        stack = deque()
        stack.appendleft(startNode)
        possibleExits = []
        self.instructions[0] = {startNode : "grey"}
        stepCounter = 0
        #The actual algorithm and writing the instructions
        #Algorithm was based off of wikipedia on its maze generation page
        while stack:
            currentNode = stack.popleft()
            neighbor = list(filter(lambda x: 0 <= x[0] < self.grid_size[0] and 0 <= x[1] < self.grid_size[1] and x not in visited,
            [(currentNode[0] + 2, currentNode[1]), (currentNode[0] - 2, currentNode[1]), (currentNode[0], currentNode[1] + 2), (currentNode[0], currentNode[1] - 2)]))
            if neighbor:
                stack.appendleft(currentNode)
                neighbor = choice(neighbor)
                stack.appendleft(neighbor)
                visited.add(neighbor)
                wallCell = (int((neighbor[0] + currentNode[0]) / 2), int((neighbor[1] + currentNode[1]) / 2)) 
                stepCounter += 1
                self.instructions[stepCounter] = {wallCell: "grey", neighbor: "grey"}
            else:
                possibleExits.append(currentNode)
        possibleExits.remove(startNode)
        return self.instructions, startNode, choice(possibleExits)
            