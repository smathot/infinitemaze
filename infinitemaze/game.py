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

import infinitemaze
from infinitemaze.maze import Maze
from infinitemaze.pacman import Pacman
from infinitemaze.ghost import Ghost
from random import random
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

	def __init__(self, fps=6, evolve=0, center=False, blink=False,
		intro=True, evolveIncrease=0, goalScore=None, musicFile=None, win=None,
		banner=None, js=None, showInstructions=True, rotDur=4):

		"""
		Constructor.

		Keyword arguments:
		fps			--	The number of frames per second. (default=2)
		evolve		--	Indicates the chance of a maze evolution.
						(default=0)
		center		--	Indicates whether the image should be centered in
						Pacman. (default=True)
		evolveIncrease	--	The value to be added to evolve with each step.
							(default=0)
		goalScore	--	The score at which you win the game or None for
						infinite gameplay. (default=None)
		musicFile	--	The path to a music file for in-game music.
						(default=None)
		win			--	The PyGame window or None to initialize. (default=None)
		banner		--	A banner image that is presented to the right of the
						maze to pad non-square resolutions. (default=None)
		js			--	A joystick object. (default=None)
		showInstructions	--	Indicates whether an instruction screen
								should be shown. (default=True)
		rotDur		--	The number of rotations that pac-man makes prior to the
						game. (default=4)
		"""

		self.maze = Maze(self, blink=blink, banner=banner)
		self.pacman = Pacman(self)
		self.ghosts = []
		self.addGhost(n=2)
		self.frameDur = int(1000. / fps)
		self.evolve = evolve
		self.evolveIncrease = evolveIncrease
		self.center = center
		self.blink = blink
		self.intro = intro
		self.persistentGhosts = True
		self.goalScore = goalScore
		self.musicFile = musicFile
		self.musicFadeout = 4000
		self.musicVolume = .5
		self._win = win
		self.js = js
		self.showInstructions = showInstructions
		self.rotDur = rotDur

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
			# Optionally use the joystick
			elif self.js != None and e.type == pygame.JOYBUTTONDOWN:
				if e.button == 8: # start button
					return False
			elif self.js != None and e.type == pygame.JOYAXISMOTION:
				dx = 0
				dy = 0
				for i in range(self.js.get_numaxes()):
					if self.js.get_axis(i) == 0:
						continue
					if i % 2 == 0:
						dx = self.js.get_axis(i)
					else:
						dy = self.js.get_axis(i)
				if abs(dx) > abs(dy):
					if dx < 0:
						self.pacman.setNextDir(u'left')
					elif dx > 0:
						self.pacman.setNextDir(u'right')
				else:
					if dy < 0:
						self.pacman.setNextDir(u'up')
					elif dy > 0:
						self.pacman.setNextDir(u'down')
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

		if self.showInstructions:
			imgIns = pygame.image.load(os.path.join( \
				os.path.dirname(infinitemaze.__file__), u'sprites', \
				u'instructions.png'))
			for i in range(5):
				if android != None and android.check_pause():
					android.wait_for_resume()
				self.maze.show()
				self.win().blit(imgIns, (0,0))
				pygame.display.flip()
		# Process keypress events
		if not self.wait():
			return False
		if self.musicFile != None:
			mixer.music.play()
			pygame.time.wait(200)
		i = 0
		for dir in [u'up', u'right', u'down', u'left'] * self.rotDur:
			t0 = pygame.time.get_ticks()
			self.maze.show()
			for ghost in self.ghosts:
				ghost.show(center=self.center)
			self.pacman.setDir(dir)
			self.pacman.show(center=self.center)
			if self.goalScore != None:
				self.maze.showText('Reach %d points!' % self.goalScore)
			pygame.display.flip()
			if android != None and android.check_pause():
				android.wait_for_resume()
			i += 1
			t1 = pygame.time.get_ticks()
			if (t1-t0) < self.frameDur:
				dur = self.frameDur-(t1-t0)
				print 'Sleep %d' % dur
				pygame.time.wait(dur)
		return True

	def launch(self):

		"""
		Starts a single game.

		Returns:
		True if we should play again, False otherwise.
		"""

		self.maze.initWin(self._win)
		# Initialize music
		if self.musicFile != None:
			mixer.music.load(self.musicFile)
			mixer.music.set_volume(self.musicVolume)
		if self.intro:
			if not self.introduction():
				return True
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
			if random() <= self.evolve and (self.pacman.isMoving() or \
				self.blink):
				self.maze.evolve(style=u'directional')
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
			# Evolve the evolution!
			self.evolve += self.evolveIncrease
			print 'Evolve %.2f' % self.evolve
			# Show the maze, followed by the ghosts, followed by pacman. Pacman
			# also draws the scoreboard.
			self.maze.show(center=self.center)
			for ghost in self.ghosts:
				ghost.show(center=self.center)
			self.pacman.show(center=self.center)
			# Check if we're game over
			for ghost in self.ghosts:
				if ghost.getPos() == self.pacman.getPos():
					if self.musicFile != None:
						mixer.music.fadeout(self.musicFadeout)
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
				if self.musicFile != None:
					mixer.music.fadeout(self.musicFadeout)
				return False
			# Check if we've won
			if self.goalScore != None and self.getScore() >= self.goalScore:
				if self.musicFile != None:
					mixer.music.fadeout(self.musicFadeout)
				self.maze.gameWon()
				return True

	def getScore(self):

		"""
		Returns:
		The game score.
		"""

		return self.pacman.getScore()

	def wait(self):

		"""Pauzes until the screen is tapped or a key is pressed."""

		# First flush
		for e in pygame.event.get():
			pass
		# And then wait
		while True:
			for e in pygame.event.get():
				if e.type == pygame.KEYDOWN:
					if e.key == pygame.K_ESCAPE:
						return False
					return True
				if e.type == pygame.MOUSEBUTTONDOWN:
					return True
				if self.js != None and e.type == pygame.JOYBUTTONDOWN:
					if e.button == 8: # start button
						return False
					return True
			if android != None and android.check_pause():
				android.wait_for_resume()

	def win(self):

		"""
		Return:
		The pygame window.
		"""

		return self.maze.win
