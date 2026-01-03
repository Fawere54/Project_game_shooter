import arcade
import random

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Сигма-орбита"
PLAYER_SPEED = 7  # Скорость движения игрока
game = True


class Bullet(arcade.Sprite):
    def __init__(self, filename, scale, speed):
        super().__init__(filename, scale)
        self.change_y = speed

    def update(self):
        # Обновление лазера
        self.center_y += self.change_y

        # Удаляем пулю, если она вышла за верхнюю границу экрана
        if self.bottom > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()


class Enemy(arcade.Sprite):
    def __init__(self, filename, scale, speed):
        super().__init__(filename, scale, angle=180)
        self.speed = speed

    def update(self):
        # Обновление врага
        self.center_y -= self.speed


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Создаем фон
        self.bg_game1 = arcade.Sprite("files/bg_space.jpg", scale=1.0)
        self.bg_game1.center_x = SCREEN_WIDTH // 2
        self.bg_game1.center_y = 700
        self.bg_game1.width = SCREEN_WIDTH
        self.bg_game1.height = 1400

        self.bg_game2 = arcade.Sprite("files/bg_space.jpg", scale=1.0)
        self.bg_game2.center_x = SCREEN_WIDTH // 2
        self.bg_game2.center_y = 700
        self.bg_game2.width = SCREEN_WIDTH
        self.bg_game2.height = 1400

        # Создаем список для всех спрайтов
        self.all_sprites = arcade.SpriteList()
        self.all_sprites.append(self.bg_game1)
        self.all_sprites.append(self.bg_game2)

        # Создаем спрайт игрока
        self.player_sprite = arcade.Sprite("files/Player.png", scale=0.5)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 45

        # Создаем список спрайтов
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        # Создаем списки лазеров и врагов
        self.bullets_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Создаем флаги
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.game = True

        # Создаем 3 врага
        self.create_enemy()
        self.create_enemy()
        self.create_enemy()

    def setup(self):
        pass

    def on_draw(self):
        # Отрисовка всех спрайтов
        self.clear()
        self.all_sprites.draw()
        self.player_sprites.draw()
        self.bullets_list.draw()
        self.enemy_list.draw()
        if not self.game:
            arcade.draw_text("Game Over!", 310, 290, (255, 0, 0), 30)

    def on_update(self, delta_time):
        if self.game:
            # Обновляем позицию игрока в зависимости от нажатых клавиш
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.center_x -= PLAYER_SPEED
            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.center_x += PLAYER_SPEED

            # Ограничиваем движение игрока границами экрана
            if self.player_sprite.left < 0:
                self.player_sprite.left = 0
            if self.player_sprite.right > SCREEN_WIDTH:
                self.player_sprite.right = SCREEN_WIDTH

            # Обновляем все лазеры
            for b in self.bullets_list:
                b.update()

            # Обновляем всех врагов
            for e in self.enemy_list:
                e.update()
                # При выходе за зону видимости создаем нового
                if e.center_y < -100:
                    e.remove_from_sprite_lists()
                    self.create_enemy()

            # Проверяем есть ли столкновение пулей и врагом
            for bullet in self.bullets_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()
                    for enemy in hit_list:
                        enemy.remove_from_sprite_lists()
                        self.create_enemy()

            for enemy in self.enemy_list:
                hit_list = arcade.check_for_collision_with_list(enemy, self.player_sprites)
                if hit_list:
                    enemy.remove_from_sprite_lists()
                    for player in hit_list:
                        player.remove_from_sprite_lists()
                        self.game = False

            self.bg_game1.center_y -= 2
            self.bg_game2.center_y -= 2

            if self.bg_game1.center_y == -100:
                self.bg_game2.center_y = 1300

            if self.bg_game2.center_y == -100:
                self.bg_game1.center_y = 1300
        else:
            arcade.draw_text("Game Over!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (255, 0, 0), 15)


    def on_key_press(self, key, modifiers):
        # Обработка нажатий клавиш для управления игроком
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True

    def on_key_release(self, key, modifiers):
        # Обработка отпускания клавиш
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        # Создаем лазер при ПКМ
        self.bullet = Bullet("files/laser.png", 0.3, 10)
        self.bullet.center_x = self.player_sprite.center_x
        self.bullet.center_y = self.player_sprite.center_y + self.player_sprite.height / 2
        self.bullets_list.append(self.bullet)

    def create_enemy(self):
        self.enemy = Enemy("files/enemyShip1.png", 0.5, random.randint(3, 5))
        self.enemy.center_x = random.randint(100, SCREEN_WIDTH-100)
        self.enemy.center_y = 650
        self.enemy_list.append(self.enemy)


def main():
    global game
    if game:
        game = MyGame()
        game.setup()
        arcade.run()


if __name__ == "__main__":
    main()
