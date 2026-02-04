"""Tests for spotify_rpa.controller module."""

import pytest
from unittest.mock import patch, MagicMock

from spotify_rpa.controller import get_platform, create_spotify_controller, SpotifyRPA
from spotify_rpa.exceptions import PlatformNotSupportedError


class TestGetPlatform:
    """Tests for get_platform function."""
    
    def test_get_platform_macos(self):
        """Test platform detection for macOS."""
        with patch("spotify_rpa.controller.platform.system", return_value="Darwin"):
            assert get_platform() == "macos"
    
    def test_get_platform_windows(self):
        """Test platform detection for Windows."""
        with patch("spotify_rpa.controller.platform.system", return_value="Windows"):
            assert get_platform() == "windows"
    
    def test_get_platform_linux(self):
        """Test platform detection for Linux."""
        with patch("spotify_rpa.controller.platform.system", return_value="Linux"):
            assert get_platform() == "linux"
    
    def test_get_platform_unknown(self):
        """Test platform detection for unknown OS."""
        with patch("spotify_rpa.controller.platform.system", return_value="UnknownOS"):
            assert get_platform() == "unknownos"


class TestCreateSpotifyController:
    """Tests for create_spotify_controller factory function."""
    
    def test_create_macos_controller(self):
        """Test creating macOS controller."""
        with patch("spotify_rpa.controller.platform.system", return_value="Darwin"):
            # Mock the MacOSSpotifyController import
            with patch.dict("sys.modules", {"spotify_rpa.macos": MagicMock()}):
                from spotify_rpa.macos import MacOSSpotifyController
                controller = create_spotify_controller("macos", debug=False)
                assert controller is not None
    
    def test_create_unsupported_platform(self):
        """Test creating controller for unsupported platform raises error."""
        with pytest.raises(PlatformNotSupportedError) as exc_info:
            create_spotify_controller("linux", debug=False)
        
        assert "linux" in str(exc_info.value).lower()
        assert "not supported" in str(exc_info.value).lower()
    
    def test_create_controller_with_debug(self):
        """Test creating controller with debug flag."""
        with patch("spotify_rpa.controller.platform.system", return_value="Darwin"):
            controller = create_spotify_controller("macos", debug=True)
            assert controller.debug is True


class TestSpotifyRPA:
    """Tests for SpotifyRPA facade class."""
    
    def test_spotify_rpa_init_detects_platform(self):
        """Test SpotifyRPA detects platform on init."""
        with patch("spotify_rpa.controller.get_platform", return_value="macos"):
            with patch("spotify_rpa.controller.create_spotify_controller") as mock_create:
                mock_controller = MagicMock()
                mock_create.return_value = mock_controller
                
                spotify = SpotifyRPA(debug=False)
                
                assert spotify.platform == "macos"
                mock_create.assert_called_once_with("macos", debug=False)
    
    def test_spotify_rpa_delegates_to_controller(self):
        """Test SpotifyRPA delegates method calls to controller."""
        with patch("spotify_rpa.controller.get_platform", return_value="macos"):
            with patch("spotify_rpa.controller.create_spotify_controller") as mock_create:
                mock_controller = MagicMock()
                mock_controller.play.return_value = None
                mock_create.return_value = mock_controller
                
                spotify = SpotifyRPA()
                spotify.play()
                
                mock_controller.play.assert_called_once()
    
    def test_spotify_rpa_debug_flag(self):
        """Test SpotifyRPA passes debug flag correctly."""
        with patch("spotify_rpa.controller.get_platform", return_value="macos"):
            with patch("spotify_rpa.controller.create_spotify_controller") as mock_create:
                mock_create.return_value = MagicMock()
                
                spotify = SpotifyRPA(debug=True)
                
                assert spotify.debug is True
                mock_create.assert_called_once_with("macos", debug=True)
