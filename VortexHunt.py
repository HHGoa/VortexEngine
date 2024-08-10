from Engine.Vortex import Vortex
from Engine.Vortex import *
import random
import math

# Initialize Vortex
vortex = Vortex(PrivateKey="Your_private_key")

# 1. Create the game environment with an infinite ground
ground = vortex.Object(model='plane', scale=(1000, 0.1, 1000), color=vortex.color("green"), collider='box')
background = vortex.Object(model='quad', scale=(50, 25, 1), x=0, y=12.5, z=-25, color=vortex.color("sky"))

# 2. Initialize game state
player = vortex.firstPersonController(model='cube', color=vortex.color("blue"), speed=5)
targets = []
projectiles = []
score = 0
score_label = vortex.Label(text=f'Score: {score}', scale=2, x=-0.85, y=0.45, background=True, color=vortex.color("black"))

# 3. Create targets with health
def create_target():
    x = random.uniform(-50, 50)
    y = random.uniform(1, 5)
    z = random.uniform(-50, 50)
    health = random.randint(1, 3)  # Random health between 1 and 3
    target = vortex.Object(model='sphere', x=x, y=y, z=z, scale=1, color=vortex.color("red"), collider='box')
    target.health = health
    targets.append(target)

for _ in range(10):
    create_target()

# 4. Function to shoot projectiles towards the aimed direction
def shoot():
    # Calculate direction based on player aim (center screen)
    direction = player.forward

    # Create the projectile at the player's position
    projectile = vortex.Object(model='cube', x=player.x, y=player.y + 1, z=player.z, scale=0.2, color=vortex.color("yellow"), collider='box')
    # Normalize the direction vector
    length = math.sqrt(direction.x**2 + direction.y**2 + direction.z**2)
    projectile.dx = direction.x / length
    projectile.dy = direction.y / length
    projectile.dz = direction.z / length
    projectile.gravity = -0.01  # Gravity effect
    projectile.life = 60  # lifespan of the projectile (60 frames)
    projectiles.append(projectile)

# 5. Function to update the game
def update():
    global score
    for projectile in projectiles[:]:
        projectile.x += projectile.dx
        projectile.y += projectile.dy
        projectile.z += projectile.dz
        projectile.dy += projectile.gravity  # Apply gravity effect
        projectile.life -= 1
        if projectile.life <= 0:
            destroy(projectile)
            projectiles.remove(projectile)
        else:
            for target in targets[:]:
                if target.intersects(projectile).hit:
                    destroy(projectile)
                    projectiles.remove(projectile)
                    target.health -= 1
                    if target.health <= 0:
                        destroy(target)
                        targets.remove(target)
                        score += 20  # Increase score for destroying a target
                    else:
                        score += 2  # Increase score for hitting a target
                    score_label.text = f'Score: {score}'
                    break

    # Spawn new targets periodically
    if len(targets) < 10:
        create_target()

# 6. Set the update function
vortex.app.update = update

# 7. Handle shooting input
def input(key):
    if key == 'left mouse down':
        shoot()

vortex.app.input = input

# 8. Run the game
vortex.run()
