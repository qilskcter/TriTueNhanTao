from heapq import heappush, heappop
from .base import BaseAlg

class AStar(BaseAlg):
    def solve(self, start_state):
        def get_h(state):
            count = 0
            current_board = state[2]
            for i in range(len(current_board)):
                for j in range(len(current_board[0])):
                    if current_board[i][j] == 1:
                        count += 1
            return count
        def get_current_inversions(state):
            flat = [val for row in state[2] for val in row if val != 0]
            inv = 0
            for i in range(len(flat)):
                for j in range(i + 1, len(flat)):
                    if flat[i] > flat[j]:
                        inv += 1
            return inv

        pq = []
        steps = 0
        start_g = get_current_inversions(start_state)
        start_f = start_g + get_h(start_state)
        heappush(pq, (start_f, start_g, steps, start_state, []))
        visited = {start_state: start_g}
        logs = []
        
        while pq:
            f_score, accumulated_g, _, state, path = heappop(pq)
            steps += 1
            logs.append(f"A* Duyệt Node #{steps} | Vị trí: ({state[0]},{state[1]}) | Cost: {accumulated_g}")
            
            if self.is_goal(state[2]):
                return path, logs
            
            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                new_g = accumulated_g + 1 + get_current_inversions(new_state)
                if new_state not in visited or new_g < visited[new_state]:
                    visited[new_state] = new_g
                    total_f = new_g + get_h(new_state)
                    heappush(pq, (total_f, new_g, steps, new_state, path + [action]))
                    
        return None, logs