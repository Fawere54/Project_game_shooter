import arcade
import random
from arcade.particles import FadeParticle, Emitter, EmitBurst

SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.PASTEL_YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.PEACH),
    arcade.make_soft_circle_texture(8, arcade.color.BABY_BLUE),
    arcade.make_soft_circle_texture(8, arcade.color.ELECTRIC_CRIMSON),
]

SMOKE_TEX = arcade.make_soft_circle_texture(20, arcade.color.LIGHT_GRAY, 255, 80)

def gravity_drag(p):
    p.change_y += -0.03
    p.change_x *= 0.92
    p.change_y *= 0.92


def smoke_mutator(p):
    p.scale_x *= 1.02
    p.scale_y *= 1.02
    p.alpha = max(0, p.alpha - 2)

def create_explosion(x, y):
    emitters = []

    emitters.append(
        Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(80),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=random.choice(SPARK_TEX),
                change_xy=arcade.math.rand_in_circle((0, 0), 9),
                lifetime=random.uniform(0.5, 1.1),
                start_alpha=255,
                end_alpha=0,
                scale=random.uniform(0.35, 0.6),
                mutation_callback=gravity_drag,
            ),
        )
    )

    emitters.append(
        Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(12),
            particle_factory=lambda e: FadeParticle(
                filename_or_texture=SMOKE_TEX,
                change_xy=arcade.math.rand_in_circle((0, 0), 0.6),
                lifetime=random.uniform(1.5, 2.5),
                start_alpha=200,
                end_alpha=0,
                scale=random.uniform(0.6, 0.9),
                mutation_callback=smoke_mutator,
            ),
        )
    )

    return emitters

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Сигма-орбита"
PLAYER_SPEED = 9  # Скорость движения игрока


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


class Button:
    def __init__(self, x, y, width, height, text="", color=()):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self):
        # Рисуем прямоугольник кнопки
        arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y, self.width, self.height), self.color)

        # Рисуем текст
        if self.text:
            arcade.draw_text(self.text, self.x, self.y,
                             arcade.color.WHITE, 20,
                             align="center", anchor_x="center", anchor_y="center")

    def is_clicked(self, x, y):
        """Проверяет, был ли клик по кнопке"""
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2

        return left <= x <= right and bottom <= y <= top


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Создаем фон
        self.bg_game1 = arcade.Sprite("files/bg_space.png", scale=1.0)
        self.bg_game1.center_x = SCREEN_WIDTH // 2
        self.bg_game1.center_y = 700
        self.bg_game1.width = SCREEN_WIDTH
        self.bg_game1.height = 1400

        self.bg_game2 = arcade.Sprite("files/bg_space.png", scale=1.0)
        self.bg_game2.center_x = SCREEN_WIDTH // 2
        self.bg_game2.center_y = 700
        self.bg_game2.width = SCREEN_WIDTH
        self.bg_game2.height = 1400

        self.bg_menu = arcade.Sprite("files/galaxy.jpg", scale=1.0)
        self.bg_menu.center_x = SCREEN_WIDTH // 2
        self.bg_menu.center_y = SCREEN_HEIGHT // 2
        self.bg_menu.width = SCREEN_WIDTH
        self.bg_menu.height = SCREEN_HEIGHT

        self.menu_sprite = arcade.SpriteList()
        self.menu_sprite.append(self.bg_menu)

        # Создаем список для всех спрайтов
        self.bg_game = arcade.SpriteList()
        self.bg_game.append(self.bg_game1)
        self.bg_game.append(self.bg_game2)

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

        self.button_play = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 100, 75, "Играть", (98, 99, 155))

        # Создаем флаги
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.game = False
        self.menu = True

        self.emitters = []

        # Счет
        self.score = 0
        self.miss = 0

        # Создаем 3 врага
        self.create_enemy()
        self.create_enemy()
        self.create_enemy()

    def setup(self):
        self.shoot_sound = arcade.load_sound("files/shoot.wav")
        self.background_music = arcade.load_sound("files/space.ogg")
        self.game_over_sound = arcade.load_sound("files/game_over.wav")
        self.explosion_sound = arcade.load_sound("files/explosion.wav")
        # Включаем фоновую музыку
        if self.background_music:
            self.background_player = self.background_music.play(loop=True, volume=0.3)

    def on_draw(self):
        # Отрисовка всех спрайтов
        self.clear()
        if self.menu:
            self.menu_sprite.draw()
            self.button_play.draw()

        elif self.game:
            self.bg_game.draw()

            for e in self.emitters:
                e.draw()

            self.player_sprites.draw()
            self.bullets_list.draw()
            self.enemy_list.draw()
            self.draw_score()

        else:
            # Экран Game Over с отображением финального счета
            arcade.draw_text("Game Over!", 310, 350, arcade.color.RED, 30)
            arcade.draw_text(f"Final Score: {self.score}",
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2 - 50,
                             arcade.color.WHITE,
                             24,
                             align="center",
                             anchor_x="center")

    def draw_score(self):
        score_text = f"Счет: {self.score}"
        miss_text = f"Пропущено: {self.miss}"

        # arcade.draw_rect_filled(
        #     arcade.rect.XYWH(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, 200, 60),
        #     (54, 187, 245, 255)
        # )

        arcade.draw_text(
            score_text,
            25,
            SCREEN_HEIGHT - 30,
            arcade.color.WHITE,
            30,
            align="center",
            anchor_x="left",
            anchor_y="center",
            bold=True
        )
        arcade.draw_text(
            miss_text,
            25,
            SCREEN_HEIGHT - 70,
            arcade.color.WHITE,
            30,
            align="center",
            anchor_x="left",
            anchor_y="center",
            bold=True
        )

    def on_update(self, delta_time):
        if self.menu:
            pass
        elif self.game:
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
                    self.miss += 1

            if self.miss >= 10:
                if self.background_player:
                    self.background_player.pause()
                if self.game_over_sound:
                    arcade.play_sound(self.game_over_sound, volume=0.5)
                self.game = False

            # Проверяем есть ли столкновение пулей и врагом
            for bullet in self.bullets_list:
                hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if hit_list:
                    bullet.remove_from_sprite_lists()

                    for enemy in hit_list:
                        # ВЗРЫВ В ТОЧКЕ ВРАГА
                        explosion = create_explosion(enemy.center_x, enemy.center_y)
                        self.emitters.extend(explosion)

                        if self.explosion_sound:
                            arcade.play_sound(self.explosion_sound, volume=0.3)

                        enemy.remove_from_sprite_lists()
                        self.score += 10
                        self.create_enemy()

            for enemy in self.enemy_list:
                hit_list = arcade.check_for_collision_with_list(enemy, self.player_sprites)
                if hit_list:
                    enemy.remove_from_sprite_lists()
                    for player in hit_list:
                        player.remove_from_sprite_lists()
                    if self.background_player:
                        self.background_player.pause()
                    if self.game_over_sound:
                        arcade.play_sound(self.game_over_sound, volume=0.5)
                    self.game = False

            self.bg_game1.center_y -= 2
            self.bg_game2.center_y -= 2
            if self.bg_game1.center_y == -100:
                self.bg_game2.center_y = 1300
            if self.bg_game2.center_y == -100:
                self.bg_game1.center_y = 1300

            for e in self.emitters[:]:
                e.update(delta_time)
                if e.can_reap():
                    self.emitters.remove(e)
        else:
            pass

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
        # Создаем лазер при ЛКМ
        if self.menu:
            if self.button_play.is_clicked(x, y):
                self.game = True
                self.menu = False
        elif self.game and button == arcade.MOUSE_BUTTON_LEFT:
            self.bullet = Bullet("files/laser.png", 0.3, 10)
            self.bullet.center_x = self.player_sprite.center_x
            self.bullet.center_y = self.player_sprite.center_y + self.player_sprite.height / 2
            self.bullets_list.append(self.bullet)
            if self.shoot_sound:
                arcade.play_sound(self.shoot_sound, volume=0.5)

    def create_enemy(self):
        self.enemy = Enemy(f"files/enemyShip{random.randint(1, 3)}.png", 0.5, random.randint(3, 5))
        self.enemy.center_x = random.randint(100, SCREEN_WIDTH - 100)
        self.enemy.center_y = 650
        self.enemy_list.append(self.enemy)


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
