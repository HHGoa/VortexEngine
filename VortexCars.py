from Engine.Vortex import Vortex
from Engine.Vortex import *
import random

# Initialize Vortex
vortex = Vortex(PrivateKey="Your_Private_Key")

# 1. Create the game environment with a textured ground
ground_texture = 'road_texture'  # Ensure this texture exists in your assets
ground = vortex.Object(model='plane', scale=(100, 0.1, 100), texture=ground_texture, collider='box')

# Set a background texture
background_texture = 'sky_texture'  # Ensure this texture exists in your assets
background = vortex.Object(model='quad', scale=(50, 25, 1), x=0, y=12.5, z=-25, texture=background_texture)

# 2. Create the car model
car_model = 'car_model'  # Ensure this model exists in your assets
car = vortex.Object(model=car_model, scale=(1, 0.5, 2), x=0, y=0.25, z=0, color=vortex.color("blue"), collider='box')

# 3. Generate random obstacles
num_obstacles = 20
obstacles = []

def create_obstacle():
    x = random.uniform(-45, 45)
    z = random.uniform(5, 95)
    y = ground.scale[1] / 2
    obstacle = vortex.Object(model='cube', scale=(2, 2, 2), x=x, y=y, z=z, color=vortex.color("red"), collider='box')
    obstacles.append(obstacle)

for _ in range(num_obstacles):
    create_obstacle()

# 4. Initialize game state
score = 0
health = 100
max_health = 100
speed = 0.3  # Increase car speed

# 5. Create score and health labels
score_label = vortex.Label(text=f'Score: {score}', scale=2, x=-0.85, y=0.45, background=True, color=vortex.color("white"))
health_label = vortex.Label(text=f'Health: {health}', scale=2, x=0.65, y=0.45, background=True, color=vortex.color("white"))

# 6. Function to handle car movement
def car_controls():
    global speed
    car.z += speed  # Move the car forward continuously
    if held_keys['a']:
        car.x -= 0.2
    if held_keys['d']:
        car.x += 0.2

# 7. Function to update the game
def update():
    global score, health
    car_controls()

    # Update camera position to follow the car
    camera.position = (car.x, car.y + 5, car.z - 10)
    camera.look_at(car.position + Vec3(0, 0, 10))  # Adjust to look ahead of the car

    # Reposition obstacles to simulate infinite ground
    for obstacle in obstacles:
        if car.z - obstacle.z > 50:  # If the obstacle is far behind the car
            obstacle.z += 100  # Reposition it ahead of the car
            obstacle.x = random.uniform(-45, 45)  # Randomize its x-position

    # Check for collision with obstacles
    for obstacle in obstacles:
        if car.intersects(obstacle).hit:
            health -= 10  # Reduce health significantly upon collision
            health_label.text = f'Health: {health}'
            if health <= 0:
                print("Game Over! You crashed!")
                vortex.app.quit()

    # Update score
    score += 1
    score_label.text = f'Score: {score}'

# 8. Set the update function
vortex.app.update = update

# 9. Run the game
vortex.run()

# 10. Create executable using PyShield
if __name__ == "__main__":
    vortex.create_exe_with_pyshield(script_name=__file__, exe_name="VortexGame")
