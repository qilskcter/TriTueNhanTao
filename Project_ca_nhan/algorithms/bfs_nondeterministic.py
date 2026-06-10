from collections import deque
from .base import BaseAlg

class BFS_NONDETERMINISTIC(BaseAlg):
    def __init__(self):
        super().__init__()

    def solve(self, start_state):
        frontier = deque()
        reached = set()

        frontier.append((start_state, []))
        reached.add(start_state)

        logs = []
        step = 0

        if self.is_goal(start_state[2]):
            return [], ["Goal nằm ngay tại trạng thái bắt đầu"]

        while frontier:
            current, path = frontier.popleft()
            step += 1

            logs.append(f"Bước {step} | Node hiện tại: {current}")

            x, y, ground = current
            actions_list = self.actions(x, y, ground)

            for intended_action in actions_list:
                possible_results = self.get_possible_results(current, intended_action)

                for real_action, child in possible_results:
                    logs.append(
                        f"Parent: {current} | Intended: {intended_action} | Real: {real_action} | Child: {child}"
                    )

                    if child not in reached:
                        reached.add(child)

                        if self.is_goal(child[2]):
                            logs.append("Tìm thấy goal bằng Early Goal Check")
                            return path + [real_action], logs

                        frontier.append((child, path + [real_action]))

        return None, logs

    def get_possible_results(self, state, intended_action):
        x, y, ground = state

        if intended_action == "CLEAN":
            return [("CLEAN", self.apply_action(state, "CLEAN"))]

        possible_actions = [intended_action]

        if intended_action in ["UP", "DOWN"]:
            possible_actions += ["LEFT", "RIGHT"]
        elif intended_action in ["LEFT", "RIGHT"]:
            possible_actions += ["UP", "DOWN"]

        valid_actions = self.actions(x, y, ground)
        results = []

        for act in possible_actions:
            if act in valid_actions:
                child = self.apply_action(state, act)
                results.append((act, child))

        if not results:
            results.append(("STAY", state))

        return results