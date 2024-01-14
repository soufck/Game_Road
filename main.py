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


def main():
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    road_coord = (160, 0, 480, height)

    line_move = 0

    enemy_spawn_timer = 0
    enemy_spawn_interval = 1000

    all_sprites = pygame.sprite.Group()  

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer > enemy_spawn_interval:
            enemy_spawn_timer = current_time
            num_enemies = random.randint(0, 2)
            for _ in range(num_enemies):
                lane = random.choice([240, 400, 560])
                enemy_car = EnemyCar(lane)
                all_sprites.add(enemy_car)

        all_sprites.update()

        pygame.time.Clock().tick(120)

        screen.fill((green))

        pygame.draw.rect(screen, (79, 80, 85), road_coord)

        line_move += 2

        if line_move >= heing_lines * 2:
            line_move = 0

        for y in range(0, height, heing_lines * 2):
            pygame.draw.rect(screen, white, (315, y + line_move, width_line, heing_lines))
            pygame.draw.rect(screen, white, (475, y + line_move, width_line, heing_lines))

        all_sprites.draw(screen)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

