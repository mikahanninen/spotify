"""Exceptions for Spotify RPA."""


class SpotifyRPAError(Exception):
    """Base exception for Spotify RPA errors."""
    pass


class PlatformNotSupportedError(SpotifyRPAError):
    """Raised when the current platform is not supported."""
    pass


class AutomationError(SpotifyRPAError):
    """Raised when an automation command fails."""
    pass


class AppleScriptError(AutomationError):
    """Raised when an AppleScript command fails (macOS)."""
    pass


class SpotifyNotRunningError(SpotifyRPAError):
    """Raised when Spotify is not running and an operation requires it."""
    pass
