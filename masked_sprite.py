"""Module which provides animations with bitmasks."""
import pygame

from animated_sprite import AnimatedSprite

class MaskedSprite(AnimatedSprite):
    """The class extends functionality of the AnimatedSprite base class
    by introducing means for working with bitmasks (pygame.mask.Mask).
    They are used for checking collisions."""
    def __init__(self, image, masks, scr, view_point, cols=1, rows=1,
                 reverse=False):
        """Input parameters:
        masks - list of bitmasks (pygame.mask.Mask) for each frame of
        the animation.
        (Other parameters are the same as for AnimatedSprite)."""
        super().__init__(image, scr, view_point, cols, rows, reverse)
        self.masks = masks

    def get_mask(self):
        """Returns bitmask corresponding to the current frame."""
        return self.masks[self.frame]

    def collidemask(self, mask, rect):
        """Checks a collision between given mask (pygame.mask.Mask)
        positioned with rect (pygame.Rect) in screen coordinates and
        the mask corresponding current frame of the animation.
        Returns point of collision in absolute coordinates
        if collision occurred and None otherwise."""
        if self.rect.colliderect(rect):
            offset = (rect.x - self.rect.x, rect.y - self.rect.y)
            point = self.get_mask().overlap(mask, offset)
            if point:
                return self.view_pt.scr_to_point(point[0] + self.rect.x,
                                                 point[1] + self.rect.y)

        return None
