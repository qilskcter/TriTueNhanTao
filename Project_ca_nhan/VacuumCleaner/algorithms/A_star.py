from heapq import heappush, heappop
from .base import BaseAlg

class AStar(BaseAlg):
    def solve(self, start_state):
        def count_dirt(state):
            dirt_count = 0
            grid = state[2]
            for row in range(len(grid)):
                for col in range(len(grid[0])):
                    if grid[row][col] == 1:
                        dirt_count = dirt_count + 1
            return dirt_count
        priority_queue = []
        step_counter = 0
        start_g_cost = 0
        start_h_cost = count_dirt(start_state)
        start_f_cost = start_g_cost + start_h_cost
        heappush(priority_queue, (start_f_cost, start_g_cost, step_counter, start_state, []))
        visited_nodes = {}
        visited_nodes[start_state] = start_g_cost
        algorithm_logs = []
        
        while len(priority_queue) > 0:
            current_node = heappop(priority_queue)
            f_cost = current_node[0]
            g_cost = current_node[1]
            state = current_node[3]
            path = current_node[4]
            step_counter = step_counter + 1
            log_message = f"A* Duyệt Node #{step_counter} | Vị trí: ({state[0]},{state[1]}) | Cost G: {g_cost}"
            algorithm_logs.append(log_message)
            if self.is_goal(state[2]):
                return path, algorithm_logs
            all_actions = self.actions(state[0], state[1], state[2])
            for action in all_actions:
                next_state = self.apply_action(state, action)
                next_g_cost = g_cost + 1
                if next_state not in visited_nodes or next_g_cost < visited_nodes[next_state]:
                    visited_nodes[next_state] = next_g_cost
                    next_h_cost = count_dirt(next_state)
                    next_f_cost = next_g_cost + next_h_cost
                    next_path = path + [action]
                    heappush(priority_queue, (next_f_cost, next_g_cost, step_counter, next_state, next_path))
                    
        return None, algorithm_logs