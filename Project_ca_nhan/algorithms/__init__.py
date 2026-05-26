from .bfs import BFS
from .bfs_early import BFS_EARLY
from .dfs import DFS
from .dfs_early import DFS_EARLY
from .ids import IDS
from .ids_early import IDS_EARLY
from .ucs import UCS
from .greedy import Greedy
from .A_star import AStar

ALG_MAP = {
    "BFS": BFS(),
    "BFS Early": BFS_EARLY(),
    "DFS": DFS(),
    "DFS Early": DFS_EARLY(),
    "IDS": IDS(),
    "IDS Early": IDS_EARLY(),
    "UCS": UCS(),
    "Greedy": Greedy(),
    "A*": AStar(),
}