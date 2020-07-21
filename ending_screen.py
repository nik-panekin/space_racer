"""Module for showing ending screen and playing ending music."""
import pygame
import pygame.mixer

from fading_label import FadingLabel
from blinking_label import BlinkingLabel

MUSIC_FILENAME = 'ending.ogg'
BACKGROUND_FILENAME = 'bg_07.png'
FONT_SIZE_DEFAULT = 32
FONT_SIZE_START = 24
SCORE_TEXT = 'YOUR FINAL SCORE: '
START_TEXT = 'PRESS ESC FOR QUIT THE GAME OR RETURN FOR START AGAIN!'
DEFAULT_COLOR = (255, 255, 255)
SCORE_COLOR = (109, 207, 246)
START_COLOR_PRIMARY = (109, 207, 246)
START_COLOR_SECONDARY = (0, 0, 0)

ENDING_TEXT = (
    'CONGRATULATIONS!',
    'YOU BEAT THE GAME AND SAVED THE WORLD!',
    'SORRY FOR NO COOL CUTSCENE AS A REWARD.',
    'WE ARE OUT OF BUDGET...',
    'ANYWAY THANK YOU FOR PLAYING!',
    )

class EndingScreen():
    def __init__(self, scr, score=0):
        """Input parameters:
        scr - Surface for drawing;
        score - player's final score."""
        self.scr = scr
        self.background = pygame.image.load(
            f"img/bg/{BACKGROUND_FILENAME}").convert()
        scr_rect = self.scr.get_rect()

        self.labels = []
        for i in range(0, len(ENDING_TEXT)):
            label = FadingLabel(
                scr=self.scr,
                text=ENDING_TEXT[i],
                color=DEFAULT_COLOR,
                size=FONT_SIZE_DEFAULT)
            label.rect.midtop = (
                scr_rect.centerx,
                scr_rect.top + FONT_SIZE_DEFAULT * (i * 2 + 2))
            label.set_repeat(False)
            self.labels.append(label)

        self.score_label = FadingLabel(
            scr=self.scr,
            text=self._get_score_text(score),
            color=SCORE_COLOR,
            size=FONT_SIZE_DEFAULT)
        self.score_label.rect.midtop = (
            scr_rect.centerx,
            scr_rect.top + FONT_SIZE_DEFAULT * (len(ENDING_TEXT) * 2 + 4))
        self.score_label.set_repeat(False)
        self.labels.append(self.score_label)

        self.start_fading_label = FadingLabel(
            scr=self.scr,
            text=START_TEXT,
            color=START_COLOR_PRIMARY,
            size=FONT_SIZE_START)
        self.start_fading_label.rect.midbottom = (
            scr_rect.centerx,
            scr_rect.bottom - FONT_SIZE_START * 2)
        self.start_fading_label.set_repeat(False)
        self.labels.append(self.start_fading_label)

        self.start_blinking_label = BlinkingLabel(
            scr=self.scr,
            text=START_TEXT,
            color=START_COLOR_PRIMARY,
            second_color=START_COLOR_SECONDARY,
            size=FONT_SIZE_START)
        self.start_blinking_label.rect.midbottom = (
            self.start_fading_label.rect.midbottom)
        self.labels.append(self.start_blinking_label)

    def _get_score_text(self, score):
        return "{}{:,}".format(SCORE_TEXT, score)

    def set_score(self, score):
        """Sets new value for player's final score."""
        scr_rect = self.scr.get_rect()
        self.score_label.set_text(self._get_score_text(score))
        self.score_label.rect.midtop = (
            scr_rect.centerx,
            scr_rect.top + FONT_SIZE_DEFAULT * (len(ENDING_TEXT) * 2 + 4))

    def restart(self):
        """Prepares all animation effects for playing again."""
        for label in self.labels:
            label.restart()

    def _get_active_labels(self):
        labels = []

        for label in self.labels:
            if label.finished:
                if label != self.start_fading_label:
                    labels.append(label)
            else:
                labels.append(label)
                break

        return labels

    def update(self):
        """Updates screen positions for text labels."""
        for label in self._get_active_labels():
            label.update()

    def draw(self):
        """Renders background image and text labels to the
        specified surface."""
        self.scr.blit(self.background, (0, 0))
        for label in self._get_active_labels():
            label.draw()

    def play_music(self):
        """Starts playing music for ending screen."""
        pygame.mixer.music.load(f"mus/{MUSIC_FILENAME}")
        pygame.mixer.music.play(loops=-1)
