from collections import deque
import heapq
import math

def build_graph(num_junctions, pipes):
    """
    Build an adjacency list representing the pipe network.
    Each junction is mapped to a list of (neighbor, travel_cost) tuples.
    """
    graph = {i: [] for i in range(num_junctions)}
    for node1, node2, cost in pipes:
        graph[node1].append((node2, cost))
        graph[node2].append((node1, cost))  # Since pipes are undirected
    return graph

def bfs(num_junctions, pipes, start, goal):
    """
    Breadth-First Search: finds the shortest path by steps (not by lowest cost).
    Returns the path followed and all visited junctions.
    """
    graph = build_graph(num_junctions, pipes)
    queue = deque([(start, [start])])
    visited = set([start])
    all_visited = [start]
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path, all_visited
        for neighbor, _ in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                all_visited.append(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None, all_visited

def dfs(num_junctions, pipes, start, goal):
    """
    Depth-First Search: explores as deeply as possible. Not always optimal.
    Returns the path followed and all visited junctions.
    """
    graph = build_graph(num_junctions, pipes)
    stack = [(start, [start])]
    visited = set([start])
    all_visited = [start]
    while stack:
        current, path = stack.pop()
        if current == goal:
            return path, all_visited
        for neighbor, _ in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                all_visited.append(neighbor)
                stack.append((neighbor, path + [neighbor]))
    return None, all_visited

def heuristic(a, b, coords):
    """
    Straight-line (Euclidean) distance between two junctions for A*.
    """
    x1, y1 = coords[a]
    x2, y2 = coords[b]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def a_star(num_junctions, pipes, coords, start, goal):
    """
    A* Search: finds the lowest-cost path using cost and a heuristic.
    Returns the path followed and all visited junctions.
    """
    graph = build_graph(num_junctions, pipes)
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal, coords), 0, start, [start]))
    best_cost = {start: 0}
    all_visited = [start]
    visited_node_set = set([start])

    while open_set:
        f, cost_so_far, current, path = heapq.heappop(open_set)
        if current == goal:
            return path, all_visited
        for neighbor, cost in graph[current]:
            new_cost = cost_so_far + cost
            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                estimated_total = new_cost + heuristic(neighbor, goal, coords)
                heapq.heappush(open_set, (estimated_total, new_cost, neighbor, path + [neighbor]))
                if neighbor not in visited_node_set:
                    all_visited.append(neighbor)
                    visited_node_set.add(neighbor)
    return None, all_visited

def total_cost(path, pipes):
    """
    Calculate the total travel cost in the path.
    """
    if path is None or len(path) < 2:
        return 0
    # (u,v) sorted for undirected edge matching
    edges = {(min(u, v), max(u, v)): cost for u, v, cost in pipes}
    cost = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        key = (min(u, v), max(u, v))
        cost += edges.get(key, 0)
    return cost

# ------ Example Network (replace it with own input data as needed) ------
num_junctions = 5
pipes = [
    (0, 1, 3),
    (1, 2, 5),
    (2, 3, 2),
    (1, 3, 8),
    (3, 4, 1)
]
coords = [  # Example coordinates for A*
    (0, 0),   # Junction 0
    (1, 1),   # Junction 1
    (2, 2),   # Junction 2
    (3, 1),   # Junction 3
    (4, 0)    # Junction 4
]
start = 0
goal = 4

# ------------ Run search algorithms and print results ---------------------

bfs_path, bfs_visited = bfs(num_junctions, pipes, start, goal)
dfs_path, dfs_visited = dfs(num_junctions, pipes, start, goal)
a_star_path, a_star_visited = a_star(num_junctions, pipes, coords, start, goal)

print("BFS strategy:")
print(" - Path:", bfs_path)
print(" - Total cost:", total_cost(bfs_path, pipes))
print(" - Junctions visited (in order):", bfs_visited)
print(" - Number of junctions visited:", len(bfs_visited))
print()

print("DFS strategy:")
print(" - Path:", dfs_path)
print(" - Total cost:", total_cost(dfs_path, pipes))
print(" - Junctions visited (in order):", dfs_visited)
print(" - Number of junctions visited:", len(dfs_visited))
print()

print("A* strategy:")
print(" - Path:", a_star_path)
print(" - Total cost:", total_cost(a_star_path, pipes))
print(" - Junctions visited (in order):", a_star_visited)
print(" - Number of junctions visited:", len(a_star_visited))
print()


"""OUTPUT OF THE EXAMPLE DATA:
BFS strategy:
 - Path: [0, 1, 3, 4]
 - Total cost: 12
 - Junctions visited (in order): [0, 1, 2, 3, 4]
 - Number of junctions visited: 5

DFS strategy:
 - Path: [0, 1, 3, 4]
 - Total cost: 12
 - Junctions visited (in order): [0, 1, 2, 3, 4]
 - Number of junctions visited: 5

A* strategy:
 - Path: [0, 1, 2, 3, 4]
 - Total cost: 11
 - Junctions visited (in order): [0, 1, 2, 3, 4]
 - Number of junctions visited: 5
"""
