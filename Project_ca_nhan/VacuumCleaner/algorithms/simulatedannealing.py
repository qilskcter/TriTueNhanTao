import math
import random
from .base import BaseAlg

class SimulatedAnnealing(BaseAlg):
    def __init__(self, T0=100.0, Tmin=0.1, alpha=0.95):
        self.T0 = T0
        self.Tmin = Tmin
        self.alpha = alpha
    def solve(self, start_state):
        current_state = start_state
        path = []
        algorithm_logs = []
        step_counter = 0
        T = self.T0
        while T > self.Tmin:
            step_counter += 1
            if self.is_goal(current_state[2]):
                return path, algorithm_logs
            actions_list = self.actions(current_state[0], current_state[1], current_state[2])
            if not actions_list:
                break
            action = random.choice(actions_list)
            next_state = self.apply_action(current_state, action)
            delta = self.count_dirt(next_state) - self.count_dirt(current_state)
            if delta < 0:
                current_state = next_state
                path.append(action)
            else:
                p = math.exp(-delta / T)
                if random.random() < p:
                    current_state = next_state
                    path.append(action)
            best_h = self.count_dirt(current_state)
            algorithm_logs.append(f"Bước {step_counter} | T: {T:.2f} | Best H: {best_h}")
            T = self.alpha * T
        return path, algorithm_logs

    def count_dirt(self, state):
        return sum(row.count(1) for row in state[2])