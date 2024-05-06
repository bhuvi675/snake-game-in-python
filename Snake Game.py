import turtle as ttl
import tkinter as tk
import random

# Set up the game environment
delay = 0.1
score = 0
high_score = 0
running = False  # Controls whether the game is running

# Initialize the window
window = ttl.Screen()
window.title("Snake Game")
window.bgcolor("black")
window.setup(width=650, height=650)
window.tracer(0)

# Create the snake's head
head = ttl.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Create the food
food = ttl.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(random.randint(-290, 290), random.randint(-290, 290))

# Create the score display
pen = ttl.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 280)
pen.write(f"Score: {score}, High Score: {high_score}", align="center", font=("Consolas", 24, "bold"))

# Define functions for controlling the snake
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# Define function to move the snake
def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

# Define the key bindings for movement
window.listen()
window.onkeypress(go_up, "w")
window.onkeypress(go_down, "s")
window.onkeypress(go_left, "a")
window.onkeypress(go_right, "d")

# Define the snake body
segments = []

# Create a flag to check if the game is running
running = False

# Define a function to update the score and high score display
def update_score():
    pen.clear()
    pen.write(f"Score: {score}, High Score: {high_score}", align="center", font=("Consolas", 24, "bold"))

# Define a function to handle game over
def game_over():
    global running
    running = False
    pen.goto(0, 0)
    pen.color("red")
    pen.write("GAME OVER", align="center", font=("Consolas", 36, "bold"))

# Define a function to restart the game
def restart_game():
    global running, score, delay
    score = 0
    delay = 0.1
    pen.goto(0, 280)
    pen.color("white")
    pen.clear()
    update_score()
    head.goto(0, 0)
    head.direction = "stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()
    running = True

# Define a function to randomly place food
def place_food():
    food.goto(random.randint(-290, 290), random.randint(-290, 290))

# Define a function to handle the game loop
def game_loop():
    global score, high_score, delay

    if not running:
        return

    window.update()

    # Check if the snake hits the wall
    if abs(head.xcor()) > 320 or abs(head.ycor()) > 320:
        game_over()
        return

    # Check if the snake eats the food
    if head.distance(food) < 20:
        place_food()

        # Add a segment to the snake
        new_segment = ttl.Turtle()
        new_segment.shape("square")
        new_segment.color("green")
        new_segment.penup()
        segments.append(new_segment)

        # Increase the score
        score += 10
        if score > high_score:
            high_score = score

        # Update the score display
        update_score()

        # Speed up the game
        delay -= 0.001

    # Move the snake's segments
    for i in range(len(segments) - 1, 0, -1):
        segments[i].goto(segments[i - 1].xcor(), segments[i - 1].ycor())
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # Move the snake
    move()

    # Check if the snake collides with itself
    for segment in segments:
        if segment.distance(head) < 20:
            game_over()
            return

    # Call the game loop again after the delay
    ttl.ontimer(game_loop, int(delay * 1000))

# Define a function to start the game
def start_game():
    global running
    running = True
    game_loop()

# Create a Tkinter window
root = tk.Tk()
root.title("Snake Game Controls")

# Create start and restart buttons
start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack(pady=10)

restart_button = tk.Button(root, text="Restart Game", command=restart_game)
restart_button.pack(pady=10)

# Start the Tkinter mainloop
root.mainloop()

# Main turtle mainloop
window.mainloop()
