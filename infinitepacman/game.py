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

import infinitepacman
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

	def __init__(self, fps=6, evolve=False, center=False, blink=False, intro= \
		True):

		"""
		Constructor.

		Keyword arguments:
		fps			--	The number of frames per second. (default=2)
		evolve		--	Indicates whether the maze should evolve.
						(default=False)
		center		--	Indicates whether the image should be centered in
						Pacman. (default=True)
		"""

		self.maze = Maze(self, blink=blink)
		self.pacman = Pacman(self)
		self.ghosts = []
		self.addGhost(n=2)
		self.frameDur = int(1000. / fps)
		self.evolve = evolve
		self.center = center
		self.blink = blink
		self.intro = intro
		self.persistentGhosts = True
		
	def addGhost(self, n=1):
		
		"""
		Populates the maze with ghosts.
		
		Keyword arguments:
		n		--	The number of ghosts to add. (default=1)
		"""
		
		for i in range(n):
			self.ghosts.append(Ghost(self))
			
	def handleEvents(self):
		
		"""
		Handles keyboard and mouse events.
		
		Returns:
		False if the game was aborted, True otherwise.
		"""
		
		xc = (self.maze.width() * self.maze.cellSize()[0])/2
		yc = (self.maze.height() * self.maze.cellSize()[1])/2
		# Process keypress events
		for e in pygame.event.get():
			# For the PC
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
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
		return True
	
	def introduction(self):
		
		"""Shows the introduction animation."""
		
		imgIns = pygame.image.load(os.path.join( \
			os.path.dirname(infinitepacman.__file__), u'sprites', \
			u'instructions.png'))
		for i in range(5):
			if android != None and android.check_pause():
				android.wait_for_resume()		
			self.win().blit(imgIns, (0,0))
			pygame.display.flip()
		# Process keypress events
		self.wait()
		
		i = 0
		for dir in [u'up', u'right', u'down', u'left'] * 2:
			t0 = pygame.time.get_ticks()
			if i < 8:
				self.maze.showClear()
			else:
				self.maze.show()
			for ghost in self.ghosts:
				ghost.show(center=self.center)
			self.pacman.setDir(dir)
			self.pacman.show(center=self.center)
			pygame.display.flip()
			if android != None and android.check_pause():
				android.wait_for_resume()
			i += 1
			t1 = pygame.time.get_ticks()
			if (t1-t0) < self.frameDur:
				dur = self.frameDur-(t1-t0)
				print 'Sleep %d' % dur
				pygame.time.wait(dur)
				
	def launch(self):

		"""
		Starts a single game.
		
		Returns:
		True if we should play again, False otherwise.
		"""

		self.maze.initWin()
		if self.intro:
			self.introduction()
		# And start the main game loop!
		self.pacman.setDir(u'stop')
		while True:
			t0 = pygame.time.get_ticks()
			# Move pacman and the ghosts. If a ghost and pacman have collided,
			# we don't move the ghost, because that will cause them to jump
			# over eachother
			self.pacman.move()
			for ghost in self.ghosts:
				if ghost.getPos() != self.pacman.getPos():
					ghost.move()
			# Next evolve the maze.
			if self.evolve and (self.pacman.isMoving() or self.blink):
				self.maze.evolve()
				if self.persistentGhosts:
					# Remove walls where there are ghosts
					for ghost in self.ghosts:
						if self.maze.wallAt(ghost.getPos()):
							self.maze.clearAt(ghost.getPos())
				else:
					# Respawn ghosts that are in a wall
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
					self.maze.gameOver()
					return True
			# Sleep to pad the end of the frame
			t1 = pygame.time.get_ticks()
			if (t1-t0) < self.frameDur:
				dur = self.frameDur-(t1-t0)
				print 'Sleep %d' % dur
				pygame.time.wait(dur)
			pygame.display.flip()
			if android != None and android.check_pause():
				android.wait_for_resume()
			# Handle input events and return if the game was aborted
			if not self.handleEvents():
				return False
			
	def wait(self):
		
		"""Pauzes until the screen is tapped or a key is pressed."""
		
		while True:
			for e in pygame.event.get():
				if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
					return
			if android != None and android.check_pause():
				android.wait_for_resume()

	def win(self):
		
		"""
		Return:
		The pygame window.
		"""
		
		return self.maze.win
