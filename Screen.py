import pygame

class Screen:
    def __init__(self, window, updates, eventListeners, bgColor = None, bgImage = None):
        self.window = window
        self.updates = updates
        self.eventListeners = eventListeners
        self.bgColor = bgColor
        self.bgImage = bgImage

    def update(self):
        if self.bgColor:
            self.window.fill(self.bgColor)
        if self.bgImage:
            self.window.blit(self.bgImage, (0, 0))
        for update in self.updates:
            update.update()

    def handleEvent(self, event):
        for listener in self.eventListeners:
            listener.handleEvent(event)

