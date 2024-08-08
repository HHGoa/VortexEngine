from Engine.Vortex import Vortex
from Engine.Vortex import *

# Initialize Vortex
vortex = Vortex(PrivateKey="0xa4b20ab4faf41ee253f57dc8c5724a0aec3e7efa27600ffb83ec4d64be097225")

# 1. Create the Tic Tac Toe grid
grid_size = 3
cell_size = 2
grid = []

for x in range(grid_size):
    row = []
    for y in range(grid_size):
        cell = vortex.Object(model='quad', x=(x - grid_size / 2) * cell_size, y=(y - grid_size / 2) * cell_size, scale=(cell_size, cell_size), collider='box', color=vortex.color("black"))
        row.append(cell)
    grid.append(row)

# Add grid lines for better visibility
for i in range(grid_size + 1):
    vortex.Object(model='quad', x=(i - grid_size / 2 - 0.5) * cell_size, y=0, scale=(0.1, grid_size * cell_size), color=vortex.color("white"))
    vortex.Object(model='quad', x=0, y=(i - grid_size / 2 - 0.5) * cell_size, scale=(grid_size * cell_size, 0.1), color=vortex.color("white"))

# 2. Initialize game state
current_player = 'X'
board = [['' for _ in range(grid_size)] for _ in range(grid_size)]
game_over = False
scores = {'X': 0, 'O': 0}

# 3. Display Title and Score
title = vortex.Label(text='Tic Tac Toe', scale=2, y=6, background=True, color=vortex.color("white"))
score_label = vortex.Label(text=f'X: {scores["X"]} - O: {scores["O"]}', scale=1.5, y=5, background=True, color=vortex.color("white"))
current_player_label = vortex.Label(text=f'Current Player: {current_player}', scale=1.5, y=4, background=True, color=vortex.color("white"))

# 4. Function to check for a win
def check_win(player):
    # Check rows, columns, and diagonals
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(grid_size):
        if all(board[row][col] == player for row in range(grid_size)):
            return True
    if all(board[i][i] == player for i in range(grid_size)) or all(board[i][grid_size - 1 - i] == player for i in range(grid_size)):
        return True
    return False

# 5. Function to handle cell clicks
def on_click(cell, x, y):
    global current_player, game_over
    if game_over or board[x][y]:
        return
    board[x][y] = current_player
    cell.color = vortex.color("red" if current_player == 'X' else "blue")
    if check_win(current_player):
        scores[current_player] += 1
        score_label.text = f'X: {scores["X"]} - O: {scores["O"]}'
        vortex.Label(text=f'{current_player} Wins!', scale=2, origin=(0, 0), background=True, color=vortex.color("green"))
        vortex.UpdateBlock()  # Call update block function
        game_over = True
    elif all(all(cell for cell in row) for row in board):
        vortex.Label(text='Draw!', scale=2, origin=(0, 0), background=True, color=vortex.color("yellow"))
        vortex.UpdateBlock()  # Call update block function
        game_over = True
    else:
        current_player = 'O' if current_player == 'X' else 'X'
        current_player_label.text = f'Current Player: {current_player}'

# 6. Function to reset the game
def reset_game():
    global board, current_player, game_over
    for x in range(grid_size):
        for y in range(grid_size):
            grid[x][y].color = vortex.color("black")
    board = [['' for _ in range(grid_size)] for _ in range(grid_size)]
    current_player = 'X'
    game_over = False
    current_player_label.text = f'Current Player: {current_player}'

# 7. Attach click event to each cell
for x in range(grid_size):
    for y in range(grid_size):
        cell = grid[x][y]
        cell.on_click = lambda cell=cell, x=x, y=y: on_click(cell, x, y)

# 8. Add a reset button
reset_button = vortex.Object(model='quad', x=0, y=-6, scale=(4, 1), color=vortex.color("gray"))
reset_label = vortex.Label(text='Reset Game', parent=reset_button, scale=1.5, origin=(0, 0), background=True, color=vortex.color("white"))
reset_button.on_click = reset_game

# 9. Run the game
vortex.run()
