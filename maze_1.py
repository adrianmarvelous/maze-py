def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]

    # Create walls along the borders
    for i in range(width):
        maze[0][i] = maze[height - 1][i] = 1
    for i in range(height):
        maze[i][0] = maze[i][width - 1] = 1

    # Create paths
    for i in range(2, height - 1, 2):
        for j in range(2, width - 1, 2):
            maze[i][j] = 0

    return maze

def print_maze(maze):
    for row in maze:
        print("".join(["#" if cell == 1 else " " for cell in row]))

# Example usage
width = 20
height = 10
maze = generate_maze(width, height)
print("Generated Maze:")
print_maze(maze)
