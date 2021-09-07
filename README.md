# MazeRunner
Maze Generator done using Tkinter in Python 3 with various path algorithm visualizations.

Implemented Currently:
- Manual Maze Creation
- Dijikstra Visualization
- Depth First Search Visualization
- Ability to highlight/unhighlight Maze Path blocks with Highlight Path option

Left to Implement:
- Floyd-Warshall Visualization
- Bellman-Ford Visualization
- A* Visualization with one or multiple different heuristics
- Random Maze Generation with possible Algorithm selection for generation

Run by running GUI.py with
$ python3 GUI.py

Bugs:
- Maze does not render on Windows correctly (Linux untested)
- Maze on Windows will glitch out once size of maze is set to over 20 x 20 (untested for Mac and Linux)