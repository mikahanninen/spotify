#!/usr/bin/env python3
"""
Spotify RPA - Command-line entrypoint.

This is the main entrypoint for the Spotify RPA command-line tool.
All functionality is provided by the spotify_rpa package.

Usage:
    python spotify.py play-playlist "Göstän parhaat"
    python spotify.py status
    python spotify.py --help
"""

import sys
from spotify_rpa import main

if __name__ == "__main__":
    sys.exit(main())
