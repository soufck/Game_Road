import pygame

green = (70, 200, 50)
white = (255, 255, 254)
width_line = 10
heing_lines = 50

def main():
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    road_coord = (160, 0, 480, height)

    line_move = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.time.Clock().tick(120)

        screen.fill((green))

        pygame.draw.rect(screen, (79, 80, 85), road_coord)

        line_move += 4

        if line_move >= heing_lines * 1.5:
            line_move = 0

        for y in range(0, height, int(heing_lines * 1.5)):
            pygame.draw.rect(screen, white, (315, y + line_move, width_line, heing_lines))
            pygame.draw.rect(screen, white, (475, y + line_move, width_line, heing_lines))

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
