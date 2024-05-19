import random

# Function to generate a maze using Prim's algorithm
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    
    # Randomly select a starting cell
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    maze[start_y][start_x] = 0
    visited_cells = [(start_x, start_y)]

    while visited_cells:
        current_x, current_y = visited_cells.pop()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            next_x, next_y = current_x + 2 * dx, current_y + 2 * dy
            if 0 <= next_x < width and 0 <= next_y < height and maze[next_y][next_x] == 1:
                maze[next_y][next_x] = 0
                maze[current_y + dy][current_x + dx] = 0
                visited_cells.append((next_x, next_y))
                visited_cells.append((current_x + dx, current_y + dy))

    return maze

# Function to print the maze
def print_maze(maze):
    for row in maze:
        print("".join(["#" if cell == 1 else " " if cell == 0 else "X" for cell in row]))

# Backtracking algorithm to solve the maze
def solve_maze(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def backtrack(x, y):
        if (x, y) == end:
            return True
        if is_valid_move(x, y):
            maze[y][x] = 2  # Mark as visited
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if backtrack(x + dx, y + dy):
                    return True
            maze[y][x] = 0  # Unmark if not part of solution path
        return False

    return backtrack(start[0], start[1])

# Example usage
width = 20
height = 10
maze = generate_maze(width, height)
print("Generated Maze:")
print_maze(maze)
start = (1, 1)
end = (width - 2, height - 2)
print("\nSolving Maze...")
if solve_maze(maze, start, end):
    print("\nSolution Found:")
    print_maze(maze)
else:
    print("\nNo Solution Found.")
