"""Module for showing special screen
while game resources are being loaded."""
import pygame

from text_label import TextLabel

FONT_SIZE = 32
TEXT_COLOR = (109, 207, 246)
SCREEN_COLOR = (8, 0, 51)
TEXT_MESSAGE = 'LOADING UNIVERSE... PLEASE STAND BY'

class LoadingScreen():
    def __init__(self, scr):
        """Input parameters:
        scr - Surface for drawing."""
        self.scr = scr
        self.label = TextLabel(
            scr=self.scr,
            text=TEXT_MESSAGE,
            color=TEXT_COLOR,
            size=FONT_SIZE)
        self.label.rect.center = self.scr.get_rect().center

    def draw(self):
        """Fills the specified surface with solid color and renders
        the text label with message."""
        self.scr.fill(SCREEN_COLOR)
        self.label.draw()
        pygame.display.flip()
