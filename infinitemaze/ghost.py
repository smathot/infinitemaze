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

from random import randint, choice
from infinitemaze.creature import Creature

class Ghost(Creature):

	"""A ghost creature."""

	def __init__(self, game):

		"""
		Constructor.

		Arguments:
		game	--	The game object.
		"""

		self.game = game
		self.pacman = game.pacman
		# Select an empty position that is not too close to Pacman.
		px, py = self.pacman.getPos()
		while True:
			x, y = game.maze.emptyPos()
			if abs(x-px) > 2 and abs(y-py) > 2:
				break
		super(Ghost, self).__init__(game, pos=(x,y))

	def loadSprites(self):

		"""Loads the sprites."""

		color = choice( [u'green', u'red', u'blue'] )
		self._sprite = self.sprite(u'ghost-%s-1.png' % color), \
			self.sprite(u'ghost-%s-2.png' % color)

	def move(self):

		"""Moves in the direction of pacman, without bumping into a wall."""

		if not self.isMoving():
			self.setDir(choice([u'left', u'right', u'up', u'down']))
		super(Ghost, self).move()

	def show(self, center=True):

		"""
		Shows the creature.

		Keyword arguments:
		center		--	Indicates whether the image should be centered on
						Pacman. (default=True)
		"""

		x, y = self.pos
		if center:
			mw = self.maze.width()
			mh = self.maze.height()
			px, py = self.pacman.getPos()
			x = ((x-px) + mw/2) % mw
			y = ((y-py) + mh/2) % mh
		dx, dy = self.dir
		w, h = self.size()
		self.win().blit(self._sprite[0], (x*w, y*h))
		self._sprite = self._sprite[1], self._sprite[0]
