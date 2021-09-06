import tkinter as tk
from tkinter.constants import ANCHOR
from Algorithms import AlgorithmVisualizer
import time

class MazeGrid():

    def __init__(self):
        
        #Create Tkinter Window
        self.root = tk.Tk()
        self.root.wm_title("Mazes Am I Right?")
        self.main_frame = tk.Frame(self.root, width = 600, height = 400)
        self.main_frame.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.maze_frame = tk.Frame(self.main_frame, width = 400, height = 400)
        self.maze_frame.grid(row = 0, column = 0, padx = 5, pady = 5)

        #Init variables
        self.grid_rows = tk.IntVar(self.root, value=10)
        self.grid_cols = tk.IntVar(self.root, value=10)
        self.maze_data = {}
        self.place_maze_object = tk.StringVar(self.root, value = "Maze Path")
        self.use_algorithm = tk.StringVar(self.root, value = "Dijikstra")
        self.num_entrances = 0
        self.num_exits = 0
        self.algorithm_running = 0

        #Create frame on side for selecting grid size
        self.side_frame = tk.Frame(self.main_frame, width = 200, height = 400)
        self.side_frame.grid(row = 0, column = 1, padx = 5, pady = 5)

        self.row_entry_label = tk.Label(self.side_frame, text="Number of Rows: ")
        self.row_entry_label.grid(row = 0, column = 1)
        self.row_entry = tk.Entry(self.side_frame, textvariable=self.grid_rows)
        self.row_entry.grid(row = 0, column = 2)
        
        self.column_entry_label = tk.Label(self.side_frame, text="Number of Columns: ")
        self.column_entry_label.grid(row = 1, column = 1)
        self.column_entry = tk.Entry(self.side_frame, textvariable=self.grid_cols)
        self.column_entry.grid(row = 1, column = 2)

        self.set_grid = tk.Button(self.side_frame, text = "Set Grid/Reset", command = self.initGrid)
        self.set_grid.grid(row = 2, column = 2)
        
        self.maze_object_selector = tk.OptionMenu(self.side_frame, self.place_maze_object, "Maze Path", "Maze Wall", "Entrance", "Exit")
        self.maze_object_selector.grid(row = 5, column = 2)

        self.algorithm_selector  = tk.OptionMenu(self.side_frame, self.use_algorithm, "Dijikstra")
        self.algorithm_selector.grid(row = 7, column = 2)

        self.run_button = tk.Button(self.side_frame, text="Run Algorithm", command = self.visualizeAlgorithm) 
        self.run_button.grid(row = 8, column = 2)
        
    def visualizeAlgorithm(self): #Create AlgorithmVisualizer instance and run algorithm
        #Make sure there's an entrance and exit in maze
        if self.num_entrances != 1 or self.num_exits != 1: return -1
        #Make sure an algorithm isn't running already
        if self.algorithm_running: return -1
        else: self.algorithm_running = 1
        #Create 2D-Array representing maze and remove previous algorithm trails
        maze = []
        translateColor = {
            "black": 1,       #wall
            "grey": 0,        #path
            "orange": 0,
            "blue": 0,
            "red": 2,         #exit
            "green": 3        #entrance
        }
        for x in range(self.grid_rows.get()):
            row = []
            for y in range(self.grid_cols.get()):
                if self.maze_data[(x,y)].cget("bg") in ["blue", "orange"]:
                    self.maze_data[(x,y)].configure(highlightbackground = "grey", bg = "grey")
                row.append(translateColor[self.maze_data[(x,y)].cget("bg")])
            maze.append(row)
        self.root.update()
        #Create instance of AlgorithmVisualizer
        visual = AlgorithmVisualizer(maze, self.use_algorithm.get())
        instructions = visual.runAlgorithm()
        #Visualize Algorithm
        for step in instructions:
            for square in instructions[step]:
                self.maze_data[square].configure(highlightbackground = instructions[step][square], bg = instructions[step][square])
            self.root.update()
            time.sleep(.1)
        #End Algorithm
        self.algorithm_running = 0

    def initGrid(self): #Initialize maze_frame grid using size select options
        #Make sure algorithm isn't already running
        if self.algorithm_running: return -1
        #Reset init vars
        self.num_exits = 0
        self.num_entrances = 0
        #Destroy old maze cells
        for widget in self.maze_frame.winfo_children():
            widget.destroy()
        self.maze_data = {}
        #Create maze cells
        for x in range(self.grid_rows.get()):
            for y in range(self.grid_cols.get()):
                self.maze_data[(x,y)] = tk.Button(self.maze_frame, highlightbackground = "grey", bg = "grey", command = lambda row = x, col = y: self.gridSquareColor(row, col))
                self.maze_data[(x,y)].grid(row = x, column = y)
        self.root.update()

    def gridSquareColor(self, x, y): #Change color of button based of maze_object_selector
        colors = {
            "Maze Wall": "black",
            "Exit": "red",
            "Entrance": "green",
            "Maze Path": "grey",
        }
        current_color = self.maze_data[(x,y)].cget("bg") #Color of button before change
        change_color = colors[self.place_maze_object.get()] #Color of button to change to

        #If there will be more than 1 exit or entrances after color change, don't change
        self.num_entrances += (change_color == "green") - (current_color == "green")
        self.num_exits += (change_color == "red") - (current_color == "red")
        if (self.num_entrances <= 1 and self.num_exits <= 1):
            self.maze_data[(x,y)].configure(highlightbackground = change_color, bg = change_color)
            self.root.update()
        else:
            self.num_entrances -= ((change_color == "green") - (current_color == "green"))
            self.num_exits -= ((change_color == "red") - (current_color == "red"))

if __name__ == '__main__':
    gui = MazeGrid()
    gui.root.mainloop()