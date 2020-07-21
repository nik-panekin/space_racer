"""Module introduces BlinkingLabel class which can render blinking
on-screen text."""
import pygame

from text_label import DEFAULT_COLOR, DEFAULT_SIZE, TYPEFACE_NORMAL
from animated_label import AnimatedLabel

class BlinkingLabel(AnimatedLabel):
    """This type of label implements blinking animation effect. The text
    slowly changes its color - one time or in the loop."""
    def __init__(self, scr, text='', color=DEFAULT_COLOR, size=DEFAULT_SIZE,
                 typeface=TYPEFACE_NORMAL, second_color=DEFAULT_COLOR):
        """Input parameters:
        color, second_color - colors of the text for performing blinking
        effect (list or tuple [r, g, b]).
        The scheme of color changing for one period of animation:

        color  ========>  second_color  ========> color
          |--------------------+--------------------|
          0             max_progress/2        max_progress

        (Other parameters are the same as for TextLabel)."""
        super().__init__(scr, text, color, size, typeface)
        self.first_color = tuple(self.color)
        self.second_color = second_color

    def update(self):
        """Updates the color of the text label."""
        if not self.finished:
            # fraction vary like this [0..1..0] during one period of animation
            fraction = 1 - 2*abs(self.progress/self.max_progress - 0.5)
            for i in range(0, len(self.color)):
                self.color[i] = int(self.first_color[i] + (self.second_color[i]
                                    - self.first_color[i]) * fraction)
            self._render()

        super().update()
