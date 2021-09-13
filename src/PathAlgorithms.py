from collections import deque, defaultdict
from heapq import *

class PathAlgorithmVisualizer():

    def __init__(self, grid, algorithm = "DepthFirstSearch"):

        self.grid = grid
        self.algorithm = algorithm
        #Instructions in format: Ex: {1: {(1,1):"blue", (2,2):"red", (3,3):"orange", (1,4):"blue"}, 2: {(1,2):"green"}}
        #Coloring instructions are: Orange - Searched Square, Blue - Square on Final Path, Red - Exit, Green - Entrance
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
        if self.algorithm == "Dijikstra": return self.Dijikstra()
        elif self.algorithm == "DepthFirstSearch": return self.DepthFirstSearch()
        elif self.algorithm == "Floyd-Warshall": return self.FloydWarshall()
        elif self.algorithm == "test": return self.testAlgorithm()

    def FloydWarshall(self):
        step = 0
        dist = defaultdict(lambda: dict())
        next = defaultdict(lambda: dict())
        #Initalize dist between all nodes as infinite
        for u in self.vertices:
            for v in self.vertices:
                dist[u][v] = float("inf")
                next[u][v] = v
        #Initalize paths from maze in dist
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                neighbors = filter(lambda x: x in self.vertices,
                             [(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
                for neighbor in neighbors:
                    dist[(x,y)][neighbor] = 1
        #Initialize distance from node to itself as 0
        for v in self.vertices:
            dist[v][v] = 0
            next[v][v] = v
        #Main Algorithm
        color_cycle = True
        for k in self.vertices:
            for i in self.vertices:
                for j in self.vertices:
                    if color_cycle:
                        step += 1
                        self.instructions[step] = {k: "orange", i: "orange", j: "orange", self.entrance: "green", self.exit:"red"}
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next[i][j] = next[i][k]
                color_cycle = False
        #Reconstruct Path
        step += 1
        self.instructions[step] = {}
        u, v = self.entrance, self.exit
        if not (next[u][v]): return self.instructions
        while u != v:
            u = next[u][v]
            self.instructions[step][u] = "blue"
        self.instructions[step][v] = "red"
        return self.instructions
        
    '''DepthFirst figure out why it aint blue and reset visited like currentPath'''

    def _testRecursive(self, node, visited, currentPath, prevPath, instructionPath):
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
            self._testRecursive(i, visited, copyCurrentPath, prevPath, instructionPath)

    def testAlgorithm(self):
        visited = {self.entrance}
        currentPath = []
        prevPath = []
        instructionPath = []
        self._testRecursive(self.entrance, visited, currentPath, prevPath, instructionPath)
        for i in range(len(instructionPath)):
            self.instructions[i] = instructionPath[i]
        return self.instructions

    def DepthFirstSearch(self): #Run DFS Algorithm and return coloring instructions for visualizing it
        step = 0
        q = deque([self.entrance])
        visited = set([self.entrance])
        prev = {self.entrance: None}

        while q:
            #Increment step for instructions
            step += 1
            self.instructions[step] = {}
            #Pop off node from stack and add to visited
            node = q.popleft()
            visited.add(node)

            #If exit found, color path from entrance blue and return instructions
            if node == self.exit:
                while prev[node] != None:
                    self.instructions[step][node] = "blue"
                    node = prev[node]
                self.instructions[step][self.exit] = "red"
                return self.instructions
            #Color newly visited nodes orange
            self.instructions[step][node] = "orange"
            
            #Get valid neighbors
            neighbors = filter(lambda x: x not in visited and x in self.vertices,
                             [(node[0]+1, node[1]), (node[0]-1,node[1]), (node[0], node[1]+1), (node[0], node[1]-1)])
            #Add valid neighbors to stack and to prev
            for neighbor in neighbors:
                q.appendleft(neighbor)
                prev[neighbor] = node
            #Make sure entrance stays green
            self.instructions[step][self.entrance] = "green"
        return self.instructions
                   
    def Dijikstra(self): #Run Dijikstra Algorithm and return coloring instructions for visualizing it
        step = 0
        dist = {self.entrance: 0}
        prev = {self.entrance: None}
        q = []
        heapify(q)

        for v in self.vertices:
            if v != self.entrance:
                dist[v] = float("inf")
            heappush(q, (dist[v], v))

        while q:
            #Pop off node from min-priority queue
            _,u = heappop(q)
            #Get valid neighbors
            neighbors = filter(lambda x: 0 <= x[0] <= self.bottom_edge and 0 <= x[1] <= self.right_edge and dist.get(x,0) and dist[x] == float("inf"),
                                [(u[0]+1,u[1]), (u[0]-1,u[1]), (u[0],u[1]+1), (u[0],u[1]-1)])
            #Increment Step for Instructions
            step += 1
            self.instructions[step] = {}

            for v in neighbors:
                temp = dist[u] + 1
                #Color newly visited neighbors orange
                self.instructions[step][v] = "orange"
                #If new path faster to v
                if temp < dist[v]:
                    dist[v] = temp
                    prev[v] = u
                    heappush(q, (dist[v], v))
                    #If exit found, color path to exit from entrance blue and return instructions
                    if v == self.exit:
                        while prev[v]:
                            v = prev[v]
                            self.instructions[step][v] = "blue"
                        self.instructions[step][self.entrance] = "green"
                        self.instructions[step][self.exit] = "red"
                        return self.instructions
        return self.instructions
        
    def __str__(self):
        text = ""
        for row in self.grid:
            text += str(row) + "\n"
        text += "\nAlgorithm: " + self.algorithm
        return text