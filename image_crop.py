"""Crops the image: removes transparent area near the edges."""
import pygame

def image_crop(image):
    """Input: pygame.Surface.
    Returns a dict in format:
    {
    'image': pygame.Surface for image have been cropped,
    'offset_x': left coordinate of source image cropping rect,
    'offset_y': top coordinate of source image cropping rect
    }
    """
    rect = image.get_rect()
    image.lock()

    # Scanning for left edge
    x_left = rect.width - 1
    x = 0
    while x < rect.width - 1:
        for y in range(0, rect.height):
            if image.get_at((x, y)).a > 0:
                x_left = x
                x = rect.width # For breaking outer loop
                break
        x += 1

    # Scanning for right edge
    x_right = 0
    x = rect.width - 1
    while x > 0:
        for y in range(0, rect.height):
            if image.get_at((x, y)).a > 0:
                x_right = x
                x = 0 # For breaking outer loop
                break
        x -= 1

    # Scanning for top edge
    y_top = rect.height - 1
    y = 0
    while y < rect.height - 1:
        for x in range(0, rect.width):
            if image.get_at((x, y)).a > 0:
                y_top = y
                y = rect.height # For breaking outer loop
                break
        y += 1

    # Scanning for bottom edge
    y_bottom = 0
    y = rect.height - 1
    while y > 0:
        for x in range(0, rect.width):
            if image.get_at((x, y)).a > 0:
                y_bottom = y
                y = 0 # For breaking outer loop
                break
        y -= 1

    image.unlock()

    width = x_right - x_left + 1
    height = y_bottom - y_top + 1

    out_image = pygame.Surface((width, height), pygame.SRCALPHA, image)
    out_image.fill((0, 0, 0, 0))
    out_image.blit(image, (0, 0), pygame.Rect(x_left, y_top, width, height))

    return {'image': out_image, 'offset_x': x_left, 'offset_y': y_top}
