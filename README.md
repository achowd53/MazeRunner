# MazeRunner
Maze Generator done using Tkinter in Python 3 with various path algorithm visualizations. Currently, tested to work/look best on macOS dark mode.

Implemented Currently:
- Manual Maze Creation
- Dijikstra Visualization
- Depth First Search Visualization
- Floyd-Warshall Visualization
- A* Visualization with Manhattan Distance heuristic
- Randomized Kruskall's Algorithm for Maze Generation
- Randomized DFS Algorithm for Maze Generation
- Ability to highlight/unhighlight Maze Path blocks with Highlight Path option
- Time to taken to run algorithms to obtain visualization instructions
- Number of nodes visited including repeats throughout algorithms

Left to Implement:
- Bellman-Ford Visualization
- More Random Maze Generation Algorithms

Run by running GUI.py with $ python3 src/GUI.py

Bugs:
- Maze does not render on Windows correctly (Linux untested)
- Maze on Windows will glitch out once size of maze is set to over 20 x 20 (untested for Linux)
- Maze does not render on macOS light mode correctly (rather it looks terrible)
- Count of nodes visited may be slightly off