from Engine.Vortex import Vortex
from Engine.Vortex import *

vortex = Vortex(PrivateKey="0x0ca8a8b46e83400f942a5a6889f88896dcfe5d71619a0a8a23533d0293c7c9f5")

# 1. Build 4 walls
ceiling = vortex.Object(model='quad', x=0, y=4, scale=(16, 0.2), collider='box', color=vortex.color("orange"))
left_wall = vortex.Object(model='quad', x=-7.2, y=0, scale=(0.2, 10), collider='box', color=vortex.color("orange"))
right_wall = vortex.Object(model='quad', x=7.2, y=0, scale=(0.2, 10), collider='box', color=vortex.color("orange"))

# 2. Create a ball
ball = vortex.Object(model='circle', scale=0.2, collider='box', dx=0.05, dy=0.05)

# 3. Create a paddle
paddle = vortex.Object(model='quad', x=0, y=-3.5, scale=(2, 0.2), collider='box', color=vortex.color("orange"))

# 4. Lay out bricks
bricks = []
for x_pos in range(-65, 75, 10):
    for y_pos in range(3, 7):
        brick = vortex.Object(model='quad', x=x_pos/10, y=y_pos/3, scale=(0.9, 0.3), collider='box', color=vortex.color("red"))
        bricks.append(brick)

# 5. Initialize score
score = 0

# 6. Function to update the ball speed based on score
def update_ball_speed():
    global score
    speed_multiplier = 1 + (score / 10) * 0.1  # Adjust the factor as needed
    ball.dx = 0.05 * speed_multiplier if ball.dx > 0 else -0.05 * speed_multiplier
    ball.dy = 0.05 * speed_multiplier if ball.dy > 0 else -0.05 * speed_multiplier

# 7. Move the ball so it bounces off the walls
def update():
    global score
    ball.x += ball.dx
    ball.y += ball.dy
    paddle.x += (held_keys['right arrow'] - held_keys['left arrow']) * time.dt * 5
    
    hit_info = ball.intersects()
    if hit_info.hit:
        if hit_info.entity == left_wall or hit_info.entity == right_wall:
            ball.dx = -ball.dx
        if hit_info.entity == ceiling:
            ball.dy = -ball.dy
        if hit_info.entity in bricks:
            destroy(hit_info.entity)
            bricks.remove(hit_info.entity)
            ball.dy = -ball.dy
            score += 1  # Increment score
            update_ball_speed()  # Update ball speed based on new score
        if hit_info.entity == paddle:
            ball.dy = -ball.dy
            ball.dx = 0.05 * (ball.x - paddle.x)
    
    if ball.y < -5:
        message = vortex.Label(text='You LOST', scale=2, origin=(0, 0), background=True, color=vortex.color("blue"))
        vortex.UpdateBlock()
        print("working..")
        application.pause()
    
    if len(bricks) == 0:
        message = vortex.Label(text='You WON', scale=2, origin=(0, 0), background=True, color=vortex.color("blue"))
        application.pause()


vortex.run()
