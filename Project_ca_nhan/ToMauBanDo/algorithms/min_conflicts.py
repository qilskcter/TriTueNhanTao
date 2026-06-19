import random


class MinConflictsSolver:
    def __init__(self, ward_count, ward_names, neighbors, max_steps=1000):
        self.ward_count = ward_count
        self.ward_names = ward_names
        self.neighbors = neighbors
        self.max_steps = max_steps
        self.assignment = {}
        self.colors = ["red", "lime", "blue", "yellow"]

    def initial_assignment(self):
        self.assignment = {
            i: random.choice(self.colors)
            for i in range(self.ward_count)
        }

    def get_conflicts(self, ward_index, color):
        count = 0

        for neighbor in self.neighbors[ward_index]:
            if self.assignment.get(neighbor) == color:
                count += 1

        return count

    def get_conflicted_variables(self):
        conflicted = []

        for i in range(self.ward_count):
            if self.get_conflicts(i, self.assignment[i]) > 0:
                conflicted.append(i)

        return conflicted

    def get_conflict_pairs(self):
        pairs = []

        for i in range(self.ward_count):
            for neighbor in self.neighbors[i]:
                if i < neighbor:
                    if self.assignment.get(i) == self.assignment.get(neighbor):
                        pairs.append((i, neighbor))

        return pairs

    def solve_generator(self):
        self.initial_assignment()

        yield ("mc_init", None, None, self.assignment.copy())

        for step in range(1, self.max_steps + 1):
            conflict_pairs = self.get_conflict_pairs()

            yield ("mc_check", None, None, self.assignment.copy(), conflict_pairs)

            if not conflict_pairs:
                yield ("done", None, None, self.assignment.copy())
                return True

            conflicted_vars = self.get_conflicted_variables()
            ward_to_change = random.choice(conflicted_vars)

            yield ("mc_choose", ward_to_change, None, self.assignment.copy(), conflict_pairs)

            color_results = []

            for color in self.colors:
                conflict_count = self.get_conflicts(ward_to_change, color)
                color_results.append((color, conflict_count))

            min_conflict = min(count for color, count in color_results)
            best_colors = [
                color for color, count in color_results
                if count == min_conflict
            ]

            chosen_color = random.choice(best_colors)

            yield (
                "mc_try_all",
                ward_to_change,
                chosen_color,
                self.assignment.copy(),
                color_results
            )

            self.assignment[ward_to_change] = chosen_color

            yield ("mc_update", ward_to_change, chosen_color, self.assignment.copy())

        yield ("done", None, None, self.assignment.copy())
        return False