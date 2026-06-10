from collections import deque
from .base import BaseAlg

class BFS_UNOBSERVABLE(BaseAlg):
    def solve(self, start_state):
        frontier = deque()
        reached = set()

        frontier.append((start_state, []))
        reached.add(start_state)

        logs = []
        step = 0

        while frontier:
            current, path = frontier.popleft()
            step += 1

            logs.append(f"Bước {step} | Node hiện tại: {current}")

            if self.is_goal(current[2]):
                logs.append("Tìm thấy goal trong môi trường không nhìn thấy")
                return path, logs

            x, y, ground = current
            actions_list = self.actions(x, y, ground)

            for act in actions_list:
                child = self.apply_action(current, act)

                if child not in reached:
                    reached.add(child)

                    logs.append(
                        f"Parent: {current} | Action: {act} | Child: {child}"
                    )

                    if self.is_goal(child[2]):
                        logs.append("Tìm thấy goal bằng Early Goal Check")
                        return path + [act], logs

                    frontier.append((child, path + [act]))

        return None, logs