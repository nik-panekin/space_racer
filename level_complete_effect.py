"""Module for rendering 'level complete' animation effect."""
import pygame

from sliding_label import SlidingLabel, SLIDE_RIGHT
from blinking_label import BlinkingLabel

FONT_SIZE = 48
COLOR_PRIMARY = (0, 84, 166)
COLOR_SECONDARY = (255, 255, 255)
TEXT_MESSAGE = 'LEVEL COMPLETE'
SLIDING_SPEED = 16

class LevelCompleteEffect():
    def __init__(self, scr):
        """Input parameters:
        scr - Surface for drawing."""
        self.scr = scr
        scr_rect = self.scr.get_rect()

        self.incoming_label = SlidingLabel(
            scr=self.scr,
            text=TEXT_MESSAGE,
            color=COLOR_PRIMARY,
            size=FONT_SIZE,
            slide=SLIDE_RIGHT)
        self.incoming_label.set_origin_center((
            -self.incoming_label.rect.width // 2,
            scr_rect.centery))
        self.incoming_label.set_max_progress(
            (scr_rect.width + self.incoming_label.rect.width) // 2)
        self.incoming_label.set_speed(SLIDING_SPEED)
        self.incoming_label.set_repeat(False)

        self.outcoming_label = SlidingLabel(
            scr=self.scr,
            text=TEXT_MESSAGE,
            color=COLOR_PRIMARY,
            size=FONT_SIZE,
            slide=SLIDE_RIGHT)
        self.outcoming_label.set_origin_center(scr_rect.center)
        self.outcoming_label.set_max_progress(
            (scr_rect.width + self.outcoming_label.rect.width) // 2)
        self.outcoming_label.set_speed(SLIDING_SPEED)
        self.outcoming_label.set_repeat(False)

        self.blinking_label = BlinkingLabel(
            scr=self.scr,
            text=TEXT_MESSAGE,
            color=COLOR_PRIMARY,
            second_color=COLOR_SECONDARY,
            size=FONT_SIZE)
        self.blinking_label.rect.center = scr_rect.center
        self.blinking_label.set_repeat(False)
        self.blinking_label.set_speed(1)

    def restart(self):
        """Prepares the animation effect for playing again."""
        self.incoming_label.restart()
        self.outcoming_label.restart()
        self.blinking_label.restart()

    def _get_active_labels(self):
        labels = []

        if self.incoming_label.finished:
            if self.blinking_label.finished:
                labels.append(self.outcoming_label)
            else:
                labels.append(self.blinking_label)
        else:
            labels.append(self.incoming_label)

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
        return self.outcoming_label.finished
