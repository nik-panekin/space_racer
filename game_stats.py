"""Module for storing and rendering game statistics."""
import sys

import pygame

from sound_box import get_sound_box
from text_label import TextLabel

if '--easymode' in sys.argv:
    STARTING_LIVES = 30
else:
    STARTING_LIVES = 3

ASTEROID_HIT_PTS = 100
LEVEL_COMPLETE_PTS = 2000
EXTRA_LIFE_PTS = 10000
TEXT_OFFSET = 16

class GameStats():
    """The class encapsulates general game parameters: player's score
    and ships left. Also it renders them on the screen."""
    def __init__(self, scr):
        """Input parameters:
        scr - Surface for drawing."""
        self.scr = scr
        self.score = 0
        self.lives = STARTING_LIVES
        self.score_label = TextLabel(self.scr, self._get_score_text())
        self.lives_label = TextLabel(self.scr, self._get_lives_text())
        self._update_labels_pos()

    def _get_score_text(self):
        return "Score: {:,}".format(self.score)

    def _get_lives_text(self):
        return f"Lives: {self.lives}"

    def reset(self):
        """Sets score to zero and resets lives counter."""
        self.score = 0
        self.lives = STARTING_LIVES
        self._update()

    def _update_labels_pos(self):
        self.score_label.rect.top = self.scr.get_rect().top + TEXT_OFFSET
        self.score_label.rect.right = self.scr.get_rect().right - TEXT_OFFSET

        self.lives_label.rect.top = self.scr.get_rect().top + TEXT_OFFSET
        self.lives_label.rect.left = self.scr.get_rect().left + TEXT_OFFSET

    def _update(self):
        """No need to call manually."""
        self.score_label.set_text(self._get_score_text())
        self.lives_label.set_text(self._get_lives_text())
        self._update_labels_pos()

    def draw(self):
        """Draws game statistics on the screen."""
        self.score_label.draw()
        self.lives_label.draw()

    def increase_score(self, increment):
        """Increase score by increment parameter. Increment lives
        counter if the player has earned extra life."""
        new_score = self.score + increment
        if (self.score // EXTRA_LIFE_PTS) != (new_score // EXTRA_LIFE_PTS):
            get_sound_box().play_extra_life()
            self.lives += 1
        self.score = new_score
        self._update()

    def lost_life(self):
        """Decrease lives counter by one."""
        if (self.lives > 0):
            self.lives -= 1
        self._update()

    def game_over(self):
        """Returns True if lives counter is positive
        and False otherwise."""
        return self.lives <= 0
