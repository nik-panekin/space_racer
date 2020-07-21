"""Module for rendering 'game over' animation effect."""
import pygame

from sliding_label import SlidingLabel, SLIDE_BOTTOM
from blinking_label import BlinkingLabel

FONT_SIZE = 92
COLOR_PRIMARY = (121, 0, 0)
COLOR_SECONDARY = (242, 108, 79)
TEXT_MESSAGE = 'GAME OVER'
SLIDING_SPEED = 4

class GameOverEffect():
    def __init__(self, scr):
        """Input parameters:
        scr - Surface for drawing."""
        self.scr = scr
        scr_rect = self.scr.get_rect()

        self.sliding_label = SlidingLabel(
            scr=self.scr,
            text=TEXT_MESSAGE,
            color=COLOR_PRIMARY,
            size=FONT_SIZE,
            slide=SLIDE_BOTTOM)
        self.sliding_label.set_origin_center((
            scr_rect.centerx,
            -self.sliding_label.rect.height // 2))
        self.sliding_label.set_max_progress(
            (scr_rect.height + self.sliding_label.rect.height) // 2)
        self.sliding_label.set_speed(SLIDING_SPEED)
        self.sliding_label.set_repeat(False)

        self.blinking_label = BlinkingLabel(
            scr=self.scr,
            text=TEXT_MESSAGE,
            color=COLOR_PRIMARY,
            second_color=COLOR_SECONDARY,
            size=FONT_SIZE)
        self.blinking_label.rect.center = scr_rect.center
        self.blinking_label.set_repeat(False)
        self.blinking_label.set_speed(0.25)

    def restart(self):
        """Prepares the animation effect for playing again."""
        self.sliding_label.restart()
        self.blinking_label.restart()

    def _get_active_labels(self):
        labels = []

        if self.sliding_label.finished:
            labels.append(self.blinking_label)
        else:
            labels.append(self.sliding_label)

        return labels

    def update(self):
        """Updates screen positions for text labels."""
        for label in self._get_active_labels():
            label.update()

    def draw(self):
        """Renders the animation effect to the specified surface."""
        for label in self._get_active_labels():
            label.draw()

    def finished(self):
        """Returns True if the animation effect is completed and
        False if it is still in progress."""
        return self.blinking_label.finished
