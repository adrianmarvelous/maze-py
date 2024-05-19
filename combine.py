def generate_maze(width, height):
    maze = [
        [0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    ]
    return maze

def solve_maze(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def backtrack(x, y, path):
        if (x, y) == end:
            return True
        if is_valid_move(x, y):
            path.append((x, y))
            maze[y][x] = 2  # Mark as visited
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if backtrack(x + dx, y + dy, path):
                    return True
            path.pop()  # Backtrack
            maze[y][x] = 0  # Unmark if not part of solution path
        return False

    path = []
    if backtrack(start[0], start[1], path):
        return True, path
    return False, []

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
solution_found, path = solve_maze(maze, start, end)
if solution_found:
    print("\nSolution Found:")
    solution_maze = [row[:] for row in maze]  # Make a copy of the maze to mark the path
    for x, y in path:
        solution_maze[y][x] = "@"  # Mark path cells as visited
    for row in solution_maze:
        print("".join(["#" if cell == 1 else " " if cell == 0 else "@" for cell in row]))  # Print path as @
else:
    print("\nNo Solution Found.")
