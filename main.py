import pygame
import random

green = (70, 200, 50)
white = (255, 255, 254)
width_line = 10
heing_lines = 50
boom = pygame.transform.scale(pygame.image.load("images/boom.png"), (360, 120))
stop = True


class GreatingWindow:
    def __init__(self):
        self.game = 0
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Игра Машинки")

    def show_greating(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill(green)
            self.message_to_screen("Добро пожаловать в игру Машинки", (0, 0, 0), -100, size="large")
            self.button("Начать игру", 150, 450, 100, 50, (0, 0, 0), (0, 255, 0), self.game_loop)
            self.button("Правила", 550, 450, 100, 50, (0, 0, 0), (0, 0, 255), self.show_rules)

            pygame.display.update()

    def message_to_screen(self, text, color, y_displace=0, size="small"):
        font = pygame.font.SysFont(None, 55)
        text_surf, text_rect = self.text_objects(text, font)
        text_rect.center = (self.screen_width / 2), (self.screen_height / 2) + y_displace
        self.screen.blit(text_surf, text_rect)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, (255, 255, 255))
        return text_surface, text_surface.get_rect()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))
            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))

        small_text = pygame.font.SysFont(None, 20)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(text_surf, text_rect)

    def show_rules(self):
        pass
        # conn = sqlite3.connect('rules.db')
        # cursor = conn.cursor()
        # cursor.execute('SELECT * FROM rules')
        # rules = cursor.fetchall()
        # for rule in rules:
        #     print(rule)
        # conn.close()

    def game_loop(self):
        main()


def loop():
    pygame.init()
    greet = GreatingWindow()
    greet.show_greating()


class Button:
    def __init__(self, x, y, size_x, size_y, image, image_hover=None, group_sprite=None):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        if image_hover:
            self.image_hover = pygame.image.load(image_hover)
            self.image_hover = pygame.transform.scale(self.image_hover, (size_x, size_y))
        self.is_hover = False

    def draw(self, screen):
        if self.is_hover:
            images = self.image_hover
        else:
            images = self.image
        screen.blit(images, (self.x, self.y))

    def check_pos(self, mouse_pos):
        self.is_hover = self.rect.collidepoint(mouse_pos)

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            main()


class ButtonStop(Button):
    def click(self, event):
        pass


class CarPlayer(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/red.png")

        self.image = pygame.transform.scale(self.image, (80, 150))

        self.rect = self.image.get_rect()
        self.rect.center = [x, 600]

    def move(self, type_event):
        if type_event == pygame.K_LEFT and self.rect.x > 240:
            self.rect.x -= 160
        if type_event == pygame.K_RIGHT and self.rect.x < 480:
            self.rect.x += 160

    def get_x(self):
        return self.rect.x


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, lane, speed):
        pygame.sprite.Sprite.__init__(self)

        num = random.randint(1, 3)
        self.image = pygame.image.load("images/car" + str(num) + ".png")
        self.image = pygame.transform.scale(self.image, (80, 150))

        self.rect = self.image.get_rect()
        self.rect.centerx = lane
        self.rect.top = -80

        self.pause = False

        self.speed = speed

        self.moving = True

    def update(self):
        if self.moving and not self.pause:
            self.rect.y += self.speed

    def stop_end(self):
        self.moving = False

    def stop(self):
        if not self.pause:
            self.pause = True
        else:
            self.pause = False

    def get_y(self):
        return self.rect.y


def main():
    moving = True
    stop = True
    pygame.init()

    def drow_score(screen, score):
        font = pygame.font.Font(None, 50)
        text = font.render(str(score), True, (0, 0, 0))
        screen.blit(text, (40, 50))

    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)

    car_player_group = pygame.sprite.Group()
    other_car_group = pygame.sprite.Group()
    player_x = 400
    player = CarPlayer(player_x)
    car_player_group.add(player)

    road_coord = (160, 0, 480, height)

    score = 0
    cod_score = 4000
    timer = 0

    speed_car = 4

    line_move = 0

    enemy_spawn_timer = 0
    enemy_spawn_interval = 1500

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - timer > 1000 and moving and stop:
            timer = current_time
            score += 200
            for car in other_car_group:
                if car.rect.y > 800:
                    car.kill()
            if score >= cod_score:
                cod_score += 4000
                speed_car += 1

                if enemy_spawn_interval > 600 and cod_score % 8000 == 0:
                    enemy_spawn_interval -= 200

                print(cod_score)

        if moving:
            if stop:
                line_move += 4
                if current_time - enemy_spawn_timer > enemy_spawn_interval:
                    enemy_spawn_timer = current_time
                    num_enemies = random.randint(0, 2)
                    for _ in range(num_enemies):
                        lane = random.choice([240, 400, 560])
                        enemy_car = EnemyCar(lane, speed_car)
                        other_car_group.add(enemy_car)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN and stop:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.move(event.key)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        button_stop = Button(200, 200, 400, 400, "images/stop.png")
                        if stop:
                            stop = False
                            for car in other_car_group:
                                car.stop()
                        else:
                            stop = True
                            for car in other_car_group:
                                car.stop()

        pygame.time.Clock().tick(120)

        screen.fill(green)

        pygame.draw.rect(screen, (79, 80, 85), road_coord)

        if not moving:
            line_move = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                buttun.click(event)

        if line_move >= heing_lines * 2:
            line_move = 0

        for y in range(-50, height, int(heing_lines * 2)):
            pygame.draw.rect(screen, white, (315, y + line_move, width_line, heing_lines))
            pygame.draw.rect(screen, white, (475, y + line_move, width_line, heing_lines))

        car_player_group.update()
        other_car_group.update()
        car_player_group.draw(screen)
        other_car_group.draw(screen)

        if pygame.sprite.groupcollide(car_player_group, other_car_group, False, False):
            moving = False
            for car in other_car_group:
                car.stop_end()
            x = player.get_x()
            screen.blit(boom, (x - 150, 530))
            buttun = Button(200, 200, 400, 200, "images/restart_0.png", image_hover="images/restart.png")
            buttun.check_pos(pygame.mouse.get_pos())
            buttun.draw(screen)

        if not stop:
            button_stop.draw(screen)

        drow_score(screen, score)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    loop()
