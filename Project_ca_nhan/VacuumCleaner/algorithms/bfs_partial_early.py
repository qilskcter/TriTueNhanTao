from collections import deque
from .base import BaseAlg

class BFS_PARTIAL_EARLY(BaseAlg):
    def __init__(self):
        super().__init__()
        self.start_state_used = None

    def solve(self, start_state):
        self.start_state_used = None

        S1 = start_state
        S2 = self.create_second_start(start_state)

        frontier = deque()
        reached = set()
        parent = {}
        action = {}
        source = {}

        for label, state in [("S1", S1), ("S2", S2)]:
            if state not in reached:
                frontier.append(state)
                reached.add(state)
                parent[state] = None
                action[state] = None
                source[state] = label

                if self.is_goal(state[2]):
                    self.start_state_used = state
                    return [], [f"Goal nằm ngay tại {label}"]

        logs = []
        step = 0

        while frontier:
            current = frontier.popleft()
            step += 1

            logs.append(f"Bước {step} | Đang xét {source[current]} | Node: {current}")

            x, y, ground = current
            actions_list = self.actions(x, y, ground)

            for act in actions_list:
                child = self.apply_action(current, act)

                if child not in reached:
                    reached.add(child)
                    parent[child] = current
                    action[child] = act
                    source[child] = source[current]

                    logs.append(
                        f"Parent: {current} | Action: {act} | Child: {child}"
                    )

                    if self.is_goal(child[2]):
                        logs.append(
                            f"Tìm thấy goal bằng Early Goal Check từ {source[child]}"
                        )

                        self.start_state_used = self.find_start(child, parent)

                        return self.build_path(child, parent, action), logs

                    frontier.append(child)

        self.start_state_used = S1
        return None, logs

    def create_second_start(self, start_state):
        x, y, ground = start_state
        actions_list = self.actions(x, y, ground)

        for act in actions_list:
            if act != "CLEAN":
                return self.apply_action(start_state, act)

        return start_state

    def find_start(self, node, parent):
        while parent[node] is not None:
            node = parent[node]

        return node

    def build_path(self, goal, parent, action):
        path = []
        node = goal

        while parent[node] is not None:
            path.append(action[node])
            node = parent[node]

        path.reverse()
        return path