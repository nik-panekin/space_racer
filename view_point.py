"""Module for working with absolute and screen systems of coordinates.
For this purpose ViewPoint class is presented. Also it serves
as a 'camera' for viewport.

Understanding systems of coordinates:

         y_absolute (+)
        ^
        |     (0, 0)
        |        +------------> x_screen (+)
        |        |            |
        |        |    view    |
        |        |    port    |
        |        |            |
        |        V------------+
        |         y_screen (+)
        |
--------+----------------------------------> x_absolute (+)
 (0, 0) |
        |
        |

Absolute coordinates are floats and are used for storing game objects
positions. Screen coordinates are integers and are used for drawing
game objects to the screen.
"""
import pygame

from map import GRID_SIZE

# Min. distance between view point and trace point to start moving view point
TRACE_OFFSET = 2 * GRID_SIZE

class ViewPoint():
    """Class which works as game 'camera' and provides methods for
    conversion between absolute and screen coordinates. It contains
    absolute coordinates for view point which can move with specified
    speed or follow another point."""
    def __init__(self, scr):
        """Input parameters: scr - Surface for drawing."""
        self.scr = scr
        self.reset()

    def reset(self):
        """Returns view point to the start position i.e. the center of
        the first map screen and resets all the parameters to its
        default values (zero speed, no trace point, no limits)."""
        scr_rect = self.scr.get_rect()
        self.half_width = scr_rect.width / 2
        self.half_height = scr_rect.height / 2
        self.x = 0
        self.y = scr_rect.centery
        self.trace_point = None
        self.speed = 0
        self.left_limit = None
        self.right_limit = None
        self.top_limit = None
        self.bottom_limit = None

    def set_limits(self, left=None, right=None, top=None, bottom=None):
        """Sets the limits which don't allow the view point to cross
        specified lines (if the view point is moving)."""
        self.left_limit = left
        self.right_limit = right
        self.top_limit = top
        self.bottom_limit = bottom

    def set_center(self, x, y):
        """Sets the absolute coordinates of the view point, which is
        actually the center of view port."""
        self.x = x
        self.y = y

    def set_trace_point(self, trace_point):
        """Sets the point to follow. Parameter trace_point contains
        tuple (x, y) of absolute coordinates."""
        self.trace_point = trace_point

    def set_speed(self, speed):
        """Sets the speed for view point vertical moving."""
        self.speed = speed

    def x_to_scr(self, x):
        """Converts absolute x-coordinate to screen x-coordiate."""
        return int(round(x - self.x + self.half_width))

    def scr_to_x(self, x):
        """Converts screen x-coordiate to absolute x-coordinate."""
        return float(x + self.x - self.half_width)

    def y_to_scr(self, y):
        """Converts absolute y-coordinate to screen y-coordiate."""
        return int(round(self.y - y + self.half_height))

    def scr_to_y(self, y):
        """Converts screen y-coordiate to absolute y-coordinate."""
        return float(self.y - y + self.half_height)

    def point_to_scr(self, x, y):
        """Input: absolute x and y coordiates.
        Output: tuple (x, y) of screen coordinates."""
        return (self.x_to_scr(x), self.y_to_scr(y))

    def scr_to_point(self, x, y):
        """Input: screen x and y coordiates.
        Output: tuple (x, y) of absolute coordinates."""
        return (self.scr_to_x(x), self.scr_to_y(y))

    def update(self):
        """Updates the position of the view point."""
        self.y += self.speed
        if self.trace_point:
            min_right = self.trace_point[0] - self.half_width + TRACE_OFFSET
            if self.x < min_right:
                self.x = min_right
            max_left = self.trace_point[0] + self.half_width - TRACE_OFFSET
            if self.x > max_left:
                self.x = max_left
            min_top = self.trace_point[1] - self.half_height + TRACE_OFFSET
            if self.y < min_top:
                self.y = min_top
            max_bottom = self.trace_point[1] + self.half_height - TRACE_OFFSET
            if self.y > max_bottom:
                self.y = max_bottom

        if self.left_limit:
            if self.x < self.left_limit:
                self.x = self.left_limit

        if self.right_limit:
            if self.x > self.right_limit:
                self.x = self.right_limit

        if self.top_limit:
            if self.y > self.top_limit:
                self.y = self.top_limit

        if self.bottom_limit:
            if self.y < self.bottom_limit:
                self.y = self.bottom_limit
