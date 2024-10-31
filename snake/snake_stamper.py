import random
import turtle
from graphic.turtle_screen import ScreenManager, ScreenConfig

INITIAL_DELAY = 300
DELAY = 300
WIDTH = 800
HEIGHT = 600
FOOD_SIZE = 32  # the dimensions of the image
FOOD_COUNT = 10
FOOD_SHAPE = "foodShape"
FOOD_FILE = "assets/snake-food-32x32.gif"
FOOD_COLOR = "red"
BG_FILE = "assets/bg2.gif"
SNAKE_SIZE = 20
SNAKE_SHAPE = "circle"
SNAKE_COLOR = "#009ef1"
SNAKE_HEAD_FILE = "assets/snake-head-20x20.gif"
high_score = 0

offsets = {
    "up": (0, SNAKE_SIZE),
    "down": (0, -SNAKE_SIZE),
    "right": (SNAKE_SIZE, 0),
    "left": (-SNAKE_SIZE, 0)
}


def load_high_score():
    global high_score
    try:
        with open("scores.txt", "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        pass


def save_high_score():
    try:
        with open("scores.txt", "w") as file:
            file.write(str(high_score))
    finally:
        print("score saved")


def bind_direction_keys():
    scr_mgr.bind_keypress(lambda: set_snake_direction("up"), "Up")
    scr_mgr.bind_keypress(lambda: set_snake_direction("down"), "Down")
    scr_mgr.bind_keypress(lambda: set_snake_direction("left"), "Left")
    scr_mgr.bind_keypress(lambda: set_snake_direction("right"), "Right")
    scr_mgr.bind_keypress(lambda: terminate("user"), "Escape")


def terminate(reason):
    print(f"terminating due to {reason}")
    save_high_score()
    scr_mgr.terminate()
    # screen.bye()


def set_snake_direction(new_direction):
    global direction
    if (new_direction == "up" and direction == "down" or
            new_direction == "down" and direction == "up"
            or new_direction == "right" and direction == "left"
            or new_direction == "left" and direction == "right"):
        reset()
    direction = new_direction


load_high_score()

scr_mgr = ScreenManager(ScreenConfig(bg_file=BG_FILE))
scr_mgr.register_shape(*[FOOD_FILE, SNAKE_HEAD_FILE])
bind_direction_keys()

snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
direction = "up"
score = 0

food_pos = scr_mgr.get_random_pos(FOOD_SIZE)


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    # print(f"dist between {pos1} and {pos2}")
    dist = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagoras' Theorem
    return dist


def food_collision():
    global food_pos, DELAY, score, high_score
    # d = distance(snake[-1], food_pos)
    # print(f"distance is {d}")
    if distance(snake[-1], food_pos) < 20:
        food_pos = scr_mgr.get_random_pos(FOOD_SIZE)
        food.goto(food_pos)
        DELAY = int(DELAY * 0.9)
        score += 1
        if high_score < score:
            high_score = score
            save_high_score()
            # save high score now, async
        return True
    return False


def game_loop():
    global snake
    stamper.clearstamps()
    x, y = offsets[direction]
    new_stamp = snake[-1].copy()
    new_stamp[0] += x
    new_stamp[1] += y
    if not move_valid(new_stamp[0], new_stamp[1]):
        reset()
    else:
        snake.append(new_stamp)
        if not food_collision():
            snake.pop(0)
        stamper.shape(SNAKE_HEAD_FILE)
        stamper.goto(snake[-1][0], snake[-1][1])
        stamper.stamp()
        stamper.shape(SNAKE_SHAPE)
        for segment in snake[:-1]:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()
        scr_mgr.update_scr(game_loop, f"Snake Game, Score: {score}, high score: {high_score}")


def move_valid(x, y):
    x_bounds = (- WIDTH / 2, WIDTH / 2)
    y_bounds = (- HEIGHT / 2, HEIGHT / 2)
    if x < x_bounds[0] or x > x_bounds[1] \
            or y < y_bounds[0] or y > y_bounds[1]:
        print(f"move to {x},{y} is outside screen")
        return False
    if (x, y) in snake:
        print(f"move to {x},{y} is inside the snake")
        return False
    return True


def reset():
    global score, snake, direction, food_pos, food, DELAY, high_score
    DELAY = INITIAL_DELAY
    high_score = max(score, high_score)
    score = 0
    snake = [[0, 0], [SNAKE_SIZE, 0], [SNAKE_SIZE * 2, 0], [SNAKE_SIZE * 3, 0]]
    direction = "up"
    food_pos = scr_mgr.get_random_pos(FOOD_SIZE)
    food.goto(food_pos)
    game_loop()


def setup_turtle(shape, color):
    trt = turtle.Turtle()
    trt.shape(shape)
    trt.color(color)

    trt.penup()
    return trt


stamper = turtle.Turtle()
stamper.shape(SNAKE_SHAPE)
stamper.color(SNAKE_COLOR)
stamper.penup()

food = turtle.Turtle()

food.shape(FOOD_FILE)
food.color(FOOD_COLOR)
food.shapesize(FOOD_SIZE / 20)
food.penup()

reset()

turtle.done()
