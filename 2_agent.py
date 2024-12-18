import tkinter as tk
from tkinter import messagebox
import time

# Predefined single maze
maze = [
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,0,0,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,1,1,1,1,0,0,1,0,0,0,1,0,1],
    [1,1,1,0,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0],
    [1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,1,0,1,1,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,1],
    [1,0,0,0,1,1,1,0,1,0,1,0,1,1,0,0,0,1,1,1],
    [0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def solve_maze_backtracking(maze, start, end, app, player_id, delay=20):
    def is_valid_move(x, y):
        return 0 <= x < len(maze[0]) and 0 <= y < len(maze) and maze[y][x] == 0

    def backtrack(x, y, path):
        if (x, y) == end:
            path.append((x, y))
            return True
        if is_valid_move(x, y):
            path.append((x, y))
            color = "blue" if player_id == 1 else "yellow"  # Different colors for each player
            app.update_canvas(x, y, color, delay=delay)  # Visualize path exploration with delay
            maze[y][x] = 2  # Mark as visited
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if backtrack(x + dx, y + dy, path):
                    return True
            path.pop()  # Backtrack
            app.update_canvas(x, y, "red", delay=delay)  # Visualize backtracking with delay
            maze[y][x] = 0  # Unmark if not part of solution path
        return False

    path = []
    if backtrack(start[0], start[1], path):
        return True, path
    return False, []

class MazeApp:
    def __init__(self, root, maze):
        self.root = root
        self.root.title("Maze Solver")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.maze = maze
        self.original_maze = [row[:] for row in self.maze]  # Save the original maze layout
        self.width = len(maze[0])
        self.height = len(maze)
        self.cell_size = 500 // self.width  # Adjust cell size
        self.start1 = (0, 15)  # Player 1 start position
        self.start2 = (0, 0)   # Player 2 start position
        self.end = (self.width - 1, self.height - 7)  # End position

        self.draw_maze()
        self.solve_button = tk.Button(self.root, text="Solve with Backtracking", command=self.solve_maze_backtracking)
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
        self.canvas.create_rectangle(
            self.start1[0] * self.cell_size, self.start1[1] * self.cell_size,
            (self.start1[0] + 1) * self.cell_size, (self.start1[1] + 1) * self.cell_size,
            fill="green"
        )
        self.canvas.create_rectangle(
            self.start2[0] * self.cell_size, self.start2[1] * self.cell_size,
            (self.start2[0] + 1) * self.cell_size, (self.start2[1] + 1) * self.cell_size,
            fill="orange"
        )
        self.canvas.create_rectangle(
            self.end[0] * self.cell_size, self.end[1] * self.cell_size,
            (self.end[0] + 1) * self.cell_size, (self.end[1] + 1) * self.cell_size,
            fill="red"
        )

    def update_canvas(self, x, y, color, delay=0):
        self.canvas.create_rectangle(
            x * self.cell_size, y * self.cell_size,
            (x + 1) * self.cell_size, (y + 1) * self.cell_size,
            fill=color
        )
        self.canvas.update_idletasks()
        if delay > 0:
            self.canvas.after(delay)

    def solve_maze_backtracking(self):
        self.maze = [row[:] for row in self.original_maze]  # Reset the maze before solving
        self.draw_maze()
        start_time = time.time()  # Start the timer

        # Solve for Player 1 (Blue) path
        solution_found1, path1 = solve_maze_backtracking(self.maze, self.start1, self.end, self, 1)

        # Now make Player 2 (Yellow) follow the Blue player's path
        if solution_found1:
            for x, y in path1:
                self.update_canvas(x, y, "blue", delay=20)
            
            # Player 2 follows the same path
            for i, (x, y) in enumerate(path1):
                color = "yellow"
                self.update_canvas(x, y, color, delay=20)
                if i < len(path1) - 1:
                    next_x, next_y = path1[i+1]
                    self.update_canvas(next_x, next_y, color, delay=20)

            end_time = time.time()  # End the timer
            elapsed_time = end_time - start_time  # Calculate elapsed time
            messagebox.showinfo("Maze Solver", f"Both Players Found Solutions!\nTime taken: {elapsed_time:.2f} seconds")
        else:
            messagebox.showinfo("Maze Solver", "No Solution Found.")

    def reset_maze(self):
        self.maze = [row[:] for row in self.original_maze]  # Restore the original maze layout
        self.draw_maze()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    maze_app = MazeApp(root, maze)
    maze_app.run()
