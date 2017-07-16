#!/usr/bin/env python
# -*- coding: utf-8 -*-
# slacker-game - A clone of the arcade game Stacker
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2007 Clint Herron
# Copyright (C) 2017 Nguyễn Gia Phong

from math import cos, pi
from random import randrange

import pygame
from pkg_resources import resource_filename

TANGO = {'Butter': ((252, 233, 79), (237, 212, 0), (196, 160, 0)),
         'Orange': ((252, 175, 62), (245, 121, 0), (206, 92, 0)),
         'Chocolate': ((233, 185, 110), (193, 125, 17), (143, 89, 2)),
         'Chameleon': ((138, 226, 52), (115, 210, 22), (78, 154, 6)),
         'Sky Blue': ((114, 159, 207), (52, 101, 164), (32, 74, 135)),
         'Plum': ((173, 127, 168), (117, 80, 123), (92, 53, 102)),
         'Scarlet Red': ((239, 41, 41), (204, 0, 0), (164, 0, 0)),
         'Aluminium': ((238, 238, 236), (211, 215, 207), (186, 189, 182),
                       (136, 138, 133), (85, 87, 83), (46, 52, 54))}


def data(resource):
    """Return a true filesystem path for specified resource."""
    return resource_filename('slacker_game', resource)


class SlackerTile:
    """SlackerTile(x, y) -> SlackerTile

    Slacker object for storing tiles.
    """
    SIZE = 40
    BG = TANGO['Aluminium'][5]
    MAJOR = 5

    def __init__(self, screen, x, y, state=1, missed_time=None):
        self.screen, self.x, self.y = screen, x, y
        if state == Slacker.LOSE:
            self.dim = 1
        elif missed_time is None:
            self.dim = 0
        else:
            self.dim = 2
        self.missed_time = missed_time
        self.wiggle = state in (Slacker.INTRO, Slacker.WIN)

    def get_xoffset(self, maxoffset, duration=820):
        """Return the offset on x-axis to make the tile complete an cycle of
        wiggling oscillation in given duration (in milliseconds).
        """
        if self.wiggle:
            return maxoffset * cos((pygame.time.get_ticks()/float(duration)
                                   + self.y/float(Slacker.BOARD_HEIGHT)) * pi)
        return 0

    def get_yoffset(self):
        """Return the offset on y-axis when the tile is falling."""
        if self.missed_time is None:
            return 0
        return (pygame.time.get_ticks() - self.missed_time)**2 / 25000.0

    def isfallen(self):
        """Return if the tile has fallen off the screen."""
        return self.y + self.get_yoffset() > Slacker.BOARD_HEIGHT

    def draw(self, max_x_offset=2):
        """Draw the tile."""
        color = (Slacker.COLOR_MAJOR if self.y < self.MAJOR else Slacker.COLOR_MINOR)[self.dim]
        rect = pygame.Rect((self.x+self.get_xoffset(max_x_offset)) * self.SIZE,
                           (self.y+self.get_yoffset()) * self.SIZE,
                           self.SIZE, self.SIZE)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.BG, rect, self.SIZE / 11)


class Slacker:
    """This class provides functions to run the game Slacker, a clone of
    the popular arcade game Stacker.
    """
    BOARD_SIZE = BOARD_WIDTH, BOARD_HEIGHT = 7, 15
    SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 280, 600
    TILE_SIZE = 40

    COLOR_MAJOR = TANGO['Scarlet Red']
    COLOR_MINOR = TANGO['Sky Blue']
    BG_COLOR = TANGO['Aluminium'][5]
    ICON = pygame.image.load(data('icon.png'))

    MAX_WIDTH = (1,)*7 + (2,)*5 + (3,)*3
    COLOR_CHANGE_Y = 5  # blocks below which are displayed in the alternate color
    WIN_LEVEL = 15
    WIN_SPEED = 100
    INTRO, PLAYING, LOSE, WIN = range(4)

    def __init__(self, restart=False):
        pygame.init()
        pygame.display.set_icon(self.ICON)
        pygame.display.set_caption('Slacker')
        self.board = [[False] * self.BOARD_WIDTH for _ in range(self.BOARD_HEIGHT)]
        self.game_state = self.PLAYING if restart else self.INTRO
        self.falling_tiles = []
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.speed = 84 + randrange(5)
        self.speed_ratio = 1.0
        self.width = self.MAX_WIDTH[-1]
        self.y = self.BOARD_HEIGHT - 1

    def draw_text(self, string, height):
        """Width-fit the string in the screen on the given height."""
        font = pygame.font.Font(
            data('VT323-Regular.ttf'),
            int(self.SCREEN_WIDTH * 2.5 / (len(string) + 1)))
        text = font.render(string, False, self.COLOR_MINOR[0])
        self.screen.blit(text, ((self.SCREEN_WIDTH - text.get_width()) // 2,
                                int(self.SCREEN_HEIGHT * height)))

    def intro(self):
        """Draw the intro screen."""
        for i in [(2, 2), (3, 2), (4, 2), (1.5, 3), (4.5, 3),
                  (1.5, 4), (2, 5), (3, 5), (4, 5), (4.5, 6),
                  (1.5, 7), (4.5, 7), (2, 8), (3, 8), (4, 8)]:
            SlackerTile(self.screen, *i, state=self.INTRO).draw(1.5)
        if pygame.time.get_ticks() // 820 % 2:
            self.draw_text('Press Spacebar', 0.75)

    def draw_board(self):
        """Draw the board and the tiles inside."""
        for y, row in enumerate(self.board):
            for x, block in enumerate(row):
                if block:
                    SlackerTile(self.screen, x, y, state=self.game_state).draw()

        # Draw the falling tiles
        for ft in self.falling_tiles:
            if ft.isfallen():
                self.falling_tiles.remove(ft)
            else:
                ft.draw()

    def update_screen(self):
        """Draw the whole screen and everything inside."""
        self.screen.fill(self.BG_COLOR)
        if self.game_state == self.INTRO:
            self.intro()
        elif self.game_state in (self.PLAYING, self.LOSE, self.WIN):
            self.draw_board()
        pygame.display.flip()

    def update_movement(self):
        """Update the direction the blocks are moving in."""
        speed = self.speed * self.speed_ratio
        positions = self.BOARD_WIDTH + self.width - 2
        p = int(round(pygame.time.get_ticks() / speed)) % (positions * 2)
        self.x = (-p % positions if p > positions else p) - self.width + 1
        self.board[self.y] = [0 <= x - self.x < self.width
                              for x in range(self.BOARD_WIDTH)]

    def key_hit(self):
        """Process the current position of the blocks relatively to the
        ones underneath when user hit the switch, then decide if the
        user will win, lose or go to the next level of the tower.
        """
        if self.y < self.BOARD_HEIGHT - 1:
            for x in range(max(0, self.x),
                           min(self.x + self.width, self.BOARD_WIDTH)):
                # If there isn't any block underneath
                if not self.board[self.y + 1][x]:
                    # Get rid of the block not standing on solid ground
                    self.board[self.y][x] = False
                    # Then, add that falling block to falling_tiles
                    self.falling_tiles.append(SlackerTile(
                        self.screen, x, self.y, missed_time=pygame.time.get_ticks()))
        self.width = sum(self.board[self.y])
        if not self.width:
            self.game_state = self.LOSE
        elif not self.y:
            self.game_state = self.WIN
        else:
            self.y -= 1
            self.width = min(self.width, self.MAX_WIDTH[self.y])
            self.speed = 42 + self.y*3 + randrange(5)

    def main_loop(self, loop=True):
        """The main loop."""
        while loop:
            if self.game_state == self.INTRO:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_state = self.PLAYING
                        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                            loop = False

            elif self.game_state == self.PLAYING:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.key_hit()
                        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                            self.__init__()
                        # Yes, this is a cheat.
                        elif event.key == pygame.K_0 and self.width < self.BOARD_WIDTH:
                            self.width += 1
                        elif event.key in range(pygame.K_1, pygame.K_9 + 1):
                            self.speed_ratio = (pygame.K_9 - event.key + 1) / 5.0
                self.update_movement()

            elif self.game_state in (self.LOSE, self.WIN):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    elif event.type == pygame.KEYDOWN:
                        self.__init__(restart=True)
            self.update_screen()


def main():
    pygame.init()
    slacker = Slacker()
    slacker.main_loop()
    pygame.display.quit()


if __name__ == '__main__':
    main()
