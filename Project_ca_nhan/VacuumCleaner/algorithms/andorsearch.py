from .base import BaseAlg

class AndOrSearch(BaseAlg):
    def solve(self, start_state):
        logs = []
        plan = self.or_search(start_state, [], logs)

        if plan == "failure":
            return None, logs

        path = self.flatten_plan(plan)
        return path, logs

    def or_search(self, state, path, logs):
        logs.append(f"OR: {state[0]}, {state[1]}")

        if self.is_goal(state[2]):
            return []

        if state in path:
            return "failure"

        for action in self.actions(state[0], state[1], state[2]):
            next_state = self.apply_action(state, action)
            plan = self.and_search([next_state], path + [state], logs)

            if plan != "failure":
                return [action, plan]

        return "failure"

    def and_search(self, states, path, logs):
        plans = {}

        for state in states:
            logs.append(f"AND: {state[0]}, {state[1]}")
            plan = self.or_search(state, path, logs)

            if plan == "failure":
                return "failure"

            plans[state] = plan

        return plans

    def flatten_plan(self, plan):
        result = []

        if plan == []:
            return result

        action = plan[0]
        sub_plan = plan[1]

        result.append(action)

        if isinstance(sub_plan, dict):
            for p in sub_plan.values():
                result.extend(self.flatten_plan(p))

        return result