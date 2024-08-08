from Engine.Vortex import Vortex
from Engine.Vortex import *
import random

# Initialize Vortex
vortex = Vortex(PrivateKey="0xa4b20ab4faf41ee253f57dc8c5724a0aec3e7efa27600ffb83ec4d64be097225")

# List of possible background textures
background_textures = ['brick', 'stone', 'wood']

# Choose a random texture for the background
random_texture = random.choice(background_textures)

# List of maze layouts
maze_layouts = [
    [
        "###############",
        "#             #",
        "# ###### #### #",
        "# #      # #  #",
        "# # #### # ####",
        "# #    # #    #",
        "# #### # #### #",
        "#      #      #",
        "###############"
    ],
    [
        "###############",
        "#   #         #",
        "# # ###### #  #",
        "# #      # #  #",
        "# ###### # ####",
        "#      # #    #",
        "###### # #### #",
        "#             #",
        "###############"
    ],
    [
        "###############",
        "#   #         #",
        "### # ######  #",
        "#   #      #  #",
        "# #######  #  #",
        "#       #     #",
        "##### # #######",
        "#             #",
        "###############"
    ],
    [
        "###############",
        "#   #    #    #",
        "### # ## # ## #",
        "#   #  # #  # #",
        "### ### # ##  #",
        "# #    #      #",
        "# # #### #### #",
        "#      #      #",
        "###############"
    ],
    [
        "###############",
        "#             #",
        "# #### ###### #",
        "#   #  #      #",
        "### #### #### #",
        "#      #   #  #",
        "# ## ####### ##",
        "# #         # #",
        "###############"
    ],
    [
        "###############",
        "#   #         #",
        "# # ##### #### #",
        "# #   # #      #",
        "# ##### #### # #",
        "# #         #  #",
        "# ########### ##",
        "#             #",
        "###############"
    ],
    [
        "###############",
        "# #           #",
        "# # #### #### #",
        "#   #  #      #",
        "# ### ####### #",
        "#    #        #",
        "##### ##### ###",
        "#             #",
        "###############"
    ],
    [
        "###############",
        "#  #     #    #",
        "# ## ### # ## #",
        "#    #   #  # #",
        "# ## #######  #",
        "# #   #     # #",
        "# ### ####### #",
        "#             #",
        "###############"
    ],
    [
        "###############",
        "#        #    #",
        "# #### # ## # #",
        "#   #  #    # #",
        "### ### ##### #",
        "#    #   #    #",
        "# ####### #### #",
        "# #           #",
        "###############"
    ],
    [
        "###############",
        "#   #       # #",
        "# # ##### # # #",
        "# #   #   # # #",
        "# ##### ### # #",
        "#           # #",
        "##### ####### #",
        "#             #",
        "###############"
    ]
]

# Choose a random maze layout
maze_layout = random.choice(maze_layouts)

# 1. Create the game environment with a textured ground and random background
ground = vortex.Object(model='plane', scale=(20, 0.1, 20), texture=random_texture, collider='box')
background = vortex.Object(model='quad', scale=(50, 25, 1), x=0, y=12.5, z=-25, texture=random_texture)

# 2. Create the maze walls with the same random texture as background
walls = []

def create_wall(x, z):
    wall = vortex.Object(model='cube', scale=(1, 2, 1), x=x, y=1, z=z, texture=random_texture, collider='box')
    walls.append(wall)

for z, row in enumerate(maze_layout):
    for x, char in enumerate(row):
        if char == "#":
            create_wall(x - 7, z - 4)  # Adjusting positions to center the maze

# 3. Initialize game state with a player character model (using 'sphere' instead of 'humanoid')
player = vortex.firstPersonController(model='sphere', color=vortex.color("blue"), speed=5, x=-6, y=1, z=-3, collider='box')
end_point = vortex.Object(model='cube', scale=(1, 1, 1), x=6, y=0.5, z=3, color=vortex.color("yellow"), collider='box')

# 4. Function to check if player reached the end point and save data
def check_end_point():
    if player.intersects(end_point).hit:
        print("Congratulations! You reached the end of the maze!")
        game_data = {
            "end_time": vortex.app.time,
            "score": 100  # Example score, update with actual score if applicable
        }
        vortex.UpdateBlock(game_data)  # Ensure the UpdateBlock method is called correctly
        vortex.app.quit()  # Ensure the app quits correctly

# 5. Function to update the game
def update():
    check_end_point()

# 6. Set the update function
vortex.app.update = update

# 7. Run the game
vortex.run()
