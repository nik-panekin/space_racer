"""Module for rendering static single-line on-screen text."""
import pygame
import pygame.font

FONT_FILENAMES = ('Suggested.ttf', 'Suggested3D.ttf')
# Typefaces are actually indexes for FONT_FILENAMES list
TYPEFACE_NORMAL = 0
TYPEFACE_3D = 1
DEFAULT_COLOR = (255, 255, 255)
DEFAULT_SIZE = 24

class TextLabel():
    """Stores text attributes (such as text itself, color, size,
    typeface) and renders the text to specified position.
    Note: self.rect attribute contains size and position of the label.
    You may change position of the rect, but not the size: it may break
    proper class operation."""
    def __init__(self, scr, text='', color=DEFAULT_COLOR, size=DEFAULT_SIZE,
                 typeface=TYPEFACE_NORMAL):
        """Input parameters:
        scr - pygame.Surface for drawing;
        text - text of the label itself;
        color - color of the font (list or tuple [r, g, b]);
        size - size of the font;
        typeface - index of the font typeface."""
        self.scr = scr
        self.text = text
        self.color = list(color)
        self.size = size
        filename = FONT_FILENAMES[typeface]
        self.font = pygame.font.Font(f'fnt/{filename}', self.size)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self._render()

    def _render(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect.width, self.rect.height = self.image.get_size()

    def draw(self):
        """Renders the label to the surface."""
        self.scr.blit(self.image, self.rect)

    def set_text(self, text):
        """Sets new text of the label."""
        if self.text != text:
            self.text = text
            self._render()
        else:
            self.text = text

    def set_color(self, color):
        """Sets new color of the label (list or tuple [r, g, b])."""
        if self.color != list(color):
            self.color = list(color)
            self._render()
        else:
            self.color = list(color)

    def set_size(self, size):
        """Sets new size of the label font."""
        if self.size != size:
            self.size = size
            self._render()
        else:
            self.size = size
