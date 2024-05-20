import tkinter as tk
from tkinter import messagebox

def generate_maze(width, height):
    maze = [
        [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0],
        [0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
        [0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,1,0,1],
    ]
    return maze

def solve_maze(maze, start, end):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def backtrack(x, y, path):
        if (x, y) == end:
            path.append((x, y))
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

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.width = 18  # Adjust width and height
        self.height = 18
        self.cell_size = 500 // self.width  # Adjust cell size

        self.maze = generate_maze(self.width, self.height)
        self.original_maze = [row[:] for row in self.maze]  # Save the original maze layout
        self.start = (0, 0)
        self.end = (self.width - 1, self.height - 1)

        self.draw_maze()
        self.solve_button = tk.Button(self.root, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack()
        self.reset_button = tk.Button(self.root, text="Reset Maze", command=self.reset_maze)
        self.reset_button.pack()

    def draw_maze(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                color = "white" if self.maze[y][x] == 0 else "black"
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color
                )

    def solve_maze(self):
        solution_found, path = solve_maze(self.maze, self.start, self.end)
        if solution_found:
            for x, y in path:
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill="green"
                )
            messagebox.showinfo("Maze Solver", "Solution Found!")
        else:
            messagebox.showinfo("Maze Solver", "No Solution Found.")

    def reset_maze(self):
        self.maze = [row[:] for row in self.original_maze]  # Restore the original maze layout
        self.draw_maze()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
