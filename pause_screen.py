"""Module for showing pause screen."""
import pygame

from text_label import TextLabel

FONT_SIZE_TOP = 48
FONT_SIZE_BOTTOM = 32
FONT_COLOR_TOP = (255, 255, 255)
FONT_COLOR_BOTTOM = (109, 207, 246)
TOP_TEXT = 'GAME PAUSED'
BOTTOM_TEXT = 'PRESS ENTER FOR QUIT OR ESC FOR UNPAUSE'
# Fading factor for the game screenshot
SCREEN_ALPHA = 64

class PauseScreen():
    def __init__(self, scr):
        """Input parameters:
        scr - Surface for drawing."""
        self.scr = scr
        self.refresh_background()

        scr_rect = self.scr.get_rect()

        self.top_label = TextLabel(
            scr=self.scr,
            text=TOP_TEXT,
            color=FONT_COLOR_TOP,
            size=FONT_SIZE_TOP)
        self.top_label.rect.center = (
            scr_rect.centerx,
            scr_rect.centery - FONT_SIZE_TOP // 2)

        self.bottom_label = TextLabel(
            scr=self.scr,
            text=BOTTOM_TEXT,
            color=FONT_COLOR_BOTTOM,
            size=FONT_SIZE_BOTTOM)
        self.bottom_label.rect.center = (
            scr_rect.centerx,
            scr_rect.centery + FONT_SIZE_TOP // 2)

    def refresh_background(self):
        """Makes instant 'screenshot' of the game for further usage
        as a background for pause screen."""
        self.background = pygame.Surface(self.scr.get_size(), 0, self.scr)
        self.background.blit(self.scr, (0, 0))
        self.background.set_alpha(SCREEN_ALPHA)

    def draw(self):
        """Renders previously saved 'screenshot' with some fading effect
        and the text labels with messages."""
        self.scr.fill((0, 0, 0))
        self.scr.blit(self.background, (0, 0))
        self.top_label.draw()
        self.bottom_label.draw()
