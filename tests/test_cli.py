"""Tests for spotify_rpa.cli module."""

import pytest
import sys
from unittest.mock import patch, MagicMock

from spotify_rpa.cli import (
    main,
    print_status,
    verify_playback,
    cmd_play_playlist,
    cmd_status,
    cmd_volume,
)
from spotify_rpa.models import TrackInfo


class TestMainCLI:
    """Tests for main CLI entry point."""
    
    def test_cli_no_command_shows_help(self, capsys):
        """Test running without command shows help."""
        with patch.object(sys, "argv", ["spotify"]):
            result = main()
        
        assert result == 0
        captured = capsys.readouterr()
        assert "Spotify RPA" in captured.out
    
    def test_cli_help_flag(self):
        """Test --help flag exits with 0."""
        with patch.object(sys, "argv", ["spotify", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    
    def test_cli_debug_flag_parsed(self):
        """Test --debug flag is parsed correctly."""
        with patch.object(sys, "argv", ["spotify", "--debug", "status"]):
            with patch("spotify_rpa.cli.SpotifyRPA") as mock_spotify:
                mock_instance = MagicMock()
                mock_instance.is_running.return_value = False
                mock_spotify.return_value = mock_instance
                
                main()
                
                mock_spotify.assert_called_once_with(debug=True)
    
    def test_cli_status_command(self):
        """Test status command."""
        with patch.object(sys, "argv", ["spotify", "status"]):
            with patch("spotify_rpa.cli.SpotifyRPA") as mock_spotify:
                mock_instance = MagicMock()
                mock_instance.is_running.return_value = False
                mock_spotify.return_value = mock_instance
                
                result = main()
                
                assert result == 0


class TestPrintStatus:
    """Tests for print_status helper function."""
    
    def test_print_status_playing(self, capsys):
        """Test print_status when playing."""
        mock_spotify = MagicMock()
        mock_spotify.get_player_state.return_value = "playing"
        mock_spotify.get_current_track.return_value = TrackInfo(
            name="Test Song",
            artist="Test Artist",
            album="Test Album",
            duration_ms=180000,
            spotify_url="spotify:track:abc123"
        )
        mock_spotify.get_player_position.return_value = 60.0
        
        print_status(mock_spotify)
        
        captured = capsys.readouterr()
        assert "playing" in captured.out
        assert "Test Song" in captured.out
        assert "Test Artist" in captured.out
    
    def test_print_status_stopped(self, capsys):
        """Test print_status when stopped."""
        mock_spotify = MagicMock()
        mock_spotify.get_player_state.return_value = "stopped"
        
        print_status(mock_spotify)
        
        captured = capsys.readouterr()
        assert "stopped" in captured.out


class TestVerifyPlayback:
    """Tests for verify_playback helper function."""
    
    def test_verify_playback_success(self):
        """Test verify_playback returns True when playing."""
        mock_spotify = MagicMock()
        mock_spotify.is_playing.return_value = True
        
        result = verify_playback(mock_spotify, timeout=1.0)
        
        assert result is True
    
    def test_verify_playback_timeout(self):
        """Test verify_playback returns False on timeout."""
        mock_spotify = MagicMock()
        mock_spotify.is_playing.return_value = False
        
        result = verify_playback(mock_spotify, timeout=0.5)
        
        assert result is False


class TestCommandFunctions:
    """Tests for individual command functions."""
    
    def test_cmd_status_not_running(self, capsys):
        """Test cmd_status when Spotify not running."""
        args = MagicMock()
        mock_spotify = MagicMock()
        mock_spotify.is_running.return_value = False
        
        result = cmd_status(args, mock_spotify)
        
        assert result == 0
        captured = capsys.readouterr()
        assert "not running" in captured.out
    
    def test_cmd_volume_get(self, capsys):
        """Test cmd_volume to get current volume."""
        args = MagicMock()
        args.level = None
        mock_spotify = MagicMock()
        mock_spotify.is_running.return_value = True
        mock_spotify.get_volume.return_value = 75
        
        result = cmd_volume(args, mock_spotify)
        
        assert result == 0
        captured = capsys.readouterr()
        assert "75" in captured.out
    
    def test_cmd_volume_set(self, capsys):
        """Test cmd_volume to set volume."""
        args = MagicMock()
        args.level = 50
        mock_spotify = MagicMock()
        mock_spotify.is_running.return_value = True
        
        result = cmd_volume(args, mock_spotify)
        
        assert result == 0
        mock_spotify.set_volume.assert_called_once_with(50)
