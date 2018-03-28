from que import PriorityQueue
from math import inf

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def manhattan_dist(goal, current):
    (x1, y1) = goal.point
    (x2, y2) = current.point
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    path_in_meters = 0
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next in current.getConnections():
            if next.terrain == inf:
                continue
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                path_in_meters += current.getWeight(next)
                priority = new_cost + manhattan_dist(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far, path_in_meters