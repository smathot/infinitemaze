# Infinite Maze of Pac-man

*The change-blindness game*

Copyright 2014  
Sebastiaan Mathôt <s.mathot@cogsci.nl> (Concept and development)  
Theo Danes <theo@theodanes.nl> (Artwork and design)

## Overview

%--
toc:
 mindepth: 2
--%

## About

*Infinite Maze of Pac-man* is a simple game for Android in the Pac-man tradition. What makes this game unique is that it exploits the psychological phenomenon of change blindness to make the maze literally ... infinite!

## Download

### Source code

- <https://github.com/smathot/infinitemaze/releases>

### Android (Google Play Store)

Available soon.

## Build instructions

### Dependencies

- [Python][]
- [PyGame][]
- [PyGame subset for Android][pgs4a]

### Android

Change the `pgs4a_folder` variable in `setup-android.py` so that it points to the folder where the [PyGame subset for Android][pgs4a] is installed.

Next, run the following command to build the package ...

	python setup-android.py

... or the following command to build the package and immediately transfer it
to your device:

	python setup-android.py install
	
## License

`artwork/svg/*` and `infinitemaze/sprites/*` are released under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. Credit should be attributed to Theo Danes.

`infinitemaze/sounds/*` are released under a Creative Commons Attributions 3.0 International license. Credit should be attributed to the original creators of <http://opengameart.org/>.

All other content is released under the GNU general public license v3. For details, see the enclosed file `COPYING`, or visit:

- <http://www.gnu.org/licenses/gpl-3.0.txt>

[pgs4a]: http://pygame.renpy.org/
[pygame]: http://www.pygame.org/
[python]: http://www.python.org/
