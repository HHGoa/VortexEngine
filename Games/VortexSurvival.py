from ..Engine.Vortex import Vortex
from ..Engine.Vortex import *
import random

# Initialize Vortex
vortex = Vortex(PrivateKey="Your_private_key")

# 1. Create the game environment with a textured ground
ground_texture = 'grass'  # Assuming you have a grass texture
ground = vortex.Object(model='plane', scale=(100, 0.1, 100), texture=ground_texture, collider='box')

# Set a background texture
background_texture = 'sky'  # Assuming you have a sky texture
background = vortex.Object(model='quad', scale=(50, 25, 1), x=0, y=12.5, z=-25, texture=background_texture)

# 2. Create random terrain
terrain = vortex.Object(model='terrain', scale=(100, 10, 100), texture=ground_texture)

# 3. Generate random collectible items
num_items = 10
collectible_items = []

def create_collectible_item():
    x = random.uniform(-50, 50)
    z = random.uniform(-50, 50)
    y = ground.scale[1] / 2  # Place item on the ground
    item = vortex.Object(model='cube', scale=(1, 1, 1), x=x, y=y, z=z, color=vortex.color("red"), collider='box')
    collectible_items.append(item)

for _ in range(num_items):
    create_collectible_item()

# 4. Initialize game state with a player character model
player = vortex.firstPersonController(model='sphere', color=vortex.color("blue"), speed=5, x=0, y=ground.scale[1] / 2 + 1, z=0, collider='box')
score = 0
time_limit = 60  # 60 seconds time limit
time_remaining = time_limit
health = 100  # Player health
max_health = 100
health_replenish_amount = 100  # Initial health replenishment amount

# 5. Create score, time, and health labels
score_label = vortex.Label(text=f'Score: {score}', scale=2, x=-0.85, y=0.45, background=True, color=vortex.color("white"))
time_label = vortex.Label(text=f'Time: {time_remaining}', scale=2, x=0.65, y=0.45, background=True, color=vortex.color("white"))
health_label = vortex.Label(text=f'Health: {health}', scale=2, x=0.65, y=0.35, background=True, color=vortex.color("white"))

# 6. Function to update the game
def update():
    global score, time_remaining, health, health_replenish_amount
    time_remaining -= time.dt  # Decrease time remaining
    health -= 0.1  # Decrease health over time
    time_label.text = f'Time: {int(time_remaining)}'
    health_label.text = f'Health: {int(health)}'
    
    # Check for item collection
    for item in collectible_items[:]:
        if player.intersects(item).hit:
            collectible_items.remove(item)
            destroy(item)
            score += 1
            health = min(health + health_replenish_amount, max_health)  # Replenish health
            health_replenish_amount = max(0, health_replenish_amount - 10)  # Decrease health replenishment amount
            score_label.text = f'Score: {score}'
    
    # Check for game over conditions
    if score == num_items:
        print("Congratulations! You collected all items!")
        vortex.app.quit()
    
    if health <= 0:
        print("Game Over! You ran out of health!")
        vortex.app.quit()

# 7. Set the update function
vortex.app.update = update

# 8. Run the game
vortex.run()
