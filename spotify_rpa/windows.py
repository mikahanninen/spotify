"""Windows-specific Spotify controller using rpaframework-windows."""

import re
import time
from typing import Optional

from .base import SpotifyControllerBase
from .models import TrackInfo
from .exceptions import AutomationError

# Conditional import for Windows only
try:
    from RPA.Windows import Windows
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False


class WindowsSpotifyController(SpotifyControllerBase):
    """
    Windows Spotify controller using rpaframework-windows.
    
    This implementation uses:
    - RPA.Windows for window control and UI automation
    - Media keys for playback control
    - Window title parsing for track information
    
    Note: Some features available on macOS (volume, position, shuffle/repeat state)
    are not available on Windows due to lack of native API access.
    """
    
    def __init__(self, debug: bool = False):
        super().__init__(debug)
        if not WINDOWS_AVAILABLE:
            raise AutomationError(
                "rpaframework-windows is not installed. "
                "Install with: pip install rpaframework-windows"
            )
        self._windows = Windows()
    
    # =========================================================================
    # Application Control
    # =========================================================================
    
    def launch(self, wait: bool = True, delay: Optional[float] = None) -> None:
        """Launch Spotify using Windows Run."""
        self._windows.windows_run("spotify")
        if wait:
            time.sleep(delay or self.DEFAULT_LAUNCH_DELAY)
    
    def is_running(self) -> bool:
        """Check if Spotify window exists."""
        try:
            self._windows.control_window("executable:Spotify.exe", timeout=1)
            return True
        except Exception:
            return False
    
    def bring_to_front(self) -> None:
        """Focus Spotify window."""
        self._windows.control_window("executable:Spotify.exe")
        time.sleep(self._ui_delay)
    
    def quit(self) -> None:
        """Close Spotify window."""
        self.bring_to_front()
        self._windows.close_current_window()
    
    # =========================================================================
    # Playback Controls (via Media Keys)
    # =========================================================================
    
    def play(self) -> None:
        """Start playback using media key."""
        if not self.is_playing():
            self._windows.send_keys("{MEDIA_PLAY_PAUSE}")
    
    def pause(self) -> None:
        """Pause playback using media key."""
        if self.is_playing():
            self._windows.send_keys("{MEDIA_PLAY_PAUSE}")
    
    def play_pause(self) -> None:
        """Toggle play/pause."""
        self._windows.send_keys("{MEDIA_PLAY_PAUSE}")
    
    def next_track(self) -> None:
        """Skip to next track."""
        self._windows.send_keys("{MEDIA_NEXT_TRACK}")
    
    def previous_track(self) -> None:
        """Go to previous track."""
        self._windows.send_keys("{MEDIA_PREV_TRACK}")
    
    # =========================================================================
    # Track Information (from window title)
    # =========================================================================
    
    def _get_window_title(self) -> Optional[str]:
        """Get Spotify window title."""
        try:
            element = self._windows.get_element("executable:Spotify.exe")
            return element.name
        except Exception:
            return None
    
    def get_player_state(self) -> str:
        """Determine player state from window title."""
        title = self._get_window_title()
        if not title:
            return "stopped"
        # When playing: "Artist - Song - Spotify"
        # When paused/idle: "Spotify" or "Spotify Premium"
        if title in ("Spotify", "Spotify Premium", "Spotify Free"):
            return "paused"
        return "playing"
    
    def get_current_track(self) -> Optional[TrackInfo]:
        """Parse track info from window title."""
        title = self._get_window_title()
        if not title or title in ("Spotify", "Spotify Premium", "Spotify Free"):
            return None
        
        # Title format: "Artist - Song - Spotify"
        match = re.match(r"(.+?) - (.+?) - Spotify", title)
        if match:
            return TrackInfo(
                name=match.group(2),
                artist=match.group(1),
                album="",  # Not available from title
                duration_ms=0,
                spotify_url=""
            )
        return None
    
    # =========================================================================
    # UI Automation
    # =========================================================================
    
    def _keystroke(self, key: str, modifiers: Optional[list] = None) -> None:
        """Send keystroke to Spotify."""
        self.bring_to_front()
        if modifiers and "control" in modifiers:
            self._windows.send_keys(f"{{Ctrl}}{key}")
        else:
            self._windows.send_keys(key)
        time.sleep(self.DEFAULT_KEYSTROKE_DELAY)
    
    def _key_code(self, code: int, modifiers: Optional[list] = None) -> None:
        """Send key code - maps to send_keys for common keys."""
        key_map = {
            0x0D: "{ENTER}",
            0x1B: "{ESC}",
            0x09: "{TAB}",
            0x28: "{DOWN}",
            0x26: "{UP}",
            0x20: "{SPACE}",
        }
        key = key_map.get(code, "")
        if key:
            self.bring_to_front()
            self._windows.send_keys(key)
            time.sleep(self.DEFAULT_KEYSTROKE_DELAY)
    
    def _type_text(self, text: str, delay_per_char: float = 0.02) -> None:
        """Type text into Spotify."""
        self.bring_to_front()
        self._windows.send_keys(text)
        time.sleep(len(text) * delay_per_char + self._ui_delay)
    
    # =========================================================================
    # Key codes (Windows VK codes)
    # =========================================================================
    
    def _get_return_key_code(self) -> int:
        return 0x0D  # VK_RETURN
    
    def _get_escape_key_code(self) -> int:
        return 0x1B  # VK_ESCAPE
    
    def _get_tab_key_code(self) -> int:
        return 0x09  # VK_TAB
    
    def _get_down_arrow_key_code(self) -> int:
        return 0x28  # VK_DOWN
    
    def _get_up_arrow_key_code(self) -> int:
        return 0x26  # VK_UP
    
    def _get_space_key_code(self) -> int:
        return 0x20  # VK_SPACE
    
    def _get_command_modifier(self) -> str:
        return "control"  # Windows uses Ctrl instead of Cmd
    
    # =========================================================================
    # Limited functionality (no API access on Windows)
    # =========================================================================
    
    def get_volume(self) -> int:
        """Get volume - not available on Windows."""
        raise NotImplementedError(
            "Volume reading is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def set_volume(self, level: int) -> None:
        """Set volume - not available on Windows."""
        raise NotImplementedError(
            "Volume control is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def get_player_position(self) -> float:
        """Get playback position - not available on Windows."""
        raise NotImplementedError(
            "Playback position is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def set_player_position(self, position: float) -> None:
        """Set playback position - not available on Windows."""
        raise NotImplementedError(
            "Seeking is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def play_track(self, spotify_uri: str) -> None:
        """Play track by URI - not available on Windows."""
        raise NotImplementedError(
            "Playing by URI is not available on Windows. "
            "Use play_playlist_by_name() with search instead."
        )
    
    def is_shuffling(self) -> bool:
        """Check shuffle state - not available on Windows."""
        raise NotImplementedError(
            "Shuffle state is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def is_repeating(self) -> bool:
        """Check repeat state - not available on Windows."""
        raise NotImplementedError(
            "Repeat state is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def set_shuffling(self, enabled: bool) -> None:
        """Set shuffle - not available on Windows."""
        raise NotImplementedError(
            "Shuffle control is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
    
    def set_repeating(self, enabled: bool) -> None:
        """Set repeat - not available on Windows."""
        raise NotImplementedError(
            "Repeat control is not available on Windows. "
            "Spotify on Windows does not expose this via an API."
        )
