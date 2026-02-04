"""Tests for spotify_rpa.models module."""

import pytest
from spotify_rpa.models import TrackInfo


class TestTrackInfo:
    """Tests for TrackInfo dataclass."""
    
    def test_track_info_creation(self):
        """Test basic TrackInfo creation."""
        track = TrackInfo(
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration_ms=180000,
            spotify_url="spotify:track:abc123"
        )
        
        assert track.name == "Test Song"
        assert track.artist == "Test Artist"
        assert track.album == "Test Album"
        assert track.duration_ms == 180000
        assert track.spotify_url == "spotify:track:abc123"
    
    def test_duration_seconds_property(self):
        """Test duration_seconds conversion."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=180000,
            spotify_url=""
        )
        
        assert track.duration_seconds == 180.0
    
    def test_duration_seconds_zero(self):
        """Test duration_seconds with zero duration."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=0,
            spotify_url=""
        )
        
        assert track.duration_seconds == 0.0
    
    def test_web_url_track(self):
        """Test web_url conversion for tracks."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=0,
            spotify_url="spotify:track:abc123def456"
        )
        
        assert track.web_url == "https://open.spotify.com/track/abc123def456"
    
    def test_web_url_album(self):
        """Test web_url conversion for albums."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=0,
            spotify_url="spotify:album:xyz789"
        )
        
        assert track.web_url == "https://open.spotify.com/album/xyz789"
    
    def test_web_url_playlist(self):
        """Test web_url conversion for playlists."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=0,
            spotify_url="spotify:playlist:playlist123"
        )
        
        assert track.web_url == "https://open.spotify.com/playlist/playlist123"
    
    def test_web_url_empty(self):
        """Test web_url with empty spotify_url."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=0,
            spotify_url=""
        )
        
        assert track.web_url is None
    
    def test_web_url_invalid_format(self):
        """Test web_url with invalid spotify_url format."""
        track = TrackInfo(
            name="Test",
            artist="Artist",
            album="Album",
            duration_ms=0,
            spotify_url="invalid:url"
        )
        
        assert track.web_url is None
    
    def test_track_info_with_fixture(self, sample_track):
        """Test using the sample_track fixture."""
        assert sample_track.name == "Test Song"
        assert sample_track.duration_seconds == 180.0
        assert sample_track.web_url == "https://open.spotify.com/track/abc123def456"
