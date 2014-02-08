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

# This dictionary is used to generate the .android.json file that pgs4a uses
# to build the package. It also contains some information that is useful for
# non-Android system, notably the version.
info = {
	"version"			: "0.4.0", # Human readable version
	"numeric_version"	: "6", # Android build number
	"name"				: "Infinite Maze of Pac-man",
	"layout"			: "internal",
	"orientation"		: "portrait",
	"package"			: "nl.cogsci.infinitemaze",
	"include_pil"		: True,
	"icon_name"			: "Infinite Maze of Pac-man",
	"permissions"		: ["INTERNET", "VIBRATE"],
	"include_sqlite"	: False,
	}
