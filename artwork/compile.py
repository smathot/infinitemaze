#!/usr/bin/env python
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
from subprocess import call

for src in os.listdir('svg'):
	# Determine DPI
	if 'diamond' in src or src == 'instructions.svg':
		dpi = '90'
	elif src == 'android-icon.svg':
		dpi = '240'
	else:
		dpi = '120'
	# Determine destination
	dest = os.path.splitext(src)[0] + '.png'
	if src == 'android-icon.svg':
		dest = '../android/' + dest
	else:
		dest = '../infinitemaze/sprites/' + dest
	cmd = ['inkscape', '-f', 'svg/'+src, '-e', dest, '-d', dpi]
	if call(cmd) != 0:
		raise Exception('Failed to convert')

