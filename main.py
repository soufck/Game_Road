import pygame
import random

green = (70, 200, 50)
white = (255, 255, 254)
width_line = 10
heing_lines = 50

class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = lane
        self.rect.top = -80

    def update(self):
        self.rect.y += 5


class CarPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.line = 1
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("images/red.png")

        self.image = pygame.transform.scale(image, (80, 150))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def move(self, type_event):
        if type_event == pygame.K_LEFT and self.rect.x > 240:
            self.rect.x -= 160
        if type_event == pygame.K_RIGHT and self.rect.x < 480:
            self.rect.x += 160


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.image = pygame.Surface((80, 120))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = lane
        self.rect.top = -80

    def update(self):
        self.rect.y += 3


def main():
    pygame.init()
    size = width, height = 800, 700
    screen = pygame.display.set_mode(size)

    car_group = pygame.sprite.Group()
    player_x = 400
    player = CarPlayer(player_x, 600)
    car_group.add(player)

    road_coord = (160, 0, 480, height)

    line_move = 0

    enemy_spawn_timer = 0
    enemy_spawn_interval = 1000

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer > enemy_spawn_interval:
            enemy_spawn_timer = current_time
            num_enemies = random.randint(0, 2)
            for _ in range(num_enemies):
                lane = random.choice([240, 400, 560])
                enemy_car = EnemyCar(lane)
                car_group.add(enemy_car)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.move(event.key)

        pygame.time.Clock().tick(120)

        screen.fill(green)

        pygame.draw.rect(screen, (79, 80, 85), road_coord)

        line_move += 4

        if line_move >= heing_lines * 1.3:
            line_move = 0

        for y in range(0, height, int(heing_lines * 1.5)):
            pygame.draw.rect(screen, white, (315, y + line_move, width_line, heing_lines))
            pygame.draw.rect(screen, white, (475, y + line_move, width_line, heing_lines))

        car_group.update()
        car_group.draw(screen)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
