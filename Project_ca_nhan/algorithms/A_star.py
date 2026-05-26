from heapq import heappush, heappop
from .base import BaseAlg

class AStar(BaseAlg):
    def solve(self, start_state):
        # h(n): Số ô sai (số ô có bụi giá trị là 1)
        def get_h(state):
            count = 0
            current_board = state[2]
            for i in range(len(current_board)):
                for j in range(len(current_board[0])):
                    if current_board[i][j] == 1:
                        count += 1
            return count

        # Chi phí đặc trưng của trạng thái hiện tại: Số dãy ngược (Inversion Count)
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
        
        # g(n) ban đầu = Chi phí đặc trưng tại ô xuất phát (Số dãy ngược ban đầu)
        start_g = get_current_inversions(start_state)
        # f(n) = g(n) + h(n)
        start_f = start_g + get_h(start_state)
        
        # Priority Queue lưu tuple: (f_score, g_score, thứ_tự_chèn, state, path)
        heappush(pq, (start_f, start_g, steps, start_state, []))
        
        # visited dạng dictionary để lưu { trạng_thái: chi_phí_g_tích_lũy_nhỏ_nhất }
        visited = {start_state: start_g}
        logs = []
        
        while pq:
            f_score, accumulated_g, _, state, path = heappop(pq)
            steps += 1
            
            # Chi phí Cost hiển thị chính là tổng chi phí tích lũy g(n) tăng tiến liên tục
            logs.append(f"A* Duyệt Node #{steps} | Vị trí: ({state[0]},{state[1]}) | Cost: {accumulated_g}")
            
            if self.is_goal(state[2]):
                return path, logs
            
            for action in self.actions(state[0], state[1], state[2]):
                new_state = self.apply_action(state, action)
                
                # Quy tắc cộng dồn: 
                # Chi phí node tiếp theo = Tổng chi phí tích lũy node trước (accumulated_g) 
                #                          + 1 (chi phí cho hành động di chuyển) 
                #                          + chi phí ô hiện tại (số dãy ngược mới)
                new_g = accumulated_g + 1 + get_current_inversions(new_state)
                
                # Nếu trạng thái chưa được duyệt, hoặc tìm thấy đường đi có tổng chi phí g nhỏ hơn
                if new_state not in visited or new_g < visited[new_state]:
                    visited[new_state] = new_g
                    
                    # Hàm đánh giá tổng hợp f(n) = g(n)_tích_lũy + h(n)_ô_sai
                    total_f = new_g + get_h(new_state)
                    heappush(pq, (total_f, new_g, steps, new_state, path + [action]))
                    
        return None, logs