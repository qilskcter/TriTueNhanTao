from collections import deque


class AC3Solver:
    def __init__(self, ward_count, ward_names, neighbors):
        self.ward_count = ward_count
        self.ward_names = ward_names
        self.neighbors = neighbors
        self.colors = ["red", "lime", "blue", "yellow"]
        self.domains = {
            i: self.colors.copy()
            for i in range(self.ward_count)
        }
        self.assignment = {}

    def revise(self, xi, xj):
        removed = []

        for color_x in self.domains[xi][:]:
            ok = False

            for color_y in self.domains[xj]:
                if color_x != color_y:
                    ok = True
                    break

            if not ok:
                self.domains[xi].remove(color_x)
                removed.append(color_x)

        return removed

    def ac3(self):
        queue = deque()

        for xi in range(self.ward_count):
            for xj in self.neighbors[xi]:
                queue.append((xi, xj))

        yield ("ac3_init", None, None, self.assignment.copy(), list(queue), self.copy_domains())

        while queue:
            xi, xj = queue.popleft()

            yield ("ac3_check", xi, xj, self.assignment.copy(), list(queue), self.copy_domains())

            removed = self.revise(xi, xj)

            if removed:
                yield ("ac3_remove", xi, xj, self.assignment.copy(), removed, self.copy_domains())

                if len(self.domains[xi]) == 0:
                    yield ("domain_empty", xi, None, self.assignment.copy())
                    return False

                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
                        yield ("ac3_add", xk, xi, self.assignment.copy(), list(queue), self.copy_domains())

        return True

    def is_valid(self, ward_index, color):
        for neighbor in self.neighbors[ward_index]:
            if self.assignment.get(neighbor) == color:
                return False
        return True

    def backtrack(self):
        if len(self.assignment) == self.ward_count:
            yield ("done", None, None, self.assignment.copy())
            return True

        ward_index = None

        for i in range(self.ward_count):
            if i not in self.assignment:
                ward_index = i
                break

        yield ("choose", ward_index, None, self.assignment.copy())

        for color in self.domains[ward_index]:
            yield ("try", ward_index, color, self.assignment.copy())

            if self.is_valid(ward_index, color):
                self.assignment[ward_index] = color
                yield ("valid", ward_index, color, self.assignment.copy())

                result = yield from self.backtrack()

                if result:
                    return True

                del self.assignment[ward_index]
                yield ("backtrack", ward_index, color, self.assignment.copy())
            else:
                yield ("invalid", ward_index, color, self.assignment.copy())

        return False

    def solve_generator(self):
        result = yield from self.ac3()

        if not result:
            return False

        yield ("ac3_done", None, None, self.assignment.copy(), None, self.copy_domains())

        result = yield from self.backtrack()

        if not result:
            yield ("done", None, None, self.assignment.copy())

        return result

    def copy_domains(self):
        return {
            key: value.copy()
            for key, value in self.domains.items()
        }