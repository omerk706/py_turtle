import random
import turtle

INITIAL_DELAY = 300
DELAY = 300
WIDTH = 800
HEIGHT = 600
FOOD_SIZE = 10
SNAKE_SIZE = 15
FOOD_COUNT = 10

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "right": (20, 0),
    "left": (-20, 0)
}


def bind_direction_keys():
    screen.onkeypress(lambda: set_snake_direction("up"), "Up")
    screen.onkeypress(lambda: set_snake_direction("down"), "Down")
    screen.onkeypress(lambda: set_snake_direction("left"), "Left")
    screen.onkeypress(lambda: set_snake_direction("right"), "Right")
    screen.onkeypress(lambda: terminate("user"), "Escape")


def terminate(reason):
    global screen
    print(f"terminating due to {reason}")
    screen.bye()


def set_snake_direction(newDirection):
    global direction
    if (newDirection == "up" and direction == "down" or
            newDirection == "down" and direction == "up"
            or newDirection == "right" and direction == "left"
            or newDirection == "left" and direction == "right"):
        reset()
    direction = newDirection


def setup_screen():
    scr = turtle.Screen()
    # Create a window where we will do our drawing.
    scr.setup(WIDTH, HEIGHT)
    # Set the dimensions of the Turtle Graphics window.
    scr.title("snake")
    scr.bgcolor("pink")
    scr.tracer(0)
    return scr


screen = setup_screen()
screen.listen()
bind_direction_keys()

snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
direction = "up"
score = 0


def get_random_food_pos():
    x = random.randint(int(-(WIDTH - 20) / 2 - FOOD_SIZE), (int)((WIDTH - 20) / 2 + FOOD_SIZE))
    y = random.randint(int(-(HEIGHT - 20) / 2 - FOOD_SIZE), int((HEIGHT - 20) / 2 + FOOD_SIZE))
    print(f"food will be placed at {x},{y}")
    return x, y


food_pos = get_random_food_pos()


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    # print(f"dist between {pos1} and {pos2}")
    dist = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5  # Pythagoras' Theorem
    return dist


def food_collision():
    global food_pos, DELAY, score
    d = distance(snake[-1], food_pos)
    # print(f"distance is {d}")
    if distance(snake[-1], food_pos) < 20:
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        DELAY = int(DELAY * 0.9)
        score += 1
        return True
    return False


def game_loop():
    global snake
    stamper.clearstamps()
    x, y = offsets[direction]
    newStamp = snake[-1].copy()
    newStamp[0] += x
    newStamp[1] += y
    if not move_valid(newStamp[0], newStamp[1]):
        reset()
    else:
        snake.append(newStamp)
        if not food_collision():
            snake.pop(0)
        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()

        screen.title(f"Snake Game, Score: {score}")
        screen.update()
        screen.ontimer(game_loop, DELAY)


def pickDirection():
    if (direction == "right" or direction == "left"):
        return "up"
    if (direction == "up" or "direction" == "down"):
        return "left"


def change_direction(newDirection):
    global direction
    if (newDirection == "up" and direction == "down" or
            newDirection == "down" and direction == "up"
            or newDirection == "right" and direction == "left"
            or newDirection == "left" and direction == "right"):
        reset()
    direction = newDirection


def move_valid(x, y):
    xBounds = (- WIDTH / 2, WIDTH / 2)
    yBounds = (- HEIGHT / 2, HEIGHT / 2)
    if x < xBounds[0] or x > xBounds[1] \
            or y < yBounds[0] or y > yBounds[1]:
        print(f"move to {x},{y} is outside screen")
        return False;
    if (x, y) in snake:
        print(f"move to {x},{y} is inside the snake")
        return False
    return True


def reset():
    global score, snake, direction, food_pos, food, DELAY
    DELAY = INITIAL_DELAY
    score = 0
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    game_loop()


def setupTurtle(shape, color):
    trt = turtle.Turtle()
    trt.shape(shape)
    trt.color(color)

    trt.penup()
    return trt


stamper = turtle.Turtle()
stamper.shape("square")
stamper.penup()

# stamper = setupTurtle("square", "red")
# stamper.shapesize(SNAKE_SIZE / 20)
food = turtle.Turtle()
food.shape("circle")
food.color("blue")
food.shapesize(FOOD_SIZE / 20)
food.penup()

# top_left=turtle.Turtle()
# top_left.shape("triangle")
# top_left.color("brown")
# top_left.penup()
# top_left.goto(-HEIGHT/2+20,-WIDTH/2+20)
# top_left.stamp()

# trtl.shapesize()
# trtl.penup()


reset()

turtle.done()
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "right": (20, 0),
    "left": (-20, 0)
}
