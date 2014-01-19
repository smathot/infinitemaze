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

from infinitepacman.maze import Maze
from infinitepacman.pacman import Pacman
from infinitepacman.ghost import Ghost
import os
import pygame
try:
	import android
	import android.mixer as mixer
except:
	android = None
	import pygame.mixer as mixer

class Game(object):

	"""The game-controller class."""

	def __init__(self, fps=6, evolve=False, center=False, blink=False, sound= \
		True, music=False):

		"""
		Constructor.

		Keyword arguments:
		fps			--	The number of frames per second. (default=2)
		evolve		--	Indicates whether the maze should evolve.
						(default=False)
		center		--	Indicates whether the image should be centered in
						Pacman. (default=True)
		"""

		self.maze = Maze(blink=blink)
		self.pacman = Pacman(self.maze)
		self.ghosts = []
		for i in range(2):
			self.ghosts.append(Ghost(self.maze, self.pacman))
		self.frameDur = int(1000. / fps)
		self.evolve = evolve
		self.center = center
		self.blink = blink
		self.sound = sound
		self.music = music

	def launch(self):

		"""Starts the game."""

		self.maze.initWin()
		xc = (self.maze.width() * self.maze.cellSize()[0])/2
		yc = (self.maze.height() * self.maze.cellSize()[1])/2
		if self.music:
			print 'Initializing music'
			music = mixer.Sound(os.path.join(os.path.dirname(__file__),
				u'sounds', u'goof.ogg'), loops=-1)
			music.set_volume(.25)
		if self.sound:
			print 'Initializing startSound'
			startSound = mixer.Sound(os.path.join(os.path.dirname( \
				__file__), u'sounds', u'hit1.ogg'))
		# Intro animation!
		print 'Intro animation ...'
		for dir in [u'up', u'right', u'down', u'left'] * 2:
			self.maze.showClear()
			for ghost in self.ghosts:
				ghost.show(center=self.center)
			self.pacman.setDir(dir)
			self.pacman.show(center=self.center)
			if self.sound:
				startSound.play()
			pygame.display.flip()
			if android != None and android.check_pause():
				android.wait_for_resume()
			pygame.time.wait(self.frameDur)

		if self.music:
			music.play()

		# And start the main game loop!
		while True:
			t0 = pygame.time.get_ticks()
			# Add ghosts if necessary
			if self.pacman.getScore() % 50 == 0:
				self.ghosts.append(Ghost(self.maze, self.pacman))
			# Move pacman and the ghosts. If a ghost and pacman have collided,
			# we don't move the ghost, because that will cause them to jump
			# over eachother
			self.pacman.move()
			for ghost in self.ghosts:
				if ghost.getPos() != self.pacman.getPos():
					ghost.move()
			# Next evolve the maze. If the evolution kills a ghost, replace it
			# by a new ghgost
			if self.evolve and (self.pacman.isMoving() or self.blink):
				self.maze.evolve()
				_ghosts = []
				for ghost in self.ghosts:
					if self.maze.wallAt(ghost.getPos()):
						ghost = Ghost(self.maze, self.pacman)
					_ghosts.append(ghost)
				self.ghosts = _ghosts
			# Show the maze, followed by the ghosts, followed by pacman. Pacman
			# also draws the scoreboard.
			self.maze.show(center=self.center)
			for ghost in self.ghosts:
				ghost.show(center=self.center)
			self.pacman.show(center=self.center)
			# Check if we're game over
			for ghost in self.ghosts:
				if ghost.getPos() == self.pacman.getPos():
					if self.music:
						music.fadeout(1000)
					self.maze.gameOver()
					return True
			# Process keypress events
			for e in pygame.event.get():
				# For the PC
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_ESCAPE:
						if self.music:
							music.fadeout(1000)
						return False
					elif e.key == pygame.K_UP:
						self.pacman.setNextDir(u'up')
					elif e.key == pygame.K_DOWN:
						self.pacman.setNextDir(u'down')
					elif e.key == pygame.K_LEFT:
						self.pacman.setNextDir(u'left')
					elif e.key == pygame.K_RIGHT:
						self.pacman.setNextDir(u'right')
				# Tapping on the screen also steers the Pacman (for Android)
				elif e.type == pygame.MOUSEBUTTONDOWN:
					x, y = e.pos
					dx = x-xc
					dy = y-yc
					print x, y, dx, dy
					if abs(dx) > abs(dy):
						if dx > 0:
							self.pacman.setNextDir(u'right')
						else:
							self.pacman.setNextDir(u'left')
					elif dy > 0:
						self.pacman.setNextDir(u'down')
					else:
						self.pacman.setNextDir(u'up')
			t1 = pygame.time.get_ticks()
			if (t1-t0) < self.frameDur:
				dur = self.frameDur-(t1-t0)
				print 'Sleep %d' % dur
				pygame.time.wait(dur)
			pygame.display.flip()
			if android != None and android.check_pause():
				android.wait_for_resume()
