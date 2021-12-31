from collections import deque, defaultdict
from heapq import *

class PathAlgorithmVisualizer():

    def __init__(self, grid, algorithm):

        self.grid = grid
        self.algorithm = algorithm
        self.nodes_visited = 0
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
        if self.algorithm == "A*Manhattan": return self.AStarManhattan()
        elif self.algorithm == "Dijikstra": return self.Dijikstra()
        elif self.algorithm == "DepthFirstSearch": return self.DepthFirstSearch()
        elif self.algorithm == "Floyd-Warshall": return self.FloydWarshall()

    def AStarManhattan(self): #Run A* Search Algorithm with Manhattan Distance Heuristic and return coloring instructions
        step = 0
        self.instructions[step] = {}
        #Heuristic Function based on Manhattan Distance
        def ManhattanHeuristic(node):
            return abs(self.exit[1] - node[1]) + abs(self.exit[0] - node[0])
        #Initialize discovered nodes, map from node to parent, map of cost to reach node,
        #and map of estimated total path from start to finish by going through node
        q = []
        heapify(q)
        parent = dict()
        reach_cost = dict()
        total_cost = dict()
        for u in self.vertices:
            reach_cost[u] = float("inf")
            total_cost[u] = float("inf")
        reach_cost[self.entrance] = 0
        total_cost[self.entrance] = ManhattanHeuristic(self.entrance)
        heappush(q, (total_cost[self.entrance], self.entrance))
        self.nodes_visited = 1
        #While there is still nodes to go through
        while q:
            step += 1
            self.instructions[step] = {}
            #Pop min total cost node off of min-priority queue
            _, node = heappop(q)
            if node == self.exit:
                break
            #Get valid neighbors
            neighbors = filter(lambda x: x in self.vertices,
                             [(node[0]+1, node[1]), (node[0]-1,node[1]), (node[0], node[1]+1), (node[0], node[1]-1)])
            for neighbor in neighbors:
                self.instructions[step][node] = "orange"
                self.nodes_visited += 1
                new_cost = reach_cost[node] + 1
                #If the path through this node is better to reach this neighbor
                if new_cost < reach_cost[neighbor]:
                    parent[neighbor] = node
                    reach_cost[neighbor] = new_cost
                    total_cost[neighbor] = new_cost + ManhattanHeuristic(neighbor)
                    if neighbor not in q:
                        heappush(q, (total_cost[neighbor], neighbor))
            #Color all previously seen nodes orange and recalculate path
            for node in self.instructions[step-1]:
                self.instructions[step][node] = "orange"
            #Construct current shortest path to exit
            backtrack = self.exit
            if total_cost[backtrack] != float("inf"):
                while parent[backtrack] != self.entrance:
                    backtrack = parent[backtrack]
                    self.instructions[step][backtrack] = "blue"
            #Make sure entrance and exit are the right color
            self.instructions[step][self.entrance] = "green"
            self.instructions[step][self.exit] = "red"
        return self.nodes_visited, self.instructions

    def FloydWarshall(self): #Run Floyd Warshall Algorithm and return coloring instructions for visualizing it
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
                    self.nodes_visited += 1
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
        self.nodes_visited = len(self.vertices)**3
        return self.nodes_visited, self.instructions

    def DepthFirstSearch(self): #Run DFS Algorithm and return coloring instructions for visualizing it
        step = 0
        self.nodes_visited = 1
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
            self.nodes_visited += 1

            #If exit found, color path from entrance blue and return instructions
            if node == self.exit:
                while prev[node] != None:
                    self.instructions[step][node] = "blue"
                    node = prev[node]
                self.instructions[step][self.exit] = "red"
                return self.nodes_visited, self.instructions
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
        return self.nodes_visited, self.instructions
                   
    def Dijikstra(self): #Run Dijikstra Algorithm and return coloring instructions for visualizing it
        step = 0
        self.nodes_visited = 1
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
                self.nodes_visited += 1
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
                        return self.nodes_visited, self.instructions
        return self.nodes_visited, self.instructions
        
    def __str__(self):
        text = ""
        for row in self.grid:
            text += str(row) + "\n"
        text += "\nAlgorithm: " + self.algorithm
        return text