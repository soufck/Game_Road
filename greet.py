import pygame
import sqlite3

green = (70, 200, 50)


class GreatingWindow:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Игра Машинки")

    def show_greating(self):
        self.screen.fill(green)
        self.message_to_screen("Добро пожаловать в игру Машинки", (0, 0, 0), -100, size="large")
        self.button("Начать игру", 150, 450, 100, 50, (0, 0, 0), (0, 255, 0))
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
            elif click[0] == 1:
                return True
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
