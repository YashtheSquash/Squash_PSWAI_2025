from collections import deque
import copy

# === CSP Infrastructure ===

class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def is_consistent(self, var, value, assignment):
        for other_var in assignment:
            if (var, other_var) in self.constraints and not self.constraints[(var, other_var)](value, assignment[other_var]):
                return False
            if (other_var, var) in self.constraints and not self.constraints[(other_var, var)](assignment[other_var], value):
                return False
        return True

def revise(domains, xi, xj, csp):
    revised = False
    constraint = csp.constraints.get((xi, xj), None)
    if not constraint:
        return False
    to_remove = []
    for x in domains[xi]:
        if not any(constraint(x, y) for y in domains[xj]):
            to_remove.append(x)
            revised = True
    for x in to_remove:
        domains[xi].remove(x)
    return revised

def ac3(domains, csp, assignment):
    queue = deque()
    for var in domains:
        for neighbor in domains:
            if var != neighbor and (var, neighbor) in csp.constraints:
                queue.append((var, neighbor))
    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj, csp):
            if not domains[xi]:
                return False
            for xk in domains:
                if xk != xi and (xk, xi) in csp.constraints:
                    queue.append((xk, xi))
    return True

def backtrack(assignment, csp):
    if len(assignment) == len(csp.variables):
        return assignment

    unassigned = [v for v in csp.variables if v not in assignment]
    var = unassigned[0]
    for value in csp.domains[var]:
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            local_domains = copy.deepcopy(csp.domains)
            local_domains[var] = [value]
            if ac3(local_domains, csp, assignment):
                original_domains = csp.domains
                csp.domains = local_domains
                result = backtrack(assignment, csp)
                csp.domains = original_domains
                if result:
                    return result
            del assignment[var]
    return None

def backtracking_search(csp):
    return backtrack({}, csp)

# === Sudoku-Specific Functions ===

def read_sudoku(filename="text.txt"):
    board = []
    with open(filename, 'r') as file:
        for line in file:
            row = list(map(int, line.strip().split()))
            if row:
                board.append(row)
    return board

def print_sudoku(board):
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j, val in enumerate(row):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(val if val != 0 else ".", end=" ")
        print()

def sudoku_to_csp(board):
    variables = []
    domains = {}
    constraints = {}
    fixed_values = {}

    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                variables.append((r, c))
                domains[(r, c)] = list(range(1, 10))
            else:
                domains[(r, c)] = [board[r][c]]
                fixed_values[(r, c)] = board[r][c]

    def constraint_fn(a, b):
        return a != b

    all_cells = [(r, c) for r in range(9) for c in range(9)]

    for (r1, c1) in all_cells:
        for (r2, c2) in all_cells:
            if (r1, c1) == (r2, c2):
                continue
            same_row = r1 == r2
            same_col = c1 == c2
            same_box = (r1 // 3 == r2 // 3) and (c1 // 3 == c2 // 3)
            if same_row or same_col or same_box:
                constraints[((r1, c1), (r2, c2))] = constraint_fn

    return CSP(variables, domains, constraints), fixed_values

def csp_to_sudoku(solution, fixed_values):
    board = [[0 for _ in range(9)] for _ in range(9)]

    for (r, c), val in fixed_values.items():
        board[r][c] = val
    for (r, c), val in solution.items():
        board[r][c] = val

    return board

# === Run ===

if __name__ == "__main__":
    board = read_sudoku("text.txt")
    print("Initial Sudoku:")
    print_sudoku(board)

    csp, fixed_values = sudoku_to_csp(board)
    solution = backtracking_search(csp)

    if solution:
        final_board = csp_to_sudoku(solution, fixed_values)
        print("\nSolved Sudoku:")
        print_sudoku(final_board)
    else:
        print("No solution found.")
