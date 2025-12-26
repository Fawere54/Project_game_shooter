import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Color points"

# Просто используем RGB кортежи напрямую
COLORS = [
    (255, 192, 0),    # #ffc000
    (220, 0, 169),    # #dc00a9
    (0, 101, 172),    # #0065ac
    (34, 173, 0)      # #22ad00
]


class MyGame(arcade.Window):
    def __init__(self, width, height, title, colors):
        super().__init__(width, height, title)
        self.colors = colors  # RGB кортежи

    def setup(self):
        self.points = []
        self.radius = 20

    def on_draw(self):
        self.clear()
        for i, p in enumerate(self.points):
            arcade.draw_circle_filled(p[0], p[1], self.radius,
                                     self.colors[i % len(self.colors)])

    def on_mouse_press(self, x, y, button, modifiers):
        self.points.append([x, y])


def setup_game(width=800, height=600, title="Color points", colors=None):
    game = MyGame(width, height, title, COLORS if colors is None else colors)
    game.setup()
    return game


def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()