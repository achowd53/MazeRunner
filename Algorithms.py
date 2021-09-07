from collections import deque
from heapq import *

class AlgorithmVisualizer():

    def __init__(self, grid, algorithm = "DepthFirstSearch"):

        self.grid = grid
        self.algorithm = algorithm
        self.instructions = {}

        #Find Entrance, Exit, and Travellable Spaces (Vertices)
        self.entrance = None
        self.exit = None
        self.vertices = set() #(row, col)
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if self.grid[x][y] == 3:
                    self.entrance = (x,y)
                    self.vertices.add((x,y))
                elif self.grid[x][y] == 2:
                    self.exit = (x,y)
                    self.vertices.add((x,y))
                elif self.grid[x][y] == 0:
                    self.vertices.add((x,y))
        self.right_edge = len(grid[0]) - 1
        self.bottom_edge = len(grid) - 1

    def runAlgorithm(self):
        if self.algorithm == "A*": return self.Astar()
        elif self.algorithm == "Dijikstra": return self.Dijikstra()
        elif self.algorithm == "DepthFirstSearch": return self.DepthFirstSearch()
        elif self.algorithm == "iterDFS": return self.iterativeDFS()

    '''def Astar(self):
        visitedList = deque([])
        valuesList = deque([])
        currentPos = self.entrance      
        while (currentPos != self.exit):
            visitedList.append(currentPos)
            valuesList.append([currentPos[x] - visitedList))'''

    '''DepthFirst figure out why it aint blue and reset visited like currentPath'''
    '''instructions on GUI.py is commented out so i can run the actual thing.'''

    def _DFSRecursive(self, node, visited, currentPath, prevPath, instructionPath):
        if (node == self.exit):
            print("finished: node is " + str(node[0]) + " " + str(node[1]))
            if len(prevPath) == 0 or len(prevPath) > len(currentPath):
                for i in prevPath:
                    for j in range(len(instructionPath)):
                        if instructionPath[j] == i:
                            instructionPath[j][i] = "orange"
                prevPath = currentPath
                for i in prevPath:
                    for j in range(len(instructionPath)):
                        if instructionPath[j] == i:
                            instructionPath[j][i] = "blue"
            return None
        nodeChildren = []
        if node != self.entrance:
            currentPath.append(node)
        for neighbor in [(node[0]+1, node[1]), (node[0]-1,node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
            if neighbor in self.vertices and neighbor not in visited:
                nodeChildren.append(neighbor)
                visited.add(neighbor)
                if neighbor != self.exit:
                    instructionPath.append({neighbor: "orange"})
        copyCurrentPath = currentPath
        for i in nodeChildren:
            self._DFSRecursive(i, visited, copyCurrentPath, prevPath, instructionPath)

    def DepthFirstSearch(self):
        visited = {self.entrance}
        currentPath = []
        prevPath = []
        instructionPath = []
        self._DFSRecursive(self.entrance, visited, currentPath, prevPath, instructionPath)
        for i in range(len(instructionPath)):
            self.instructions[i] = instructionPath[i]
        return self.instructions

    def iterativeDFS(self): #Is not shortest path
        step = 0
        q = deque([self.entrance])
        visited = set([self.entrance])
        prev = {self.entrance: None}
        while q:
            step += 1
            self.instructions[step] = {}
            node = q.popleft()
            for neighbor in [(node[0]+1, node[1]), (node[0]-1,node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
                if neighbor not in visited and neighbor in visited:
                    visited.add(neighbor)
                    prev[neighbor] = node
                    q.appendleft(neighbor)
                    self.instructions[step][self.exit] = "orange"
                    if neighbor == self.exit:
                        while prev[node] != None:
                            self.instructions[step][node] = "blue"
                            node = prev[node]
                        return self.instructions
            self.instructions[step][self.exit] = "red"
        return self.instructions
                   
    def Dijikstra(self): 
        #Orange for searched squares, Blue for shortest path, return coloring instructions in turn order
        #Ex: {1: {(1,1):"blue", (2,2):"red", (3,3):"grey", (1,4):"blue"}, 2: {(1,2)}}
        step = 0
        #Dijikstra Algorithm
        dist = {self.entrance: 0}
        prev = {}
        q = []
        heapify(q)
        for v in self.vertices:
            if v != self.entrance:
                dist[v] = float("inf")
            prev[v] = None
            heappush(q, (dist[v], v))
        while q:
            _,u = heappop(q)
            neighbors = filter(lambda x: 0 <= x[0] <= self.bottom_edge and 0 <= x[1] <= self.right_edge and dist.get(x,0) and dist[x] == float("inf"),
                                [(u[0]+1,u[1]), (u[0]-1,u[1]), (u[0],u[1]+1), (u[0],u[1]-1)])
            step += 1
            self.instructions[step] = {}
            for v in neighbors:
                temp = dist[u] + 1
                self.instructions[step][v] = "orange"
                if temp < dist[v]:
                    dist[v] = temp
                    prev[v] = u
                    heappush(q, (dist[v], v))
                    #If you found the exit, color path to exit from entrance blue and return instructions
                    if v == self.exit:
                        while prev[v]:
                            v = prev[v]
                            self.instructions[step][v] = "blue"
                        self.instructions[step][self.entrance] = "green"
                        self.instructions[step][self.exit] = "red"
                        return self.instructions
                self.instructions[step][self.entrance] = "green"
                self.instructions[step][self.exit] = "red"
        return self.instructions
        
    def __str__(self):
        text = ""
        for row in self.grid:
            text += str(row) + "\n"
        text += "\nAlgorithm: " + self.algorithm
        return text