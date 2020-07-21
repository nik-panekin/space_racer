"""Module for showing level title screen before game level starts."""
import pygame

from fading_label import FadingLabel, STYLE_EXPOSE, STYLE_FADE

TITLE_TEXT = 'LEVEL '
SCREEN_COLOR = (8, 0, 51)
FONT_SIZE_TITLE = 48
FONT_SIZE_SUBTITLE = 32
COLOR_TITLE = (255, 255, 255)
COLOR_SUBTITLE = (109, 207, 246)
# Delay in frames between vanishing all the text labels and
# proceeding to next game screen
MAX_DELAY = 60

class LevelStartScreen():
    def __init__(self, scr, level_number=0, subtitle_text=''):
        """Input parameters:
        scr - Surface for drawing;
        level_number - number of the level to be playing;
        subtitle_text - text for game level description."""
        self.scr = scr
        self.timer = 0

        self.title_label = FadingLabel(
            scr=self.scr,
            text=self._get_title_text(level_number),
            color=COLOR_TITLE,
            size=FONT_SIZE_TITLE,
            style=STYLE_EXPOSE)
        self.title_label.set_repeat(False)

        self.subtitle_label = FadingLabel(
            scr=self.scr,
            text=subtitle_text,
            color=COLOR_SUBTITLE,
            size=FONT_SIZE_SUBTITLE,
            style=STYLE_EXPOSE)
        self.subtitle_label.set_repeat(False)

        self.title_fading_label = FadingLabel(
            scr=self.scr,
            text=self._get_title_text(level_number),
            color=COLOR_TITLE,
            size=FONT_SIZE_TITLE,
            style=STYLE_FADE)
        self.title_fading_label.set_repeat(False)

        self.subtitle_fading_label = FadingLabel(
            scr=self.scr,
            text=subtitle_text,
            color=COLOR_SUBTITLE,
            size=FONT_SIZE_SUBTITLE,
            style=STYLE_FADE)
        self.subtitle_fading_label.set_repeat(False)

        self._update_labels_pos()

    def _get_title_text(self, level_number):
        return f"{TITLE_TEXT}{level_number}"

    def _update_labels_pos(self):
        scr_rect = self.scr.get_rect()
        self.title_label.rect.center = (
            scr_rect.centerx,
            scr_rect.centery - FONT_SIZE_TITLE // 2)
        self.subtitle_label.rect.center = (
            scr_rect.centerx,
            scr_rect.centery + FONT_SIZE_TITLE // 2)
        self.title_fading_label.rect.center = self.title_label.rect.center
        self.subtitle_fading_label.rect.center = (
            self.subtitle_label.rect.center)

    def set_level_number(self, level_number):
        """Sets new value for level number to be shown in title."""
        self.title_label.set_text(self._get_title_text(level_number))
        self.title_fading_label.set_text(self._get_title_text(level_number))
        self._update_labels_pos()

    def set_subtitle_text(self, subtitle_text):
        """Sets new value for subtitle text (game level description)."""
        self.subtitle_label.set_text(subtitle_text)
        self.subtitle_fading_label.set_text(subtitle_text)
        self._update_labels_pos()

    def finished(self):
        """Returns True if the screen is considered as 'fully shown'
        and False otherwise."""
        return self.timer >= MAX_DELAY

    def restart(self):
        """Prepares all animation effects for playing again."""
        self.timer = 0
        self.title_label.restart()
        self.subtitle_label.restart()
        self.title_fading_label.restart()
        self.subtitle_fading_label.restart()

    def _get_active_labels(self):
        labels = []

        if self.title_label.finished:
            if self.subtitle_label.finished:
                if self.title_fading_label.finished:
                    labels.append(self.subtitle_fading_label)
                else:
                    labels.append(self.title_fading_label)
                    labels.append(self.subtitle_label)
            else:
                labels.append(self.title_label)
                labels.append(self.subtitle_label)
        else:
            labels.append(self.title_label)

        return labels

    def update(self):
        """Updates screen positions for text labels and inner timer."""
        for label in self._get_active_labels():
            label.update()

        if self.subtitle_fading_label.finished:
            if self.timer < MAX_DELAY:
                self.timer += 1
            else:
                self.timer = MAX_DELAY

    def draw(self):
        """Fills the specified surface with solid color and renders
        all the text labels."""
        self.scr.fill(SCREEN_COLOR)
        for label in self._get_active_labels():
            label.draw()
