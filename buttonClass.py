import pygame
from protocol import BLACK, GRAY, LIGHT_GRAY


class Button:
    def __init__(self, x, y, width, height, text=None, text_colour=BLACK, colour=GRAY, highlighted_colour=LIGHT_GRAY,
                 function=None, params=None):
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.text_colour = text_colour
        self.colour = colour
        self.highlighted = False
        self.highlighted_colour = highlighted_colour
        self.function = function
        self.params = params

    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        self.image.fill(self.highlighted_colour if self.highlighted else self.colour)
        if self.text:
            self.draw_text(self.text)
        window.blit(self.image, self.pos)

    def click(self):
        if self.params == 0 or self.params:
            self.function(self.params)
        else:
            self.function()

    def draw_text(self, text: str):
        font = pygame.font.SysFont('Arial', 30, bold=1)
        text = font.render(text, False, self.text_colour)
        width, height = text.get_size()
        x = (self.width - width) // 2
        y = (self.height - height) // 2
        self.image.blit(text, (x, y))
