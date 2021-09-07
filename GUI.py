import tkinter as tk
from tkinter.constants import ANCHOR
from Algorithms import AlgorithmVisualizer
import time

class MazeGrid():

    def __init__(self):
        
        #Create Tkinter Window
        self.root = tk.Tk()
        self.root.wm_title("Mazes Am I Right?")

        self.main_frame = tk.Frame(self.root, width = 610, height = 400, borderwidth = 5, highlightbackground = "black")
        self.main_frame.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.main_frame.pack_propagate(0)

        self.maze_frame = tk.Frame(self.main_frame, width = 400, height = 400)
        self.maze_frame.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.maze_frame.pack_propagate(0)

        #Init variables
        self.grid_rows = tk.IntVar(self.root, value=10)
        self.grid_cols = tk.IntVar(self.root, value=10)
        self.maze_data = {}
        self.place_maze_object = tk.StringVar(self.root, value = "Maze Wall")
        self.use_path_algorithm = tk.StringVar(self.root, value = "Dijikstra")
        self.use_maze_algorithm = tk.StringVar(self.root, value = "Random Kruskall")
        self.num_entrances = 0
        self.num_exits = 0
        self.algorithm_running = 0

        #Create general frame on side
        self.side_frame = tk.Frame(self.main_frame, width = 200, height = 400)
        self.side_frame.grid(row = 0, column = 1, padx = 5)

        #Create frame on side for selecting grid size and creating/resetting grid
        self.grid_size_frame = tk.Frame(self.side_frame, width = 200, height = 133)
        self.grid_size_frame.grid(row = 0, column = 0)
        self.grid_size_frame.pack_propagate(0)

        tk.Label(self.grid_size_frame, text = " "*19+"Grid Creator"+" "*19, font = "Helvetica 12 bold underline").grid(row = 0, column = 0, columnspan = 2, pady=5)

        self.row_entry_label = tk.Label(self.grid_size_frame, text = "       Number of Rows: ", font = "Helvetica 10")
        self.row_entry_label.grid(row = 1, column = 0)
        self.row_entry = tk.Entry(self.grid_size_frame, textvariable=self.grid_rows)
        self.row_entry.grid(row = 1, column = 1)
        
        self.column_entry_label = tk.Label(self.grid_size_frame, text = "   Number of Columns: ", font = "Helvetica 10")
        self.column_entry_label.grid(row = 2, column = 0)
        self.column_entry = tk.Entry(self.grid_size_frame, textvariable=self.grid_cols)
        self.column_entry.grid(row = 2, column = 1)

        self.set_grid = tk.Button(self.grid_size_frame, text = "Set Grid/Reset", command = self.initGrid)
        self.set_grid.grid(row = 3, column = 1)

        #Create frame on side for maze generation
        self.maze_generator_frame = tk.Frame(self.side_frame, width = 200, height = 133)
        self.maze_generator_frame.grid(row = 2, column = 0)
        self.maze_generator_frame.pack_propagate(0)

        tk.Label(self.maze_generator_frame, text = " "*17+"Maze Generator"+" "*17, font = "Helvetica 12 bold underline").grid(row = 0, column = 0, columnspan = 2)

        self.maze_object_selector = tk.Label(self.maze_generator_frame,text = " "*18+"Maze Object: ", font = "Helvetica 11")
        self.maze_object_selector.grid(row = 1, column = 0)
        self.maze_object_selector = tk.OptionMenu(self.maze_generator_frame, self.place_maze_object, "Maze Wall", "Entrance", "Exit", "Highlight Path", "Maze Path")
        self.maze_object_selector.grid(row = 1, column = 1)

        self.maze_generator_selector_label = tk.Label(self.maze_generator_frame, text = " "*14+"Maze Algorithm: ", font = "Helvetica 11")
        self.maze_generator_selector_label.grid(row = 2, column = 0)
        self.maze_generator_selector = tk.OptionMenu(self.maze_generator_frame, self.use_maze_algorithm, "Random Kruskall")
        self.maze_generator_selector.grid(row = 2, column = 1)

        self.maze_generator_button = tk.Button(self.maze_generator_frame, text="Run Algorithm") 
        self.maze_generator_button.grid(row = 3, column = 0, columnspan = 2)

        #Create frame on side for path algorithm selection, running, and clearing visualized path
        self.path_algorithm_frame = tk.Frame(self.side_frame, width = 200, height = 133)
        self.path_algorithm_frame.grid(row = 1, column = 0)
        self.path_algorithm_frame.pack_propagate(0)

        tk.Label(self.path_algorithm_frame, text = " "*9+"Algorithm Visualization"+" "*9, font = "Helvetica 12 bold underline").grid(row = 0, column = 0, columnspan = 2)

        self.algorithm_selector_label = tk.Label(self.path_algorithm_frame, text = " "*14+"Path Algorithm: ", font = "Helvetica 11")
        self.algorithm_selector_label.grid(row = 1, column = 0)
        self.algorithm_selector = tk.OptionMenu(self.path_algorithm_frame, self.use_path_algorithm, "Dijikstra", "DepthFirstSearch", "test")
        self.algorithm_selector.grid(row = 1, column = 1)

        tk.Label(self.path_algorithm_frame, font = "Helvetica 3").grid(row = 2, column = 0, columnspan = 2)

        self.run_button = tk.Button(self.path_algorithm_frame, text="Run Algorithm", command = self.visualizeAlgorithm) 
        self.run_button.grid(row = 3, column = 0, columnspan = 2)

        self.clear_path = tk.Button(self.path_algorithm_frame, text="Clear Visualized Path", command = self.clearVisualizedPath)
        self.clear_path.grid(row = 4, column = 0, columnspan = 2)
        
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
            "violet": 0,
            "red": 2,         #exit
            "green": 3        #entrance
        }
        for x in range(self.grid_rows.get()):
            row = []
            for y in range(self.grid_cols.get()):
                if self.maze_data[(x,y)].cget("bg") not in ["grey", "red", "green", "black"]:
                    self.maze_data[(x,y)].configure(highlightbackground = "grey", bg = "grey")
                row.append(translateColor[self.maze_data[(x,y)].cget("bg")])
            maze.append(row)
        self.root.update()
        #Create instance of AlgorithmVisualizer
        visual = AlgorithmVisualizer(maze, self.use_path_algorithm.get())
        instructions = visual.runAlgorithm()
        #Visualize Algorithm
        for step in instructions:
            for square in instructions[step]:
                self.maze_data[square].configure(highlightbackground = instructions[step][square], bg = instructions[step][square])
            self.root.update()
            time.sleep(.1)
        #End Algorithm
        self.algorithm_running = 0

    def clearVisualizedPath(self): #Clear visualized path from algorithm visualizer
        if self.algorithm_running: return -1

        for x in range(self.grid_rows.get()):
            for y in range(self.grid_cols.get()):
                if self.maze_data[(x,y)].cget("bg") not in ["grey", "red", "green", "black"]:
                    self.maze_data[(x,y)].configure(highlightbackground = "grey", bg = "grey")
        self.root.update()

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
        if self.algorithm_running: return -1

        colors = {
            "Maze Wall": "black",
            "Exit": "red",
            "Entrance": "green",
            "Maze Path": "grey",
            "Highlight Path": "violet"
        }
        current_color = self.maze_data[(x,y)].cget("bg") #Color of button before change
        change_color = colors[self.place_maze_object.get()] #Color of button to change to
        
        #Only allow highlight path to highlight/unhighlight maze walls
        if (change_color == "violet"):
            if current_color in ["orange", "blue", "grey", "violet"]: pass
            else: return 0

        #If there will be more than 1 exit or entrances after color change, don't change
        if self.num_entrances == 1 and change_color == "green" and current_color != "green": return 0
        if self.num_exits == 1 and change_color == "red" and current_color != "red": return 0

        if current_color == "green": self.num_entrances -= 1
        elif current_color == "red": self.num_exits -= 1
        if (current_color == change_color): #If trying to change a block to the same thing as before, unselect block to path instead
            self.maze_data[(x,y)].configure(highlightbackground = "grey", bg = "grey")
        else:
            if change_color == "green": self.num_entrances += 1
            elif change_color == "red": self.num_exits += 1
            self.maze_data[(x,y)].configure(highlightbackground = change_color, bg = change_color)
        self.root.update()

if __name__ == '__main__':
    gui = MazeGrid()
    gui.root.mainloop()