"""
Spotify RPA - A cross-platform Python library for automating Spotify desktop application.

This package provides a clean Python interface for controlling the Spotify desktop
application using RPA (Robotic Process Automation) techniques.

Supported platforms:
    - macOS: Full support via AppleScript and System Events
    - Windows: Stub implementation (planned)

Usage:
    from spotify_rpa import SpotifyRPA

    spotify = SpotifyRPA()
    spotify.launch()
    spotify.play_playlist_by_name("My Playlist")

Author: Mika Hänninen
License: MIT
"""

from .models import TrackInfo
from .exceptions import (
    SpotifyRPAError,
    PlatformNotSupportedError,
    AutomationError,
    AppleScriptError,
    SpotifyNotRunningError,
)
from .controller import SpotifyRPA, get_platform, create_spotify_controller
from .cli import main

__all__ = [
    # Main class
    "SpotifyRPA",
    # Factory
    "create_spotify_controller",
    "get_platform",
    # Models
    "TrackInfo",
    # Exceptions
    "SpotifyRPAError",
    "PlatformNotSupportedError",
    "AutomationError",
    "AppleScriptError",
    "SpotifyNotRunningError",
    # CLI
    "main",
]

__version__ = "1.0.0"
