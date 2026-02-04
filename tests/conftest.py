"""Pytest configuration and shared fixtures."""

import pytest
from unittest.mock import MagicMock

from spotify_rpa.models import TrackInfo


@pytest.fixture
def sample_track():
    """Create a sample TrackInfo for testing."""
    return TrackInfo(
        name="Test Song",
        artist="Test Artist",
        album="Test Album",
        duration_ms=180000,
        spotify_url="spotify:track:abc123def456"
    )


@pytest.fixture
def mock_controller():
    """Mock controller for testing without real automation."""
    controller = MagicMock()
    controller.is_running.return_value = True
    controller.get_player_state.return_value = "playing"
    controller.is_playing.return_value = True
    controller.get_volume.return_value = 50
    controller.get_player_position.return_value = 30.0
    controller.get_current_track.return_value = TrackInfo(
        name="Mock Song",
        artist="Mock Artist",
        album="Mock Album",
        duration_ms=200000,
        spotify_url="spotify:track:mock123"
    )
    return controller


@pytest.fixture
def mock_spotify(mock_controller):
    """Mock SpotifyRPA instance."""
    from unittest.mock import patch
    
    with patch("spotify_rpa.controller.create_spotify_controller", return_value=mock_controller):
        from spotify_rpa import SpotifyRPA
        spotify = MagicMock(spec=SpotifyRPA)
        spotify._controller = mock_controller
        spotify.platform = "macos"
        spotify.debug = False
        
        # Forward method calls to mock controller
        spotify.is_running = mock_controller.is_running
        spotify.get_player_state = mock_controller.get_player_state
        spotify.is_playing = mock_controller.is_playing
        spotify.get_current_track = mock_controller.get_current_track
        spotify.get_volume = mock_controller.get_volume
        spotify.get_player_position = mock_controller.get_player_position
        
        return spotify
