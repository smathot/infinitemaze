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

class Creature(object):

	"""Class description."""

	def __init__(self, game, pos=None, dir=(0,0)):

		"""
		Constructor.

		Arguments:
		game	--	The Game object.

		Keyword arguments:
		pos		--	An (x,y) tuple with the initial position, or None to
					randomly select an empty position. (default=None)
		dir		--	A (dx, dy) tuple with the initial direction. (default=(0,0))
		"""

		self.game = game
		self.maze = game.maze
		if pos == None:
			pos = self.maze.emptyPos()
		self.pos = pos
		self.dir = dir
		self.loadSprites()

	def isMoving(self):

		"""
		Returns:
		True if the creature is moving, False otherwise.
		"""
		return self.dir != (0,0)

	def getPos(self):

		"""
		Returns:
		An (x,y) tuple with the creature's position.
		"""

		return self.pos

	def move(self):

		"""Moves in the current direction, without bumping into a wall."""

		nPos = (self.pos[0]+self.dir[0]) % self.maze.width(), \
			(self.pos[1]+self.dir[1]) % self.maze.height()
		if not self.maze.wallAt(nPos):
			self.pos = nPos
		else:
			self.setDir(u'stop')

	def loadSprites(self):

		"""Loads the sprites."""

		raise NotImplementedError(u'Please subclass Creature')

	def setDir(self, dir):

		"""
		Sets the direction.

		Arguments:
		dir		--	The new direction, which can be up, down, left, or right, or
					stop.
		"""

		if dir == u'up':
			self.dir = 0, -1
		elif dir == u'down':
			self.dir = 0, 1
		elif dir == u'left':
			self.dir = -1, 0
		elif dir == u'right':
			self.dir = 1, 0
		elif dir == u'stop':
			self.dir = 0, 0
		else:
			raise Exception(u'Invalid direction!')

	def show(self):

		"""
		Shows the creature.

		Keyword arguments:
		center		--	Indicates whether the image should be centered on
						Pacman. (default=True)
		"""

		raise NotImplementedError(u'Please subclass Creature')

	def size(self):

		"""
		Returns:
		An (x, y) tuple with the sprite dimensions.
		"""

		return self.maze.cellSize()

	def sprite(self, name):

		"""
		Returns:
		A PyGame surface with the sprite.
		"""

		return pygame.transform.smoothscale(pygame.image.load(os.path.join( \
			os.path.dirname(__file__), u'sprites', name)), self.size())

	def win(self):

		"""
		Returns:
		The PyGame window.
		"""

		return self.maze.win
