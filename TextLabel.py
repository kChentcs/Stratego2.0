import pygame

class TextLabel:
    def __init__(self, s, label, x, y, w, h, font, centered = False, tc = (0,0,0), bc = None):
        self.screen = s
        self.label = label
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.centered = centered
        self.textColor = tc
        self.backgroundColor = bc
        self.font = font
        self.text = font.render(self.label, True, self.textColor)
        self.textRect = self.text.get_rect()

    def update(self):
        if self.backgroundColor:
            pygame.draw.rect(self.screen, self.backgroundColor, [self.x, self.y, self.width, self.height])
        if self.centered:
            self.textRect.center = (self.x, self.y)
        else:
            self.textRect.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.screen.blit(self.text, self.textRect)

    def setText(self, newText):
        self.label = newText
        self.text = self.font.render(self.label, True, self.textColor)