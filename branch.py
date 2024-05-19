import heapq

def generate_maze(width, height):
    maze = [
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0]
    ]
    return maze

def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def solve_maze(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def heuristic_cost_estimate(node):
        return manhattan_distance(node, end)

    queue = [(heuristic_cost_estimate(start), 0, [start])]  # (estimated cost, actual cost, path)
    heapq.heapify(queue)

    while queue:
        _, cost, path = heapq.heappop(queue)
        current_position = path[-1]

        if current_position == end:
            return path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current_position[0] + dx, current_position[1] + dy)
            if is_valid_move(*new_position) and new_position not in path:
                new_cost = cost + 1
                new_path = path + [new_position]
                heapq.heappush(queue, (new_cost + heuristic_cost_estimate(new_position), new_cost, new_path))

    return None  # No solution found

# Example usage
width = 10
height = 10
maze = generate_maze(width, height)
print("Generated Maze:")
for row in maze:
    print("".join(["#" if cell == 1 else " " for cell in row]))

start = (0, 0)
end = (width - 1, height - 1)
print("\nSolving Maze...")
solution_path = solve_maze(maze, start, end)
if solution_path:
    print("\nSolution Found:")
    solution_maze = [row[:] for row in maze]  # Make a copy of the maze to mark the path
    for x, y in solution_path:
        solution_maze[y][x] = "@"  # Mark path cells as visited
    for row in solution_maze:
        print("".join(["#" if cell == 1 else " " if cell == 0 else "@" for cell in row]))  # Print path as @
else:
    print("\nNo Solution Found.")
