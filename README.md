# MazeRunner
Maze Generator done using Tkinter in Python 3 with various path algorithm visualizations. Currently, tested to work best on macOS 11 dark mode.

Implemented Currently:
- Manual Maze Creation
- Dijikstra Visualization
- Depth First Search Visualization
- Floyd-Warshall Visualization
- Randomized Kruskall's Algorithm for Maze Generation
- Randomized DFS Algorithm for Maze Generation
- Ability to highlight/unhighlight Maze Path blocks with Highlight Path option

Left to Implement:
- Bellman-Ford Visualization
- A* Visualization with one or multiple different heuristics
- More Random Maze Generation Algorithms

Run by running GUI.py with $ python3 src/GUI.py

Bugs:
- Maze does not render on Windows correctly (Linux untested)
- Maze on Windows will glitch out once size of maze is set to over 20 x 20 (untested for Linux)
- Maze does not render on macOS light mode correctly (rather it looks terrible)