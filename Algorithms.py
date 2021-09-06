from collections import deque
from heapq import *

class AlgorithmVisualizer():

    def __init__(self, grid, algorithm = "Dijikstra"):

        self.grid = grid
        self.algorithm = algorithm

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

    '''def Astar(self):
        visitedList = deque([])
        valuesList = deque([])
        currentPos = self.entrance      
        while (currentPos != self.exit):
            visitedList.append(currentPos)
            valuesList.append([currentPos[x] - visitedList))

    def DepthFirstSeach(self):
        possibleMoves = []
        possibleMoves.append(self.entrance)
        for i in range(len(self.vertices)):
            nextMove = []
            if self.vertices[i][0] == 
            '''
        

    def Dijikstra(self): 
        #Orange for searched squares, Blue for shortest path, return coloring instructions in turn order
        #Ex: {1: {(1,1):"blue", (2,2):"red", (3,3):"grey", (1,4):"blue"}}
        instructions = {}
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
            instructions[step] = {}
            for v in neighbors:
                temp = dist[u] + 1
                instructions[step][v] = "orange"
                if temp < dist[v]:
                    dist[v] = temp
                    prev[v] = u
                    heappush(q, (dist[v], v))
                    if v == self.exit:
                        while prev[v]:
                            v = prev[v]
                            instructions[step][v] = "blue"
                        instructions[step][self.entrance] = "green"
                        instructions[step][self.exit] = "red"
                        return instructions
                instructions[step][self.entrance] = "green"
                instructions[step][self.exit] = "red"
        return instructions
        
    def __str__(self):
        text = ""
        for row in self.grid:
            text += str(row) + "\n"
        text += "\nAlgorithm: " + self.algorithm
        return text