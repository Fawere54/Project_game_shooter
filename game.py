import arcade
import random
from arcade.particles import FadeParticle, Emitter, EmitBurst
from pyglet.graphics import Batch

SPARK_TEX = [
    arcade.make_soft_circle_texture(8, arcade.color.YELLOW),
    arcade.make_soft_circle_texture(8, arcade.color.ORANGE),
    arcade.make_soft_circle_texture(8, arcade.color.RED),
    arcade.make_soft_circle_texture(8, arcade.color.RED_BROWN),
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
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2

        return left <= x <= right and bottom <= y <= top


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.batch = Batch()
        self.pause_text = arcade.Text("Пауза", self.window.width / 2, self.window.height / 2,
                                      arcade.color.WHITE, font_size=40, anchor_x="center", batch=self.batch)
        self.space_text = arcade.Text("Нажми SPACE, чтобы продолжить", self.window.width / 2,
                                      self.window.height / 2 - 50,
                                      arcade.color.WHITE, font_size=20, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)


class TextureButton:
    def __init__(self, texture_path, x, y, width, height):
        texture = arcade.load_texture(texture_path)

        # Вычисляем scale
        scale_x = width / texture.width
        scale_y = height / texture.height
        scale = min(scale_x, scale_y)

        # Создаем спрайт
        self.sprite = arcade.Sprite(texture_path, scale)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.spriteL = arcade.SpriteList()
        self.spriteL.append(self.sprite)

        # Сохраняем размеры для проверки кликов
        self.width = width
        self.height = height

    def draw(self):
        self.spriteL.draw()

    def is_clicked(self, x, y):
        left = self.sprite.center_x - self.width / 2
        right = self.sprite.center_x + self.width / 2
        bottom = self.sprite.center_y - self.height / 2
        top = self.sprite.center_y + self.height / 2

        return left <= x <= right and bottom <= y <= top


class Item:
    def __init__(self, texture_path, x, y, width, height, text):
        texture = arcade.load_texture(texture_path)

        # Вычисляем scale
        scale_x = width / texture.width
        scale_y = height / texture.height
        scale = min(scale_x, scale_y)

        # Создаем спрайт
        self.sprite = arcade.Sprite(texture_path, scale)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.spriteL = arcade.SpriteList()
        self.spriteL.append(self.sprite)

        self.width = width
        self.height = height
        self.text = text
        self.x = x
        self.y = y

    def draw(self):
        self.spriteL.draw()
        arcade.draw_text(self.text, self.x, self.y - self.height // 2,
                             arcade.color.WHITE, 20,
                             align="center", anchor_x="center", anchor_y="top")

    def is_clicked(self, x, y):
        left = self.sprite.center_x - self.width / 2
        right = self.sprite.center_x + self.width / 2
        bottom = self.sprite.center_y - self.height / 2
        top = self.sprite.center_y + self.height / 2

        return left <= x <= right and bottom <= y <= top


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("files/PlayerBlue.png", scale=0.5)
        self.idle_texture = arcade.load_texture("files/PlayerBlue.png")
        self.shoot_textures = [
            arcade.load_texture("files/PlayerBlue_move1.png"),
            arcade.load_texture("files/PlayerBlue_move2.png")
        ]
        self.is_shooting = False
        self.shoot_timer = 0
        self.current_texture_idx = 0
        self.anim_speed = 0.1
        self.anim_timer = 0

    def start_shooting_animation(self):
        self.is_shooting = True
        self.shoot_timer = 0.3
        self.current_texture_idx = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_shooting:
            self.shoot_timer -= delta_time
            self.anim_timer += delta_time
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.current_texture_idx = (self.current_texture_idx + 1) % len(self.shoot_textures)
                self.texture = self.shoot_textures[self.current_texture_idx]
            if self.shoot_timer <= 0:
                self.is_shooting = False
                self.texture = self.idle_texture
        else:
            self.texture = self.idle_texture


class MyGame(arcade.View):
    def __init__(self):
        super().__init__()
        # Создаем флаги
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.game = False
        self.menu = True
        self.shop = False
        self.update = False

        self.emitters = []

        self.skin = "files/skin_blue.png"

        # Счет
        self.money = 0
        self.score = 0
        self.miss = 0

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

        self.bg_game = arcade.SpriteList()
        self.bg_game.append(self.bg_game1)
        self.bg_game.append(self.bg_game2)

        self.bg_menu = arcade.Sprite("files/galaxy.jpg", scale=1.0)
        self.bg_menu.center_x = SCREEN_WIDTH // 2
        self.bg_menu.center_y = SCREEN_HEIGHT // 2
        self.bg_menu.width = SCREEN_WIDTH
        self.bg_menu.height = SCREEN_HEIGHT

        self.menu_sprite = arcade.SpriteList()
        self.menu_sprite.append(self.bg_menu)

        # Создаем спрайт игрока
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 45

        # Создаем список спрайтов
        self.player_sprites = arcade.SpriteList()
        self.player_sprites.append(self.player_sprite)

        self.coin = arcade.Sprite("files/coin.png",scale=1.0)
        self.coin.center_x = 50
        self.coin.center_y = 550
        self.coin.width = 50
        self.coin.height = 50

        self.shop_sprites = arcade.SpriteList()
        self.shop_sprites.append(self.coin)

        # Создаем списки лазеров и врагов
        self.bullets_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.skin_base = Item("files/PlayerBlue.png", 150, 450, 100, 100, "Установлено")
        self.skin_green = Item("files/PlayerGreen.png", 300, 450, 100, 100, "100")
        self.button_play = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 200, 75, "Играть", (98, 99, 155))
        self.button_skin = Button(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 150, 75, "Скины", (98, 99, 155))
        self.button_update = Button(SCREEN_WIDTH - SCREEN_WIDTH // 8, SCREEN_HEIGHT // 2, 150, 75, "Улучшения", (98, 99, 155))
        self.button_reset = Button(400, SCREEN_HEIGHT // 3, 100, 75, "Заново", (98, 99, 155))
        self.button_menu = Button(200, SCREEN_HEIGHT // 3, 100, 75, "В меню", (98, 99, 155))
        self.button_exit_menu = Button(60, 35, 100, 50, "Назад", (98, 99, 155))

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
            self.button_skin.draw()
            self.button_update.draw()

        elif self.shop:
            self.menu_sprite.draw()
            self.shop_sprites.draw()
            self.skin_base.draw()
            self.skin_green.draw()
            self.button_exit_menu.draw()
            arcade.draw_text(self.money,
                              80,
                              537,
                              arcade.color.WHITE,
                              30,
                              align="center",
                              anchor_x="left")

        elif self.update:
            self.menu_sprite.draw()
            self.button_exit_menu.draw()
            self.shop_sprites.draw()
            arcade.draw_text(self.money,
                             80,
                             537,
                             arcade.color.WHITE,
                             30,
                             align="center",
                             anchor_x="left")

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
            arcade.draw_text("В следующий раз повезет!", 200, 350, arcade.color.RED, 30)
            arcade.draw_text(f"Результат: {self.score}",
                             SCREEN_WIDTH // 2,
                             SCREEN_HEIGHT // 2,
                             arcade.color.WHITE,
                             24,
                             align="center",
                             anchor_x="center")
            self.button_reset.draw()
            self.button_menu.draw()

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
            # Анимация игрока
            self.player_sprite.update_animation(delta_time)
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
                        self.score += 1
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

    def reset_game(self):
        # Перезапуск игры с созданием модельки игрока
        self.money += self.score
        self.score = 0
        self.miss = 0
        self.bullets_list.clear()
        self.enemy_list.clear()
        self.emitters.clear()
        self.player_sprites.clear()
        self.player_sprite = Player()
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 45
        self.player_sprites.append(self.player_sprite)
        for i in range(3):
            self.create_enemy()
        if self.background_music and self.background_player:
            self.background_player.play()

    def on_key_press(self, key, modifiers):
        # Пауза
        if key == arcade.key.SPACE and self.game:
            pause_view = PauseView(self)
            self.window.show_view(pause_view)
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
            elif self.button_skin.is_clicked(x, y):
                self.menu = False
                self.shop = True
            elif self.button_update.is_clicked(x, y):
                self.menu = False
                self.update = True
        elif self.shop or self.update:
            if self.button_exit_menu.is_clicked(x, y):
                self.shop = False
                self.update = False
                self.menu = True
        elif self.game and button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.start_shooting_animation()
            self.bullet = Bullet("files/laser.png", 0.3, 10)
            self.bullet.center_x = self.player_sprite.center_x
            self.bullet.center_y = self.player_sprite.center_y + self.player_sprite.height / 2
            self.bullets_list.append(self.bullet)
            if self.shoot_sound:
                arcade.play_sound(self.shoot_sound, volume=0.5)
        else:
            if self.button_reset.is_clicked(x, y):
                self.reset_game()
                self.game = True
                self.menu = False
            elif self.button_menu.is_clicked(x, y):
                self.reset_game()
                self.menu = True
                self.game = False

    def create_enemy(self):
        self.enemy = Enemy(f"files/enemyShip{random.randint(1, 3)}.png", 0.5, random.randint(3, 5))
        self.enemy.center_x = random.randint(100, SCREEN_WIDTH - 100)
        self.enemy.center_y = 650
        self.enemy_list.append(self.enemy)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = MyGame()
    window.show_view(game_view)
    game_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
