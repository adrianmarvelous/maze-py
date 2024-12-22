import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
import pickle

# Maze yang udah ada
maze = [
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Parameter Maze
start = (1, 1)
end = (5, 7)
width = len(maze[0])
height = len(maze)

# Parameter Q-Learning
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.2  # Exploration rate
num_actions = 4  # UP, DOWN, LEFT, RIGHT

# Inisialisasi Q-table
agent1_Q_table = np.zeros((width * height, num_actions))
agent2_Q_table = np.zeros((width * height, num_actions))

# Map koordinat ke state index
def state_to_index(x, y, width):
    return y * width + x

def index_to_state(index, width):
    return index % width, index // width

# Dapetin gerakan yang valid
def get_valid_moves(x, y):
    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # UP, DOWN, LEFT, RIGHT
    valid_moves = []
    for i, (dx, dy) in enumerate(moves):
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < width and 0 <= new_y < height and maze[new_y][new_x] == 0:
            valid_moves.append((i, new_x, new_y))
    return valid_moves

# Langkah Q-learning
def q_learning_step(Q_table, x, y):
    state = state_to_index(x, y, width)
    moves = get_valid_moves(x, y)

    if not moves:
        return x, y  # Gak ada gerakan valid

    if random.random() < epsilon:
        # Eksplorasi: Pilih aksi random yang valid
        action, new_x, new_y = random.choice(moves)
    else:
        # Eksploitasi: Pilih aksi terbaik
        action = np.argmax(Q_table[state])
        valid_action = [(a, nx, ny) for a, nx, ny in moves if a == action]
        if valid_action:
            _, new_x, new_y = valid_action[0]
        else:
            action, new_x, new_y = random.choice(moves)

    # Sistem reward
    if (new_x, new_y) == end:
        reward = 100
    else:
        reward = -1

    # Update Q-learning
    next_state = state_to_index(new_x, new_y, width)
    Q_table[state, action] += alpha * (
        reward + gamma * np.max(Q_table[next_state]) - Q_table[state, action]
    )
    return new_x, new_y

# Latih agen-agen selama episode
def train_agents(episodes, max_steps_per_episode):
    for episode in range(episodes):
        x1, y1 = start
        x2, y2 = (1, 1)
        steps = 0

        while steps < max_steps_per_episode:
            if (x1, y1) == end or (x2, y2) == end:
                break  # Hentikan kalau salah satu agen sampai ke tujuan

            x1, y1 = q_learning_step(agent1_Q_table, x1, y1)
            x2, y2 = q_learning_step(agent2_Q_table, x2, y2)
            steps += 1

        print(f"Episode {episode + 1}: Agen 1 di {x1, y1}, Agen 2 di {x2, y2}")

# Simpan Q-table
def save_q_tables():
    with open("agent1_Q_table.pkl", "wb") as f:
        pickle.dump(agent1_Q_table, f)
    with open("agent2_Q_table.pkl", "wb") as f:
        pickle.dump(agent2_Q_table, f)

# Render maze dan agen menggunakan Tkinter
def render_maze(agent1_pos, agent2_pos):
    window = tk.Tk()
    window.title("Maze Solver")

    canvas = tk.Canvas(window, width=width * 30, height=height * 30)
    canvas.pack()

    # Gambar maze
    for y in range(height):
        for x in range(width):
            color = "white" if maze[y][x] == 0 else "black"
            canvas.create_rectangle(x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill=color)

    # Gambar Agen 1
    ax1, ay1 = agent1_pos
    canvas.create_oval(ax1 * 30 + 5, ay1 * 30 + 5, ax1 * 30 + 25, ay1 * 30 + 25, fill="blue")

    # Gambar Agen 2
    ax2, ay2 = agent2_pos
    canvas.create_oval(ax2 * 30 + 5, ay2 * 30 + 5, ax2 * 30 + 25, ay2 * 30 + 25, fill="red")

    # Flag game over
    game_over = False

    def update():
        nonlocal agent1_pos, agent2_pos, game_over

        if game_over:
            return  # Hentikan update

        if agent1_pos == end:
            if not game_over:
                messagebox.showinfo("Sukses", "Agen 1 sudah sampai ke tujuan!")
                game_over = True
            return  # Hentikan update lebih lanjut
        if agent2_pos == end:
            if not game_over:
                messagebox.showinfo("Sukses", "Agen 2 sudah sampai ke tujuan!")
                game_over = True
            return  # Hentikan update lebih lanjut

        if not game_over:
            new_agent1_pos = q_learning_step(agent1_Q_table, agent1_pos[0], agent1_pos[1])
            new_agent2_pos = q_learning_step(agent2_Q_table, agent2_pos[0], agent2_pos[1])

            if new_agent1_pos != agent1_pos:
                agent1_pos = new_agent1_pos
            if new_agent2_pos != agent2_pos:
                agent2_pos = new_agent2_pos

            canvas.delete("all")
            for y in range(height):
                for x in range(width):
                    color = "white" if maze[y][x] == 0 else "black"
                    canvas.create_rectangle(x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill=color)

            ax1, ay1 = agent1_pos
            canvas.create_oval(ax1 * 30 + 5, ay1 * 30 + 5, ax1 * 30 + 25, ay1 * 30 + 25, fill="blue")

            ax2, ay2 = agent2_pos
            canvas.create_oval(ax2 * 30 + 5, ay2 * 30 + 5, ax2 * 30 + 25, ay2 * 30 + 25, fill="red")

        if not game_over:
            window.after(100, update)  # Jadwalkan update berikutnya kalau game belum selesai

    window.after(100, update)
    window.mainloop()

# Latih dan render
train_agents(episodes=1000, max_steps_per_episode=200)
render_maze(agent1_pos=start, agent2_pos=(1, 1))
