import pygame
import os


class Road:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.road_texture = pygame.image.load(os.path.join('road_text.jpg'))
        self.road_y = 0

    def move(self, speed):
        self.road_y = (self.road_y + speed) % self.height

    def draw(self, screen):
        screen.blit(self.road_texture, (0, self.road_y))
        screen.blit(self.road_texture, (0, self.road_y - self.height))


def main():
    pygame.init()

    screen_width = 1280
    screen_height = 853

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    road = Road(screen_width, screen_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        road.move(5)

        screen.fill((255, 255, 255))
        road.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
