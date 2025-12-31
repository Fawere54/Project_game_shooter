import arcade

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Сигма-орбита"
PLAYER_SPEED = 5  # Скорость движения игрока


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Создаем спрайт игрока
        self.player_sprite = arcade.Sprite("files/Player.png", scale=0.5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2

        # Создаем список спрайтов
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        # Инициализируем флаги управления
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        """Создание и размещение монет"""
        # Здесь можно добавить создание монет или других объектов
        pass

    def on_draw(self):
        """Отрисовка всех спрайтов"""
        self.clear()
        self.player_sprites.draw()

    def on_update(self, delta_time):
        """Обновляем состояние игры"""
        # Обновляем позицию игрока в зависимости от нажатых клавиш
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.center_x -= PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.center_x += PLAYER_SPEED

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.center_y += PLAYER_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.center_y -= PLAYER_SPEED

        # Ограничиваем движение игрока границами экрана
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш для управления игроком"""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        """Обработка отпускания клавиш"""
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()