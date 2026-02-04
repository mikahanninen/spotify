"""Tests for spotify_rpa.exceptions module."""

import pytest
from spotify_rpa.exceptions import (
    SpotifyRPAError,
    PlatformNotSupportedError,
    AutomationError,
    AppleScriptError,
    SpotifyNotRunningError,
)


class TestExceptions:
    """Tests for custom exception classes."""
    
    def test_spotify_rpa_error_is_base(self):
        """Test SpotifyRPAError is the base exception."""
        error = SpotifyRPAError("test error")
        assert isinstance(error, Exception)
        assert str(error) == "test error"
    
    def test_platform_not_supported_error(self):
        """Test PlatformNotSupportedError inherits from SpotifyRPAError."""
        error = PlatformNotSupportedError("Linux not supported")
        assert isinstance(error, SpotifyRPAError)
        assert "Linux" in str(error)
    
    def test_automation_error(self):
        """Test AutomationError inherits from SpotifyRPAError."""
        error = AutomationError("Automation failed")
        assert isinstance(error, SpotifyRPAError)
    
    def test_applescript_error(self):
        """Test AppleScriptError inherits from AutomationError."""
        error = AppleScriptError("Script failed")
        assert isinstance(error, AutomationError)
        assert isinstance(error, SpotifyRPAError)
    
    def test_spotify_not_running_error(self):
        """Test SpotifyNotRunningError inherits from SpotifyRPAError."""
        error = SpotifyNotRunningError("Spotify is not running")
        assert isinstance(error, SpotifyRPAError)
    
    def test_exception_can_be_raised_and_caught(self):
        """Test exceptions can be raised and caught properly."""
        with pytest.raises(SpotifyRPAError):
            raise PlatformNotSupportedError("test")
        
        with pytest.raises(AutomationError):
            raise AppleScriptError("test")
    
    def test_exception_hierarchy(self):
        """Test the exception hierarchy is correct."""
        # All should be catchable by SpotifyRPAError
        exceptions = [
            PlatformNotSupportedError("test"),
            AutomationError("test"),
            AppleScriptError("test"),
            SpotifyNotRunningError("test"),
        ]
        
        for exc in exceptions:
            assert isinstance(exc, SpotifyRPAError)
