from .bfs import BFS
from .bfs_early import BFS_EARLY
from .dfs import DFS
from .dfs_early import DFS_EARLY

ALG_MAP = {
    "BFS": BFS(),
    "BFS Early": BFS_EARLY(),
    "DFS": DFS(),
    "DFS Early": DFS_EARLY()
}