"""Module for drawing animations."""
import pygame
from pygame.sprite import Sprite

from view_point import ViewPoint

class AnimatedSprite(Sprite):
    """Encapsulates an image with animation frames and provides methods
    for drawing appropriate frame accordingly animation progression.
    The image must be a grid of rectangular frames arranged in rows and
    columns."""
    def __init__(self, image, scr, view_point, cols=1, rows=1, reverse=False):
        """Input parameters:
        image - previously created image with animation frames;
        scr - Surface for drawing;
        view_point - ViewPoint class instance;
        cols - number of columns in animation image;
        rows - number of rows in animation image;
        reverse - if True, the animation will play in reverse order."""
        super().__init__()
        self.scr = scr
        self.view_pt = view_point
        self.image = image
        self.cols = cols
        self.rows = rows
        self.reverse = reverse
        if self.reverse:
            self.frame = self.get_max_frame()
        else:
            self.frame = 0
        self.frame_fraction = 0
        self.speed = 1.0
        self.repeat = True
        self.stopped = False
        self.x = 0
        self.y = 0
        self.rect = pygame.Rect(0, 0,
                                self.image.get_rect().width // self.cols,
                                self.image.get_rect().height // self.rows)
        self._update_rect()

    def set_speed(self, speed):
        """Sets the speed of animation.
        It may vary from 0 (stopped) to 1 (full speed)."""
        self.speed = speed

    def set_center(self, center_x, center_y):
        """Sets the absolute center coordinates of the animation."""
        self.x = center_x - (self.rect.width / 2)
        self.y = center_y + (self.rect.height / 2)
        self._update_rect()

    def get_center(self):
        """Returns point (x, y) with absolute center coordinates
        of the animation."""
        return (self.x + self.rect.width / 2, self.y - self.rect.height / 2)

    def _update_rect(self):
        self.rect.x = self.view_pt.x_to_scr(self.x)
        self.rect.y = self.view_pt.y_to_scr(self.y)

    def _get_frame_rect(self, frame=None):
        """Returns inner rect that represents single frame of animation
        (if no frame number passed then current frame is assumed)"""
        if frame == None:
            frame = self.frame

        rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
        rect.x = (frame % self.cols) * self.rect.width
        rect.y = (frame // self.cols) * self.rect.height
        return rect

    def get_max_frame(self):
        """Returns last animation frame number."""
        return self.cols*self.rows - 1

    def next_frame(self):
        """Proceeds to the next animation frame (if animation is still
        playing)."""
        if not self.stopped:
            self.frame_fraction += self.speed
            if self.frame_fraction >= 1:
                self.frame_fraction = 0

                if self.reverse:
                    self.frame -= 1
                else:
                    self.frame += 1

                if self.frame > self.get_max_frame():
                    if self.repeat:
                        self.frame = 0
                    else:
                        self.frame = self.get_max_frame()
                        self.stopped = True

                if self.frame < 0:
                    if self.repeat:
                        self.frame = self.get_max_frame()
                    else:
                        self.frame = 0
                        self.stopped = True

    def update(self):
        """Updates animation frame screen coordinates."""
        self._update_rect()

    def draw(self):
        """Draws animation frame. Don't proceeds to the next frame."""
        self.scr.blit(self.image, self.rect, self._get_frame_rect())

    def play(self):
        """Resumes animation playing after it was stopped or finished."""
        if self.stopped:
            self.stopped = False
            self.frame_fraction = 0
            if self.frame == 0 and self.reverse:
                self.frame = self.get_max_frame()

            if self.frame == self.get_max_frame() and not self.reverse:
                self.frame = 0

    def stop(self):
        """Stops animation playing. Actually works as pause."""
        self.stopped = True
