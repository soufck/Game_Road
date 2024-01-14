import pygame
import random

green = (70, 200, 50)
white = (255, 255, 254)
width_line = 10
heing_lines = 50


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
    def __init__(self, lane):
        pygame.sprite.Sprite.__init__(self)

        num = random.randint(1, 3)
        self.image = pygame.image.load("images/car" + str(num) + ".png")
        self.image = pygame.transform.scale(self.image, (80, 150))

        self.rect = self.image.get_rect()
        self.rect.centerx = lane
        self.rect.top = -80

        self.moving = True

    def update(self):
        if self.moving:
            self.rect.y += 4

    def stop(self):
        self.moving = False


def main():
    moving = True
    pygame.init()
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)

    car_player_group = pygame.sprite.Group()
    other_car_group = pygame.sprite.Group()
    player_x = 400
    player = CarPlayer(player_x)
    car_player_group.add(player)

    road_coord = (160, 0, 480, height)

    line_move = 0

    enemy_spawn_timer = 0
    enemy_spawn_interval = 900

    running = True
    while running:
        if moving:
            line_move += 4
            current_time = pygame.time.get_ticks()
            if current_time - enemy_spawn_timer > enemy_spawn_interval:
                enemy_spawn_timer = current_time
                num_enemies = random.randint(0, 2)
                for _ in range(num_enemies):
                    lane = random.choice([240, 400, 560])
                    enemy_car = EnemyCar(lane)
                    other_car_group.add(enemy_car)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        player.move(event.key)

        pygame.time.Clock().tick(120)

        screen.fill(green)

        pygame.draw.rect(screen, (79, 80, 85), road_coord)

        if not moving:
            line_move = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if line_move >= heing_lines * 1.3:
            line_move = 0

        for y in range(0, height, int(heing_lines * 1.5)):
            pygame.draw.rect(screen, white, (315, y + line_move, width_line, heing_lines))
            pygame.draw.rect(screen, white, (475, y + line_move, width_line, heing_lines))

        if pygame.sprite.groupcollide(car_player_group, other_car_group, False, False):
            moving = False
            for car in other_car_group:
                car.stop()
            x = player.get_x()
            image_boom = pygame.image.load("images/boom.png")
            image_boom = pygame.transform.scale(image_boom, (80, 150))
            screen.blit(image_boom, (x, 440, 100, 100))

        car_player_group.update()
        other_car_group.update()
        car_player_group.draw(screen)
        other_car_group.draw(screen)

        if pygame.sprite.groupcollide(car_player_group, other_car_group, False, False):
            moving = False
            for car in other_car_group:
                car.stop()

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
