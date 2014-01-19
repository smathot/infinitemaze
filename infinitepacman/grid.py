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

class Grid(object):

	"""
	A 2D grid object for the walls, ghosts, and pearls to live on. For
	compatibility with pgs4a, we cannot use numpy functionality, which makes
	this class a bit slow and clunky.
	"""

	def __init__(self, shape):

		"""
		Constructor.

		Arguments:
		shape	--	A (w, h) tuple to specify the grid dimensions or a list
					to take as starting grid.
		"""

		if isinstance(shape, list):
			self.l = shape
			self.shape = len(shape), len(shape[0])
		else:
			self.shape = shape
			self.l = []
			for x in range(self.shape[0]):
				self.l.append([0]*self.shape[1])

	def __getitem__(self, xy):

		"""Implements the getter, like so: `print a[x, y]`."""

		x, y = xy
		return self.l[x][y]

	def __setitem__(self, xy, val):

		"""Implements the setter, like so: `a[x, y] = 1`."""

		x, y = xy
		self.l[x][y] = val

	def addStripes(self):

		"""
		Fills the grid with a striped pattern, like so:

		-X-X-
		XXXXX
		-X-X-
		"""

		for x in range(self.shape[0]):
			for y in range(self.shape[1]):
				if x % 2 == 0 and y % 2 == 0:
					self.l[x][y] = 0
				else:
					self.l[x][y] = 1

	def __str__(self):

		"""Prints a representation of the grid."""

		s = ''
		for x in range(self.shape[0]):
			for y in range(self.shape[1]):
				s += str(self.l[x][y])
			s += '\n'
		return s

	def roll(self, d, axis=0):

		"""
		Implements np.roll(), in which the Grid is rotated across a particular
		axis.

		Arguments:
		d		--	The distance to roll.

		Keyword arguments:
		axis	--	The axis, with 0 being x and 1 being y. (default=0)

		Returns:
		A new Grid that has been rolled.
		"""

		if axis == 0:
			l = self.l[-d:] + self.l[:-d]
		else:
			l = []
			for x in range(self.shape[0]):
				l.append(self.l[x][-d:] + self.l[x][:-d])
		return Grid(l)
