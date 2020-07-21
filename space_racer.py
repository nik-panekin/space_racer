"""Main program module. It pulls all other game modules together and
ensures running the game."""
import sys
from random import randint
from statistics import mean

import pygame
import pygame.mixer
from pygame.time import Clock

import sound_box
from view_point import ViewPoint
from track import Track
from game_level import GameLevel
from game_stats import GameStats
from game_stats import ASTEROID_HIT_PTS, LEVEL_COMPLETE_PTS, EXTRA_LIFE_PTS
from ship import Ship
from ship import STATUS_INACTIVE as SHIP_STATUS_INACTIVE
from ship import STATUS_NORMAL as SHIP_STATUS_NORMAL
from explosions import Explosions
from asteroids import Asteroids
from stars import Stars
from loading_screen import LoadingScreen
from title_screen import TitleScreen
from level_start_screen import LevelStartScreen
from level_complete_effect import LevelCompleteEffect
from game_over_effect import GameOverEffect
from pause_screen import PauseScreen
from ending_screen import EndingScreen

if '--fullscreen' in sys.argv:
    VID_MODE_FLAGS = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
else:
    VID_MODE_FLAGS = 0

SCREEN_SIZE = (1024, 768)
WINDOW_CAPTION = "SPACE RACER"
FRAMERATE = 60
SOUND_BUFFER = 512
MUSIC_FADEOUT = 2000

# Each of the following constants represents continuous game state
STATE_TITLE = 0
STATE_PAUSE = 1
STATE_LEVEL_STARTING = 2
STATE_LEVEL_PLAYING = 3
STATE_LEVEL_FINISHING = 4
STATE_GAME_OVER = 5
STATE_ENDING = 6

class SpaceRacer():
    """Represents the game itself"""
    def __init__(self):
        """Creates all game objects needed, loads resources, initializes
        pygame library and sound mixer, sets display mode, etc."""
        self.state = STATE_TITLE
        pygame.mixer.pre_init(buffer=SOUND_BUFFER)
        pygame.init()
        self.clock = Clock()
        self.scr = pygame.display.set_mode(SCREEN_SIZE, VID_MODE_FLAGS)
        pygame.display.set_caption(WINDOW_CAPTION)
        pygame.mouse.set_visible(False)
        LoadingScreen(self.scr).draw()
        sound_box.init()

        self.level = GameLevel()
        self.stats = GameStats(self.scr)
        self.view_pt = ViewPoint(self.scr)
        self.stars = Stars(self.scr, self.view_pt)
        self.track = Track(self.scr, self.view_pt)
        self.explosions = Explosions(self.scr, self.view_pt)
        self.ship = Ship(self.scr, self.view_pt, self.explosions)
        self.asteroids = Asteroids(self.scr, self.view_pt, self.explosions,
                                   self.track)
        self.title_screen = TitleScreen(self.scr, self.view_pt, self.stars)
        self.level_start_screen = LevelStartScreen(self.scr)
        self.level_complete_effect = LevelCompleteEffect(self.scr)
        self.game_over_effect = GameOverEffect(self.scr)
        self.pause_screen = PauseScreen(self.scr)
        self.ending_screen = EndingScreen(self.scr)

        self._init_title()

    def run(self):
        """The only public method just runs the game. It starts infinite
        loop where game objects are updated, drawn and interacts with
        each other. Also system events are processed."""
        while True:
            self.clock.tick(FRAMERATE)
            # print(f"FPS: {round(self.clock.get_fps(), 2)}")
            self._process_events()
            self._update_objects()
            self._interact_objects()
            self._draw_objects()

    def _init_title(self):
        self.state = STATE_TITLE
        self.stats.reset()
        self.level.restart()
        self.title_screen.restart()
        self.title_screen.play_music()

    def _init_level_starting(self):
        self.state = STATE_LEVEL_STARTING
        self.level_start_screen.set_level_number(self.level.get_level())
        self.level_start_screen.set_subtitle_text(self.level.get_description())
        self.level_start_screen.restart()

    def _init_level_playing(self):
        self.state = STATE_LEVEL_PLAYING
        self.level.play_music()
        self.view_pt.reset()
        self.stars.respawn()
        self.track.set_tile_map(self.level.get_map())

        top_limit = (self.track.get_track_height() -
                     self.scr.get_rect().height/2)
        bottom_limit = self.scr.get_rect().height/2
        self.view_pt.set_limits(top=top_limit, bottom=bottom_limit)

        self.explosions.items.empty()
        self.asteroids.set_spawn_density(self.level.get_asteroids_density())
        self.asteroids.respawn(self.level.get_asteroid_spawns())

        self.ship.set_speed(self.level.get_ship_speed())
        self.ship.set_acceleration(self.level.get_ship_acceleration())
        self.ship.restore((0, 0), reset_control=True)

    def _init_level_finishing(self):
        self.state = STATE_LEVEL_FINISHING
        self.stats.increase_score(LEVEL_COMPLETE_PTS)
        self.level_complete_effect.restart()
        self.ship.set_autopilot()
        pygame.mixer.music.fadeout(MUSIC_FADEOUT)

    def _init_game_over(self):
        self.state = STATE_GAME_OVER
        self.game_over_effect.restart()
        pygame.mixer.music.fadeout(MUSIC_FADEOUT)

    def _init_ending(self):
        self.state = STATE_ENDING
        self.ending_screen.set_score(self.stats.score)
        self.ending_screen.restart()
        self.ending_screen.play_music()

    def _init_pause(self):
        self.state = STATE_PAUSE
        self.pause_screen.refresh_background()
        pygame.mixer.music.pause()

    def _ship_control(self, key, control_status):
        """Returns True if the key was a ship direction control key."""
        key_processed = True

        if key == pygame.K_UP:
            self.ship.moving_up = control_status
        elif key == pygame.K_DOWN:
            self.ship.moving_down = control_status
        elif key == pygame.K_LEFT:
            self.ship.moving_left = control_status
        elif key == pygame.K_RIGHT:
            self.ship.moving_right = control_status
        elif key == pygame.K_SPACE:
            self.ship.shooting = control_status
        else:
            key_processed = False

        return key_processed

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if self.state == STATE_TITLE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.fadeout(MUSIC_FADEOUT)
                        self._init_level_starting()

            elif self.state == STATE_PAUSE:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_PAUSE):
                        self.state = STATE_LEVEL_PLAYING
                        pygame.mixer.music.unpause()
                    elif event.key == pygame.K_RETURN:
                        sys.exit()

            elif self.state == STATE_LEVEL_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_PAUSE):
                        self._init_pause()
                    else:
                        self._ship_control(event.key, control_status=True)
                elif event.type == pygame.KEYUP:
                    self._ship_control(event.key, control_status=False)

            if self.state == STATE_ENDING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        self._init_title()

    def _update_objects(self):
        if self.state == STATE_TITLE:
            self.title_screen.update()

        if self.state == STATE_LEVEL_STARTING:
            self.level_start_screen.update()

        if self.state in (STATE_LEVEL_PLAYING, STATE_LEVEL_FINISHING,
                          STATE_GAME_OVER):
            self.view_pt.update()
            self.stars.update()
            self.track.update()
            self.asteroids.update()
            self.ship.update()
            self.explosions.update()

        if self.state == STATE_LEVEL_FINISHING:
            self.level_complete_effect.update()

        if self.state == STATE_GAME_OVER:
            self.game_over_effect.update()

        if self.state == STATE_ENDING:
            self.ending_screen.update()

    def _crossed_finish_line(self):
        finish_line_y = (self.track.get_track_height() -
                         self.scr.get_rect().height/2)
        return self.ship.y > finish_line_y

    def _interact_objects(self):
        if self.state == STATE_LEVEL_STARTING:
            if self.level_start_screen.finished():
                self._init_level_playing()

        elif self.state == STATE_LEVEL_PLAYING:
            if self.stats.game_over():
                self._init_game_over()
            elif self._crossed_finish_line():
                self._init_level_finishing()
            elif self.ship.status == SHIP_STATUS_NORMAL:
                self._check_collisions()
            elif self.ship.status == SHIP_STATUS_INACTIVE:
                self._ship_restore()

        elif self.state == STATE_LEVEL_FINISHING:
            if self.level_complete_effect.finished():
                if self.level.last_level():
                    self._init_ending()
                else:
                    self.level.next_level()
                    self._init_level_starting()

        elif self.state == STATE_GAME_OVER:
            if self.game_over_effect.finished():
                self._init_title()

    def _draw_objects(self):
        if self.state == STATE_TITLE:
            self.title_screen.draw()

        if self.state == STATE_PAUSE:
            self.pause_screen.draw()

        if self.state == STATE_LEVEL_STARTING:
            self.level_start_screen.draw()

        if self.state in (STATE_LEVEL_PLAYING, STATE_LEVEL_FINISHING,
                          STATE_GAME_OVER):

            self.scr.blit(self.level.get_background(), (0, 0))
            self.stars.draw()
            self.track.draw()
            self.asteroids.draw()
            self.ship.draw()
            self.explosions.draw()
            self.stats.draw()

        if self.state == STATE_LEVEL_FINISHING:
            self.level_complete_effect.draw()

        if self.state == STATE_GAME_OVER:
            self.game_over_effect.draw()

        if self.state == STATE_ENDING:
            self.ending_screen.draw()

        pygame.display.flip()

    def _ship_explode(self, collide_point=None):
        """collide_point is a tuple of absolute coordinates: (x, y)"""
        self.stats.lost_life()
        self.ship.explode(collide_point)

    def _ship_restore(self):
        restore_x, restore_y = self.ship.get_center()
        borders = self.track.get_track_borders(restore_y)
        if borders:
            restore_x = mean(borders)
        if self.ship.restore((restore_x, restore_y)):
            self.asteroids.explode_nearest(self.ship.get_center())

    def _check_ship_penalty(self):
        borders = self.track.get_track_borders(self.ship.get_center()[1])
        if borders:
            left = self.ship.x
            right = left + self.ship.rect.width
            if right < borders[0] or left > borders[1]:
                self._ship_explode()
                return True
        return False

    def _check_collisions(self):
        collide_point = self.track.collidemask(self.ship.mask, self.ship.rect)
        if collide_point:
            self._ship_explode(collide_point)
            return True

        collide_point = self.asteroids.collidemask(self.ship.mask,
                                                   self.ship.rect,
                                                   explode=True)
        if collide_point:
            self._ship_explode(collide_point)
            return True

        if self.ship.laser.shooting():
            if self.asteroids.collidemask(self.ship.laser.mask,
                                          self.ship.laser.rect, explode=True):
                self.stats.increase_score(ASTEROID_HIT_PTS)

        return self._check_ship_penalty()


if __name__ == '__main__':
    SpaceRacer().run()
