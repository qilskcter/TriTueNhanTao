# <center>Vacuum Cleaner Visualizer</center>

![Python](https://img.shields.io/badge/Python-3.9.6-3776AB?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-355938?logo=pygame&logoColor=white)
![Status](https://img.shields.io/badge/Status-UPDATING-yellow)

## Github Link

[Artificial Intelligence - Nguyen Dinh Khanh](https://github.com/qilskcter/TriTueNhanTao)

## Supported Algorithms

1. Uninformed Search

-  [BFS (Breadth-First Search)](./algorithms/bfs.py)
-  [BFS Early Goal Check](./algorithms/bfs_early.py)
-  [DFS (Depth-First Search)](./algorithms/dfs.py)
-  [DFS Early Goal Check](./algorithms/dfs_early.py)
-  [IDS (Iterative Deepening Search)](./algorithms/ids.py)
-  [IDS Early Goal Check](./algorithms/ids_early.py)
-  [UCS (Uniform Cost Search)](./algorithms/ucs.py)

2. Informed Search

-  [Greedy](./algorithms/greedy.py)
-  [A* (A-star)](./algorithms/A_star.py)
-  [IDA* (IDA-star)](./algorithms/ida_star.py)

3. Local Search

-  [Simple Hill Climbing](./algorithms/simplehillclimbing.py)
-  [Steepest Ascent Hill Climbing](./algorithms/steepestascenthillclimbing.py)
-  [Stochastic Hill Climbing](./algorithms/stochastichillclimbing.py)
-  [Random Restart Hill Climbing](./algorithms/randomrestarthillclimbing.py)
-  [Local Beam Search](./algorithms/localbeamsearch.py)
-  [Simulate Dannealing](./algorithms/simulatedannealing.py)

4. Search in Complex Environments

-  [Search in Partially Observable Environments](./algorithms/bfs_partial_early.py)
-  [Search in Unobservable Environments](./algorithms/bfs_unobservable.py)
-  [Search in Nondeterministic Environments](./algorithms/bfs_nondeterministic.py)
## Requirements

- Python 3.8+
- Pygame

> [!WARNING]
> ### Python & Pygame Compatibility Note
> Running this project with an experimental or too high Python version (e.g., **Python 3.14+**) may cause Pygame to behave unexpectedly or fail to render the graphical interface properly due to library compatibility issues.
> 
> To ensure a smooth and stable simulation, it is highly recommended to use:
> - **Python:** `3.8` up to `3.12`
> - **Pygame:** `2.5.0` or higher
> 
> If you encounter any initialization or rendering errors, please verify your Python version using `python --version` and consider downgrading to a stable release.

## Project Structure

```
Project_ca_nhan
├── Assets
│   ├── demo.gif
│   ├── dirt.png
│   ├── obstacle.png
│   └── robot.png
├── LinkGithub.txt
├── README.md
├── algorithms
│   ├── A_star.py
│   ├── __init__.py
│   ├── base.py
│   ├── bfs.py
│   ├── bfs_early.py
│   ├── bfs_partial_early.py
│   ├── dfs.py
│   ├── dfs_early.py
│   ├── greedy.py
│   ├── ida_star.py
│   ├── ids.py
│   ├── ids_early.py
│   ├── localbeamsearch.py
│   ├── randomrestarthillclimbing.py
│   ├── simplehillclimbing.py
│   ├── simulatedannealing.py
│   ├── steepestascenthillclimbing.py
│   ├── stochastichillclimbing.py
│   └── ucs.py
└── main.py
```

## Demo 
![demo](Assets/demo.gif)

## Installation & Running

1. Clone the repository:

```bash
git clone https://github.com/qilskcter/TriTueNhanTao.git
cd TriTueNhanTao
```

2. Install dependencies:

```bash
pip3 install pygame
```

3. Run the application:

```bash
python3 main.py
```

## How to Use

- **Change Grid Size:** Click on the `M` (Rows) or `N` (Columns) text boxes, type a number (from 2 to 6), and press `Enter` to resize the map.
- **Draw Obstacles:** Left-click on any empty grid cell to place a gray obstacle (wall). Click again to remove it. *(Note: You cannot place an obstacle on the robot's starting position at (0,0)).*
- **Generate Dirt:** Click the `RANDOM BUI` button to randomly scatter dirt particles across the map with a 40% probability.
- **Select Algorithm:** Click the dropdown menu in the top-left corner to choose one of the supported search algorithms.
- **Run Simulation:** Click the green `RUN` button to execute the algorithm. The path visualizer will show the logs in real-time, and the robot will start moving to clean the grid.