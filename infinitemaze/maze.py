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
from infinitemaze.grid import Grid
from random import shuffle, randint, sample, choice
import pygame
try:
	import android
	import android.mixer as mixer
except:
	android = None
	import pygame.mixer as mixer

class Maze(object):

	"""The maze-controller class."""

	def __init__(self, game, s=24, w=32, lw=2, r=4, lineCol1='#729fcf', \
		lineCol2='#204a87', wallCol='#3465a4', bgCol='#d3d7cf', fntCol= \
		'#8ae234', fntBgCol='#4e9a06', nGhosts=5, graphics=True, blink=False):

		"""
		Constructor.

		Keyword arguments:
		s		--	The maze size. (default=24)
		w		--	The cell width. (default=24)
		"""

		# Check that the maze has a valid size
		assert(s % 4 == 0)
		
		self.game = game
		self.s = s
		self.w = w
		self.lw = lw
		self.r = r
		self.frameNr = 0
		self.blink = blink
		self.pearlTypes = range(1, 13)
		if graphics:
			self.lineCol1 = pygame.Color(lineCol1)
			self.lineCol2 = pygame.Color(lineCol2)
			self.wallCol = pygame.Color(wallCol)
			self.bgCol = pygame.Color(bgCol)
			self.fntCol = pygame.Color(fntCol)
			self.fntBgCol = pygame.Color(fntBgCol)
			# Load diamond sprites
			self.pList = []
			for path in os.listdir(os.path.join(os.path.dirname(__file__), \
				u'sprites')):
				if u'diamond' not in path:
					continue
				self.pList.append(pygame.image.load(os.path.join( \
					os.path.dirname(__file__), u'sprites', path)))
			assert(len(self.pList) == len(self.pearlTypes))
			self.soundGameOver = mixer.Sound(os.path.join( \
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

	def build(self):

		"""Builds a random maze using Eller's algorithm."""

		self.walls.ellers()
		# Add pearls wherever there are no walls
		for x, y in self.allPos:
			if self.walls[x,y] == 0:
				self.pearls[x,y] = choice(self.pearlTypes)

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

	def clearAt(self, pos):

		"""
		Removes the wall at a certain position.

		Arguments:
		pos		--	An (x,y) tuple with the position.
		"""

		self.walls[pos] = 0
		self.pearls[pos] = choice(self.pearlTypes)

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

	def evolve(self, style=u'directional'):

		"""
		Randomly evolves the maze.

		Keyword arguments:
		style	--	Specifies how the maze should evolve. 'directional',
					'counterdirectional', or 'central'
		"""

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

		# The evolution happens by generating a new random maze, and copying
		# parts of the current maze onto the new maze.
		eMaze = Maze(self.game, graphics=False)
		if style == u'central':
			# Copy the region around the pacman
			minX = s/2-r
			maxX = s/2+r+1
			minY = s/2-r
			maxY = s/2+r+1
		elif style in (u'directional', u'counterdirectional'):
			# Copy the region behind the pacman
			dir = self.pacman.getDir()
			if style == u'counterdirectional':
				dir = -1*dir[0], -1*dir[1]
			if dir == (0, -1): # Up
				minX = 0
				maxX = s
				minY = 0
				maxY = s/2+r+1
			elif dir == (0, 1): # Down
				minX = 0
				maxX = s
				minY = s/2-r
				maxY = s
			elif dir == (1, 0): # Right
				minX = s/2-r
				maxX = s
				minY = 0
				maxY = s
			elif dir == (-1, 0): # Left
				minX = 0
				maxX = s/2+r+1
				minY = 0
				maxY = s
			elif dir == (0, 0): # Stop
				minX = 0
				maxX = s
				minY = 0
				maxY = s
			else:
				raise Exception(u'Invalid dir: %s' % dir)
		else:
			raise Exception(u'Invalid evolveStyle: %s' % style)
		# Now copy a chunk of the current maze onto the new maze.
		for _x in range(minX, maxX):
			eMaze.walls[_x, minY:maxY] = cWalls[_x, minY:maxY]
			eMaze.vis[_x, minY:maxY] = cVis[_x, minY:maxY]
			eMaze.pearls[_x, minY:maxY] = cPearls[_x, minY:maxY]

		# Now deisolate cells that may have become isolated by combining two
		# random mazes.
		for ix in range(0, s, 2):
			for iy in range(0, s, 2):
				isolated = True
				ld = [(0,-1), (0,1), (-1,0), (1,0)]
				shuffle(ld)
				for dx, dy in ld:
					_x = (ix+dx)%s
					_y = (iy+dy)%s
					if eMaze.walls[_x,_y] == 0:
						isolated = False
						break
				if isolated:
					print 'Deisolate!'
					eMaze.clearAt((_x,_y))
		# Uncenter the maze
		x = s - x
		y = s - y
		self.walls = self.centerView(eMaze.walls, (x,y))
		self.vis = self.centerView(eMaze.vis, (x,y))
		self.pearls = self.centerView(eMaze.pearls, (x,y))

	def initWin(self):

		"""Initialize the PyGame window."""

		print 'Initializing window'
		self.win = pygame.display.set_mode(self.resolution())
		print 'Loading font'
		self.fnt = pygame.font.Font(os.path.join(os.path.dirname(__file__), \
			u'fonts', 'FreeMono.ttf'), 64)
		print 'Done'
		#self.rg = self.rg.convert()
		#self.by = self.by.convert()

	def resolution(self):

		"""
		Gets the window resolution.

		Returns:
		An (w, h) tuple.
		"""

		return self.s*self.w, self.s*self.w

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
