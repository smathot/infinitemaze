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
from infinitepacman.grid import Grid
from random import shuffle, randint, sample, choice
import pygame
from matplotlib import pyplot as plt

class Maze(object):

	"""The maze-controller class."""

	def __init__(self, s=20, w=32, lw=3, r=5, lineCol1='#729fcf', lineCol2= \
		'#204a87', wallCol='#3465a4', bgCol='#d3d7cf', fntCol='#8ae234', \
		fntBgCol='#4e9a06', nGhosts=5, graphics=True, blink=False):

		"""
		Constructor.

		Keyword arguments:
		s		--	The maze size. (default=24)
		w		--	The cell width. (default=24)
		"""

		assert(s % 4 == 0)

		self.s = s
		self.w = w
		self.lw = lw
		self.r = r
		self.frameNr = 0
		self.blink = blink
		if graphics:
			self.lineCol1 = pygame.Color(lineCol1)
			self.lineCol2 = pygame.Color(lineCol2)
			self.wallCol = pygame.Color(wallCol)
			self.bgCol = pygame.Color(bgCol)
			self.fntCol = pygame.Color(fntCol)
			self.fntBgCol = pygame.Color(fntBgCol)
			# Load sprites and resize them to the proper size
			self.pList = [pygame.transform.smoothscale(pygame.image.load( \
				u'infinitepacman/sprites/pearl%d.png' % i), (self.w/3, self.w/3) ) \
				for i in range(1,5)]
			self.soundGameOver = pygame.mixer.Sound(os.path.join( \
				os.path.dirname(__file__), u'sounds', u'gameOver.ogg'))
		# Build a list of all positions
		self.allPos = []
		for x in range(self.s):
			for y in range(self.s):
				self.allPos.append( (x,y) )
		self.walls, self.vis, self.pearls = self.grid()
		t0 = pygame.time.get_ticks()
		self.build()
		t1 = pygame.time.get_ticks()
		print '\t%d build time' % (t1-t0)

	def build(self, exit=None):

		"""
		Builds a random maze using depth-first search.

		Keyword arguments:
		reset		--	Indicates whether the array should
		exit		--	The exit position. (default=(1,1))
		"""

		if exit == None:
			exit = self.s/2, self.s/2
		# Randomly build walls
		nPos = [ (-2, 0), (2, 0), (0, -2), (0, 2) ]
		self.vis[exit] = 1
		shuffle(nPos)
		for dx, dy in nPos:
			_dx = (exit[0]+dx) % self.s
			_dy = (exit[1]+dy) % self.s
			wx = (exit[0]+dx/2) % self.s
			wy = (exit[1]+dy/2) % self.s
			if self.vis[_dx, _dy] == 0:
				self.walls[wx, wy] = 0
				exit = _dx, _dy
				self.build(exit=exit)
		# Add pearls wherever there are no walls
		for x, y in self.allPos:
			if self.walls[x,y] == 0:
				self.pearls[x,y] = randint(1,4)

	def centerView(self, a, pos=None):

		"""
		Centers an array.

		Arguments:
		a		--	An array.

		Keyword arguments:
		pos		--	The position to center on, or None to use Pacman's position.
					(default=None)
Returns:
		A centered array.
		"""

		if pos != None:
			x, y = pos
		else:
			x, y = self.pacman.getPos()
		cx, cy = a.shape
		dx, dy = cx/2-x, cy/2-y
		a = a.roll(dx, axis=0)
		a = a.roll(dy, axis=1)
		return a

	def cellSize(self):

		"""
		Returns:
		An (w, h) tuple with the cell dimensions.
		"""

		return self.w, self.w

	def eatPearl(self, pos):

		"""
		Removes (eat) the pearl at the specified position.

		Arguments:
		pos		--	An (x,y) tuple with the position.

		Returns:
		True if a pearl was eaten, False if not.
		"""

		eaten = self.pearls[pos] > 0
		self.pearls[pos] = 0
		return eaten

	def gameOver(self):

		"""Shows the game-over message."""

		self.soundGameOver.play()
		self.showText(u'Game over!', pos=u'center')
		pygame.display.flip()
		pygame.time.wait(1000)
		self.show()
		s = u'Score: %d!' % self.pacman.getScore()
		for i in range(len(s)+1):
			self.showText(s[:i], pos=u'center')
			pygame.display.flip()
			pygame.time.wait(50)
		pygame.time.wait(1000)

	def grid(self):

		"""
		Creates an empty grid for the maze.

		Returns:
		A (walls, vis, pearls) tuple of initialized arrays.
		"""

		walls = Grid((self.s, self.s))
		walls.addStripes()
		vis = Grid((self.s, self.s))
		pearls = Grid((self.s, self.s))
		return walls, vis, pearls

	def height(self):

		"""
		Returns:
		The maze height.
		"""

		return self.s

	def emptyPos(self):

		"""
		Get a random empty position.

		Returns:
		An (x,y) tuple.
		"""

		l = []
		for x, y in self.allPos:
			if self.walls[x,y] == 0:
				l.append((x,y))
		return choice(l)

	def evolve(self):

		"""Randomly evolve the maze."""

		t0 = pygame.time.get_ticks()
		s = self.s
		r = self.r
		x, y = self.pacman.getPos()
		if x % 2 == 1:
			x += 1
		if y % 2 == 1:
			y += 1
		x = x % s
		y = y % s
		# Center the arrays on the Pacman
		cWalls = self.centerView(self.walls, (x,y))
		cVis = self.centerView(self.vis, (x,y))
		cPearls = self.centerView(self.pearls, (x,y))
		# Create a new entirely random maze and fill the region around the
		# PacMan with the current maze.
		eMaze = Maze(graphics=False)
		for _x in range(s/2-r, s/2+r+1):
			eMaze.walls[_x, s/2-r:s/2+r+1] = cWalls[_x, s/2-r:s/2+r+1]
			eMaze.vis[_x, s/2-r:s/2+r+1] = cVis[_x, s/2-r:s/2+r+1]
		eMaze.build()
		for _x in range(s/2-r, s/2+r+1):
			eMaze.pearls[_x, s/2-r:s/2+r+1] = cPearls[_x, s/2-r:s/2+r+1]
		# Uncenter the maze
		x = s - x
		y = s - y
		self.walls = self.centerView(eMaze.walls, (x,y))
		self.vis = self.centerView(eMaze.vis, (x,y))
		self.pearls = self.centerView(eMaze.pearls, (x,y))

	def initWin(self):

		"""Initialize the PyGame window."""

		self.win = pygame.display.set_mode((self.s*self.w, self.s*self.w))
		self.fnt = pygame.font.SysFont('Bandal', 64, bold=True)

	def setPacman(self, pacman):

		"""
		Sets the pacman.

		Arguments:
		pacman		--	A Pacman object.
		"""

		self.pacman = pacman

	def show(self, center=True):

		"""
		Shows a single frame.

		Keyword arguments:
		center		--	Indicates whether the image should be centered on
						Pacman. (default=True)
		"""

		if center:
			_walls = self.walls
			_pearls = self.pearls
			self.pearls = self.centerView(self.pearls)
			self.walls = self.centerView(self.walls)
		self.showClear()
		self.showWalls()
		if not self.blink or self.frameNr % 2 == 0:
			self.showPearls()
		if center:
			self.walls = _walls
			self.pearls = _pearls
		self.frameNr += 1

	def showClear(self):

		"""Clears the window."""

		self.win.fill(self.bgCol)

	def showPearls(self):

		"""Shows the pearls of the maze."""

		for x, y in self.allPos:
			if self.pearls[x,y] > 0:
				img = self.pList[self.pearls[x,y]-1]
				_x = x*self.w + (self.w-img.get_width())/2
				_y = y*self.w + (self.w-img.get_height())/2
				self.win.blit(img, (_x, _y))

	def showWalls(self):

		"""Shows the walls."""

		for x, y in self.allPos:
			if self.walls[x,y] > 0:
				pygame.draw.rect(self.win, self.wallCol, (x*self.w, \
					y*self.w, self.w, self.w))
				nPos = [ (-1, 0), (1, 0), (0, -1), (0, 1) ]
				for dx, dy in nPos:
					_x = (x+dx) % self.s
					_y = (y+dy) % self.s
					if self.walls[_x, _y] == 0:
						if dx == 1:
							pygame.draw.line(self.win, self.lineCol1, \
								(x*self.w+self.w, y*self.w), (x*self.w+ \
								self.w, y*self.w+self.w), self.lw)
						elif dx == -1:
							pygame.draw.line(self.win, self.lineCol2, \
								(x*self.w, y*self.w), (x*self.w, y*self.w+ \
								self.w), self.lw)
						elif dy == 1:
							pygame.draw.line(self.win, self.lineCol2, \
								(x*self.w, y*self.w+self.w), (x*self.w+ \
								self.w, y*self.w+self.w), self.lw)
						else:
							pygame.draw.line(self.win, self.lineCol1, \
								(x*self.w, y*self.w), (x*self.w+self.w, \
								y*self.w), self.lw)

	def showText(self, msg, pos=u'center'):

		"""
		Shows a string of text.

		Arguments:
		msg		--	The text to show.

		Keyword arguments:
		pos		--	'top-right' or 'center'
		"""

		txt = self.fnt.render(msg, 1, self.fntCol)
		if pos == u'top-right':
			subWin = self.win.subsurface((self.w*self.s-txt.get_width()-30, \
				10, txt.get_width()+20, txt.get_height()+20))
		elif pos == u'center':
			subWin = self.win.subsurface( \
				(self.w*self.s)/2-txt.get_width()/2-10,
				(self.w*self.s)/2-txt.get_height()/2-110,
				txt.get_width()+20, txt.get_height()+20)
		subWin.fill(self.fntBgCol)
		subWin.blit(txt, (10, 10))

	def wallAt(self, pos):

		"""
		Checks whether there is a wall at a given position.

		Arguments:
		pos		--	An (x,y) tuple with the position to check.

		Returns:
		True if there is a wall at the position, False otherwise.
		"""

		return self.walls[pos] > 0

	def width(self):

		"""
		Returns:
		The maze width.
		"""

		return self.s