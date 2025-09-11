import heapq
import math
import time

# ===================== Heuristic Functions =====================
# These help guide the search by estimating the cost to reach the goal.

def manhattan(a, b):
    """Manhattan Distance (for 4-directional movement)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean(a, b):
    """Euclidean Distance (straight-line)."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def diagonal(a, b):
    """Chebyshev Distance (when diagonal moves are allowed)."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


# ===================== Grid Utilities =====================

def parse_grid(grid_str):
    """
    Convert a string-based grid into a 2D list.
    Also identify the Start (S) and Goal (G) positions.
    """
    grid = [list(row) for row in grid_str.strip().split("/")]
    start = goal = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'G':
                goal = (i, j)
    return grid, start, goal


def get_neighbors(pos, grid, allow_diagonal=True):
    """
    Get valid neighbors for the current position.
    By default, allows 8-directional movement.
    """
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    if allow_diagonal:
        directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonals

    neighbors = []
    for dx, dy in directions:
        new_x, new_y = pos[0] + dx, pos[1] + dy
        if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
            if grid[new_x][new_y] != '1':  # '1' means wall
                neighbors.append((new_x, new_y))
    return neighbors


def cell_cost(to_cell):
    """Return movement cost: normal = 1, ghost zone (6) = 6."""
    return 6 if to_cell == '6' else 1


# ===================== Search Algorithms =====================

def greedy_bfs(grid, start, goal, heuristic):
    """Greedy Best-First Search (chooses node closest to goal)."""
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    came_from = {start: None}
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:  # Goal found
            break

        explored.add(current)

        for neighbor in get_neighbors(current, grid):
            if neighbor not in came_from:
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal), len(explored)


def a_star(grid, start, goal, heuristic):
    """A* Search (balances actual cost + heuristic)."""
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        explored.add(current)

        for neighbor in get_neighbors(current, grid):
            nx, ny = neighbor
            move_cost = cell_cost(grid[nx][ny])
            new_cost = cost_so_far[current] + move_cost

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal), len(explored)


def reconstruct_path(came_from, start, goal):
    """
    Reconstruct path from start to goal using the 'came_from' dictionary.
    """
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()

    # Return path only if it actually starts at 'start'
    if path and path[0] == start:
        return path
    return []


def print_grid_with_path(grid, path):
    """Print the grid with '*' marking the path."""
    display = [row[:] for row in grid]
    for x, y in path:
        if display[x][y] not in ('S', 'G'):
            display[x][y] = '*'
    for row in display:
        print("".join(row))
    print()


# ===================== Runner =====================

def run_all_algorithms(grid_str):
    """Run Greedy BFS and A* with all heuristics."""
    grid, start, goal = parse_grid(grid_str)

    if not start or not goal:
        print("Start (S) or Goal (G) missing from grid!")
        return

    heuristics = [
        ('Manhattan', manhattan),
        ('Euclidean', euclidean),
        ('Diagonal', diagonal)
    ]

    for name, h_func in heuristics:
        print(f"=== Greedy Best-First ({name}) ===")
        t1 = time.time()
        path, explored = greedy_bfs(grid, start, goal, h_func)
        t2 = time.time()
        print(f"Path length: {len(path)} | Nodes explored: {explored} | Time: {t2 - t1:.4f}s")
        print_grid_with_path(grid, path)

        print(f"=== A* Search ({name}) ===")
        t1 = time.time()
        path, explored = a_star(grid, start, goal, h_func)
        t2 = time.time()
        print(f"Path length: {len(path)} | Nodes explored: {explored} | Time: {t2 - t1:.4f}s")
        print_grid_with_path(grid, path)


# ===================== Example =====================

# Legend:
# 0 = open cell
# 1 = wall
# 6 = ghost/high-cost zone
# S = start
# G = goal
example_grid = (
    "S000000/"
    "0111110/"
    "0000100/"
    "0116100/"
    "0000100/"
    "0111100/"
    "000000G"
)


run_all_algorithms(example_grid)

"""
EXAMPLE OUTPUT:
=== Greedy Best-First (Manhattan) ===
Path length: 12 | Nodes explored: 11 | Time: 0.0001s
S*****0
011111*
000010*
011610*
000010*
011110*
000000G

=== A* Search (Manhattan) ===
Path length: 12 | Nodes explored: 11 | Time: 0.0001s
S*****0
011111*
000010*
011610*
000010*
011110*
000000G

=== Greedy Best-First (Euclidean) ===
Path length: 12 | Nodes explored: 11 | Time: 0.0001s
S*****0
011111*
000010*
011610*
000010*
011110*
000000G

=== A* Search (Euclidean) ===
Path length: 12 | Nodes explored: 21 | Time: 0.0001s
S*****0
011111*
000010*
011610*
000010*
011110*
000000G

=== Greedy Best-First (Diagonal) ===
Path length: 12 | Nodes explored: 11 | Time: 0.0001s
S*****0
011111*
00001*0
01161*0
00001*0
01111*0
000000G

=== A* Search (Diagonal) ===
Path length: 12 | Nodes explored: 31 | Time: 0.0001s
S*****0
011111*
00001*0
01161*0
00001*0
01111*0
000000G
"""


