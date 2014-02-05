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

import json
import infinitemaze
import shutil
import sys
import os
import subprocess

pgs4a_folder = 'pgs4a-0.9.4' # Must match pgs4a folder

target = os.path.join(pgs4a_folder, 'infinitemaze')
clear_cmd = \
	'./android-sdk/platform-tools/adb shell pm clear nl.cogsci.infinitemaze'
build_cmd = './android.py build infinitemaze release'
if 'install' in sys.argv:
	build_cmd += ' install'

# Recreate target folder
if os.path.exists(target):
	shutil.rmtree(target)
os.mkdir(target)

# Copy necessary files
print 'Copying main.py'
shutil.copyfile('infinitemazeofpacman', os.path.join(target, 'main.py'))
print 'Copying module'
shutil.copytree('infinitemaze', os.path.join(target, 'infinitemaze'))
# Generating .android.json
json.dump(infinitemaze.info, open(os.path.join(target, '.android.json'), 'w'))
print 'Copying android-icon.png'
shutil.copyfile('android/android-icon.png', \
        os.path.join(target, 'android-icon.png'))
print 'Copying android-presplash.png'
shutil.copyfile('android/android-presplash.jpg', \
        os.path.join(target, 'android-presplash.jpg'))

# And build!
print 'Building'
os.chdir(pgs4a_folder)
print 'Clearing application data'
subprocess.call(clear_cmd.split())
print 'Building'
subprocess.call(build_cmd.split())
