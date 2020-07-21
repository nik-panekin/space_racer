"""Module introduces FadingLabel class which can render fading or
exposing on-screen text."""
import pygame

from text_label import DEFAULT_COLOR, DEFAULT_SIZE, TYPEFACE_NORMAL
from animated_label import AnimatedLabel

# Slowly changes transparency from fully transparent to fully opaque
STYLE_EXPOSE = 0
# Slowly changes transparency from fully opaque to fully transparent
STYLE_FADE = 1
# At first changes transparency like STYLE_EXPOSE and then - like STYLE_FADE
STYLE_BLINK = 2

# This constant is used for switching rendering methods. When alpha value
# reaches its maximum, then the font must be rendered as fully opaque.
MAX_ALPHA = 255
COLORKEY = (0, 0, 0)

class FadingLabel(AnimatedLabel):
    """This type of label implements fading and exposing animation
    effects. The text slowly changes its transparency accordingly
    the specified style.
    Note: don't use pure black color for the text because it is reserved
    for transparency."""
    def __init__(self, scr, text='', color=DEFAULT_COLOR, size=DEFAULT_SIZE,
                 typeface=TYPEFACE_NORMAL, style=STYLE_EXPOSE):
        """Input parameters:
        style - determines behavior of the label (see constants).
        (Other parameters are the same as for TextLabel)."""
        self.style = style
        if self.style == STYLE_FADE:
            self.alpha = MAX_ALPHA
        else:
            self.alpha = 0
        super().__init__(scr, text, color, size, typeface)

    def update(self):
        """Updates the transparency of the text label."""
        if not self.finished:
            if self.style == STYLE_BLINK:
                # fraction may vary like this: [0..1..0]
                fraction = 1 - 2*abs(self.progress/self.max_progress - 0.5)
            elif self.style == STYLE_EXPOSE:
                # or like this: [0..1]
                fraction = self.progress/self.max_progress
            elif self.style == STYLE_FADE:
                # or like this: [1..0]
                fraction = 1 - self.progress/self.max_progress

            self.alpha = int(round(fraction * MAX_ALPHA))
            self._render()

        super().update()

    def _render(self):
        if self.alpha == MAX_ALPHA:
            super()._render()
        else:
            self.image = self.font.render(self.text, True,
                                          self.color, COLORKEY)
            self.image.set_colorkey(COLORKEY)
            self.image.set_alpha(self.alpha)
            self.rect.width, self.rect.height = self.image.get_size()
