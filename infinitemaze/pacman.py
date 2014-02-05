#-*- coding:utf-8 -*-

"""
This file is part of infinite-maze-of-pacman.

infinite-maze-of-pacman is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

infinite-maze-of-pacman is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with infinite-maze-of-pacman.  If not, see
<http://www.gnu.org/licenses/>.
"""

import os
import pygame
from infinitemaze.creature import Creature
try:
	import android
	import android.mixer as mixer
except:
	android = None
	import pygame.mixer as mixer

class Pacman(Creature):

	"""The Pacman creature."""

	def __init__(self, game):

		"""
		Constructor.

		game	--	The Game object.
		"""

		super(Pacman, self).__init__(game, pos=(game.maze.width()/2, \
			game.maze.height()/2))
		self.maze.setPacman(self)
		self.score = 0
		self.goalDir = u'stop'
		self.hit1 = mixer.Sound(os.path.join(os.path.dirname(__file__),
			u'sounds', u'hit1.ogg'))
		self.hit10 = mixer.Sound(os.path.join(os.path.dirname(__file__),
			u'sounds', u'hit10.ogg'))
		self.hit10.set_volume(.15)
		self.hit50 = mixer.Sound(os.path.join(os.path.dirname(__file__),
			u'sounds', u'hit50.ogg'))
		self.hit50.set_volume(.25)

	def getScore(self):

		"""
		Returns:
		The score.
		"""

		return self.score

	def loadSprites(self):

		"""Loads the sprites."""

		self.sprites = [
			self.sprite(u'pacman-mouth-open.png'),
			self.sprite(u'pacman-mouth-closed.png'),
			self.sprite(u'pacman-frontal.png')
			]
		self.currentSprite = 0

	def show(self, center=True):

		"""
		Shows the creature.

		Keyword arguments:
		center		--	Indicates whether the image should be centered on
						Pacman. (default=True)
		"""

		if self.isMoving():
			self.prevShowDir = self.dir
			self.currentSprite = 1 - self.currentSprite
			img = self.sprites[self.currentSprite]
		else:
			img = self.sprites[-1]
		dx, dy = self.prevShowDir
		if center:
			x = self.maze.width()/2
			y = self.maze.height()/2
		else:
			x, y = self.pos
		w, h = self.size()
		if self.isMoving():
			if dx == 1:
				img = pygame.transform.flip(img, True, False)
			elif dy == 1:
				img = pygame.transform.rotate(img, 90)
			elif dy == -1:
				img = pygame.transform.rotate(img, 270)
		self.win().blit(img, (x*w, y*h))
		# Next, show the score
		self.maze.showText('%d' % self.score, pos=u'top-right')

	def move(self):

		"""Moves in the current direction, without bumping into a wall."""

		self.setNextDir(self.goalDir)
		super(Pacman, self).move()
		if self.maze.eatPearl(self.pos):
			self.score += 1
			if self.score % 50 == 0:
				self.hit50.play()
				self.game.addGhost()
			elif self.score % 10 == 0:
				self.hit10.play()
			else:
				self.hit1.play()

	def setNextDir(self, dir):

		"""
		Sets the direction.

		Arguments:
		dir		--	The new direction, which can be up, down, left, or right, or
					stop.
		"""

		self.goalDir = dir
		_dir = self.dir
		self.setDir(dir)
		nPos = (self.pos[0]+self.dir[0]) % self.maze.width(), \
			(self.pos[1]+self.dir[1]) % self.maze.height()
		if self.maze.wallAt(nPos):
			self.dir = _dir
