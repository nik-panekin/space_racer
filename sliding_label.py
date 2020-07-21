"""Module introduces SlidingLabel class which can render moving
on-screen text."""
import pygame

from text_label import DEFAULT_COLOR, DEFAULT_SIZE, TYPEFACE_NORMAL
from animated_label import AnimatedLabel

SLIDE_RIGHT = 0
SLIDE_LEFT = 1
SLIDE_TOP = 2
SLIDE_BOTTOM = 3

class SlidingLabel(AnimatedLabel):
    """This type of label implements moving animation effect. The text
    can slide from left to right, right to left, top to bottom and
    bottom to top.
    Note: don't change self.rect attribute directly,
    use set_origin() instead."""
    def __init__(self, scr, text='', color=DEFAULT_COLOR, size=DEFAULT_SIZE,
                 typeface=TYPEFACE_NORMAL, slide=SLIDE_RIGHT):
        """Input parameters:
        slide - determines kind of sliding animation.
        (Other parameters are the same as for TextLabel)."""
        super().__init__(scr, text, color, size, typeface)
        self.slide = slide
        self.set_origin((0, 0))

    def set_origin(self, origin_point):
        """Sets the screen point with initial position of the text label
        top-left corner.
        Input format: (int(x_left), int(y_top))."""
        self.origin_point = origin_point
        self.rect.topleft = self.origin_point

    def set_origin_center(self, origin_point):
        """Sets the screen point with initial position of the text label
        center.
        Input format: (int(x_center), int(y_center))"""
        self.origin_point = (int(origin_point[0] - self.rect.width/2),
                             int(origin_point[1] - self.rect.height/2))
        self.rect.topleft = self.origin_point

    def update(self):
        """Updates the position of the text label."""
        if self.slide == SLIDE_RIGHT:
            self.rect.x = int(self.origin_point[0] + self.progress)
        elif self.slide == SLIDE_LEFT:
            self.rect.x = int(self.origin_point[0] - self.progress)
        elif self.slide == SLIDE_TOP:
            self.rect.y = int(self.origin_point[1] - self.progress)
        elif self.slide == SLIDE_BOTTOM:
            self.rect.y = int(self.origin_point[1] + self.progress)

        super().update()
