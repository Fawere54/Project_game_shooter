import arcade
import random

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Сигма-орбита"
PLAYER_SPEED = 7  # Скорость движения игрока


class Bullet(arcade.Sprite):
    def __init__(self, filename, scale, speed):
        super().__init__(filename, scale)
        self.change_y = speed  # Движение вверх

    def update(self):
        """Обновление позиции пули"""
        self.center_y += self.change_y

        # Удаляем пулю, если она вышла за верхнюю границу экрана
        if self.bottom > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    def __init__(self, filename, scale, speed):
        super().__init__(filename, scale, angle=180)
        self.speed = speed

    def update(self):
        self.center_y -= self.speed
        if self.bottom < -100:
            self.remove_from_sprite_lists()


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.bg_sprite = arcade.Sprite("files/galaxy.jpg", scale=1.0)
        self.bg_sprite.center_x = SCREEN_WIDTH // 2
        self.bg_sprite.center_y = SCREEN_HEIGHT // 2
        self.bg_sprite.width = SCREEN_WIDTH
        self.bg_sprite.height = SCREEN_HEIGHT

        # Создаем список для всех спрайтов
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.bg_sprite)

        # Создаем спрайт игрока
        self.player_sprite = arcade.Sprite("files/Player.png", scale=0.5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 45

        # Создаем список спрайтов
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        self.bullets_list = arcade.SpriteList()

        self.enemy_list = arcade.SpriteList()

        # Инициализируем флаги управления
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.create_enemy()

    def setup(self):
        """Создание и размещение монет"""
        # Здесь можно добавить создание монет или других объектов
        pass

    def on_draw(self):
        """Отрисовка всех спрайтов"""
        self.clear()
        self.all_sprites.draw()
        self.player_sprites.draw()
        self.bullets_list.draw()
        self.enemy_list.draw()

    def on_update(self, delta_time):
        """Обновляем состояние игры"""
        # Обновляем позицию игрока в зависимости от нажатых клавиш
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.center_x -= PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.center_x += PLAYER_SPEED
        #
        # if self.up_pressed and not self.down_pressed:
        #     self.player_sprite.center_y += PLAYER_SPEED
        # elif self.down_pressed and not self.up_pressed:
        #     self.player_sprite.center_y -= PLAYER_SPEED

        # Ограничиваем движение игрока границами экрана
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        if self.player_sprite.right > SCREEN_WIDTH:
            self.player_sprite.right = SCREEN_WIDTH
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.top > SCREEN_HEIGHT:
            self.player_sprite.top = SCREEN_HEIGHT

        for b in self.bullets_list:
            b.update()

        for e in self.enemy_list:
            e.update()

        for bullet in self.bullets_list:
            # Проверяем столкновение с каждым врагом
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_list:
                # Удаляем пулю при столкновении
                bullet.remove_from_sprite_lists()

                # Удаляем врагов, в которых попали (или наносим урон)
                for enemy in hit_list:
                    enemy.remove_from_sprite_lists()

                    self.create_enemy()

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

    def on_mouse_press(self, x, y, button, modifiers):
        self.bullet = Bullet("files/laser.png", 0.3, 10)
        self.bullet.center_x = self.player_sprite.center_x
        self.bullet.center_y = self.player_sprite.center_y + self.player_sprite.height / 2
        self.bullets_list.append(self.bullet)

    def create_enemy(self):
        self.enemy = Enemy("files/enemyShip1.png", 0.5, random.randint(3, 5))
        self.enemy.center_x = random.randint(100, SCREEN_WIDTH-100)
        self.enemy.center_y = 550
        self.enemy_list.append(self.enemy)



def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
