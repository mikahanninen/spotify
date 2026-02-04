"""Integration tests for Spotify RPA.

These tests require an actual Spotify installation and are skipped in CI.
Run locally with: pytest tests/test_integration.py -v
Skip in CI with: pytest --skip-integration
"""

import pytest
import platform

from spotify_rpa import SpotifyRPA, get_platform
from spotify_rpa.exceptions import PlatformNotSupportedError


@pytest.mark.integration
class TestSpotifyIntegration:
    """Integration tests that interact with real Spotify application."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for integration tests."""
        current_platform = get_platform()
        if current_platform not in ("macos", "windows"):
            pytest.skip(f"Integration tests not supported on {current_platform}")
        
        try:
            self.spotify = SpotifyRPA(debug=False)
        except PlatformNotSupportedError:
            pytest.skip("Platform not supported for integration tests")
    
    def test_is_running_check(self):
        """Test checking if Spotify is running."""
        # This should not raise an error
        result = self.spotify.is_running()
        assert isinstance(result, bool)
    
    def test_launch_spotify(self):
        """Test launching Spotify application."""
        if not self.spotify.is_running():
            self.spotify.launch(wait=True)
            assert self.spotify.is_running()
    
    def test_get_player_state(self):
        """Test getting player state."""
        if not self.spotify.is_running():
            pytest.skip("Spotify not running")
        
        state = self.spotify.get_player_state()
        assert state in ("playing", "paused", "stopped")
    
    def test_get_current_track_when_playing(self):
        """Test getting current track info when playing."""
        if not self.spotify.is_running():
            pytest.skip("Spotify not running")
        
        state = self.spotify.get_player_state()
        if state == "stopped":
            pytest.skip("No track playing")
        
        track = self.spotify.get_current_track()
        if track is not None:
            assert track.name is not None
            assert track.artist is not None


@pytest.mark.integration
class TestPlatformSpecific:
    """Platform-specific integration tests."""
    
    @pytest.mark.skipif(platform.system() != "Darwin", reason="macOS only")
    def test_macos_volume_control(self):
        """Test volume control on macOS."""
        spotify = SpotifyRPA()
        if not spotify.is_running():
            pytest.skip("Spotify not running")
        
        # Get current volume
        original_volume = spotify.get_volume()
        assert 0 <= original_volume <= 100
        
        # Set and verify volume (allow ±1 tolerance for Spotify's internal rounding)
        spotify.set_volume(50)
        assert abs(spotify.get_volume() - 50) <= 1
        
        # Restore original volume
        spotify.set_volume(original_volume)
    
    @pytest.mark.skipif(platform.system() != "Windows", reason="Windows only")
    def test_windows_media_keys(self):
        """Test media key functionality on Windows."""
        spotify = SpotifyRPA()
        if not spotify.is_running():
            pytest.skip("Spotify not running")
        
        # Just verify play_pause doesn't raise
        spotify.play_pause()
