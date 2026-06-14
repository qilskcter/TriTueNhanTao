COLORS = ["red", "lime", "blue", "yellow"]

class ForwardCheckingSolver:
    def __init__(self, ward_count, ward_names, neighbors):
        self.ward_count = ward_count
        self.ward_names = ward_names
        self.neighbors = neighbors
        self.assignment = {}
        self.domains = {
            i: COLORS.copy()
            for i in range(ward_count)
        }

    def is_valid(self, ward_index, color):
        for neighbor in self.neighbors[ward_index]:
            if self.assignment.get(neighbor) == color:
                return False
        return True

    def get_valid_colors(self, ward_index):
        return [
            color for color in self.domains[ward_index]
            if self.is_valid(ward_index, color)
        ]

    def select_unassigned_variable(self):
        unassigned = [
            i for i in range(self.ward_count)
            if i not in self.assignment
        ]

        best = None
        best_domain_size = 999
        best_degree = -1

        for ward in unassigned:
            domain_size = len(self.get_valid_colors(ward))
            degree = len(self.neighbors[ward])

            if domain_size < best_domain_size:
                best = ward
                best_domain_size = domain_size
                best_degree = degree
            elif domain_size == best_domain_size and degree > best_degree:
                best = ward
                best_degree = degree

        return best

    def solve_generator(self):
        if len(self.assignment) == self.ward_count:
            yield ("done", None, None, self.assignment.copy(), [])
            return True

        ward_index = self.select_unassigned_variable()
        yield ("choose", ward_index, None, self.assignment.copy(), [])

        for color in self.get_valid_colors(ward_index):
            yield ("try", ward_index, color, self.assignment.copy(), [])

            if not self.is_valid(ward_index, color):
                yield ("invalid", ward_index, color, self.assignment.copy(), [])
                continue

            self.assignment[ward_index] = color

            old_domains = {
                i: self.domains[i].copy()
                for i in self.domains
            }

            self.domains[ward_index] = [color]

            ok = True
            removed_list = []

            for neighbor in self.neighbors[ward_index]:
                if neighbor not in self.assignment:
                    if color in self.domains[neighbor]:
                        self.domains[neighbor].remove(color)
                        removed_list.append((neighbor, color))

                    if len(self.domains[neighbor]) == 0:
                        ok = False

            yield ("fc", ward_index, color, self.assignment.copy(), removed_list)

            if ok:
                yield ("valid", ward_index, color, self.assignment.copy(), [])

                result = yield from self.solve_generator()

                if result:
                    return True
            else:
                yield ("domain_empty", ward_index, color, self.assignment.copy(), [])

            self.domains = old_domains
            del self.assignment[ward_index]

            yield ("backtrack", ward_index, color, self.assignment.copy(), [])

        return False