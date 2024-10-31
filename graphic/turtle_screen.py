import turtle
import random

class ScreenConfig:
    DELAY = 300  # default screen delay
    WIDTH = 800  # screen width, default 800
    HEIGHT = 600  # screen height, default 600
    BG_COLOR = "cyan"
    TITLE = ""

    def __init__(self, width=WIDTH, height=HEIGHT, delay=DELAY,
                 bg_color=BG_COLOR, bg_file="", title=TITLE):
        self.height = height
        self.width = width
        self.delay = delay
        self.bg_color = bg_color
        self.bg_pic = bg_file
        self.title = title

    def configure_screen(self, scr: turtle.Screen):
        scr.setup(self.width, self.height)
        # Set the dimensions of the Turtle Graphics window.
        scr.title(self.title)
        if self.bg_pic != "":
            scr.bgpic(self.bg_pic)
        else:
            scr.bgcolor(self.bg_color)


class ScreenManager:
    def __init__(self, scr_conf=ScreenConfig()):
        self.screen_conf = scr_conf
        self.updating = 0
        self.screen = turtle.Screen()
        self.screen_conf.configure_screen(self.screen)
        if not self.updating:
            self.screen.tracer(self.updating)
        self.screen.listen()

    def get_random_pos(self, offset: int):
        x = random.randint(int(-(self.screen_conf.width - offset) / 2 - offset),
                           int((self.screen_conf.width - offset) / 2 + offset))
        y = random.randint(int(-(self.screen_conf.height - offset) / 2 - offset),
                           int((self.screen_conf.height - offset) / 2 + offset))
        return x, y

    def register_shape(self, *args):
        for shape in args:
            self.screen.register_shape(shape)

    def bind_keypress(self, fun, key):
        self.screen.onkeypress(fun, key)

    def terminate(self):
        self.screen.bye()

    def update_scr(self, func, title=None):
        if title:
            self.screen.title(title)
        self.screen.update()
        if self.screen_conf.delay > 0:
            self.screen.ontimer(func, self.screen_conf.delay)