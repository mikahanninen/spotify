"""Factory and facade for Spotify controllers."""

import platform

from .base import SpotifyControllerBase
from .exceptions import PlatformNotSupportedError


def get_platform() -> str:
    """
    Detect the current operating system.
    
    Returns:
        One of: "macos", "windows", "linux"
    """
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    return system


def create_spotify_controller(
    platform_name: str,
    debug: bool = False
) -> SpotifyControllerBase:
    """
    Create a platform-appropriate Spotify controller.
    
    Args:
        platform_name: The platform to create a controller for.
        debug: If True, enable debug output.
    
    Returns:
        A SpotifyControllerBase instance for the specified platform.
    
    Raises:
        PlatformNotSupportedError: If the platform is not supported.
    """
    if platform_name == "macos":
        from .macos import MacOSSpotifyController
        return MacOSSpotifyController(debug=debug)
    elif platform_name == "windows":
        from .windows import WindowsSpotifyController
        return WindowsSpotifyController(debug=debug)
    else:
        raise PlatformNotSupportedError(
            f"Platform '{platform_name}' is not supported. "
            "Supported platforms: macOS, Windows (stub)"
        )


class SpotifyRPA:
    """
    A cross-platform Python RPA interface for Spotify.
    
    This class automatically detects the operating system and uses the
    appropriate platform-specific controller.
    
    Example:
        >>> spotify = SpotifyRPA()
        >>> spotify.launch()
        >>> spotify.play_playlist_by_name("My Playlist")
    """
    
    def __init__(self, debug: bool = False):
        """
        Initialize the SpotifyRPA controller.
        
        Args:
            debug: If True, print debug information during execution.
        """
        self.platform = get_platform()
        self.debug = debug
        self._controller = create_spotify_controller(self.platform, debug=debug)
    
    def __getattr__(self, name):
        """Delegate all method calls to the platform-specific controller."""
        return getattr(self._controller, name)
