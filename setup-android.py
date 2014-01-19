#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.

Usage
=====

Assumptions
-----------

- The PyGame subset for Android is installed in the folder indicated under
`pgs4a_folder`.
- The Python modules are installed in the folder indicated under
`module_folder`

Build environment
-----------------

Currently, most development is done on Kubuntu 13.04. Most of the dependencies
for pgs4a are described on their homepage, but in addition you need to install
the Oracle Java JDK (v8 currently used). This is available from
`ppa:webupd8team/java`. Instructions taken from:

- <http://www.mameau.com/pygame-subset-for-android-pgs4a-on-ubuntu-precise-12-04/>

Building
--------

Build the `.apk` with the following command:

	python setup-android.py [install]

The `install` parameter is optional, and indicates that the `.apk` should be
installed on an attached Android device or emulator. The resulting `.apk` can
be found in the `bin` subfolder of the PyGame subset for Android folder.
"""

import shutil
import sys
import os
import subprocess

pgs4a_folder = 'pgs4a-0.9.4'
target = os.path.join(pgs4a_folder, 'infinitemaze')
module_folder = '/usr/lib/python2.7'
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
shutil.copyfile('pacman', os.path.join(target, 'main.py'))
print 'Copying module'
shutil.copytree('infinitepacman', os.path.join(target, 'infinitepacman'))
print 'Copying .android.json'
shutil.copyfile('android/android.json', os.path.join(target, '.android.json'))
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
