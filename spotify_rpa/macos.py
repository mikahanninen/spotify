"""macOS-specific Spotify controller using AppleScript and System Events."""

import subprocess
import time
from typing import Optional

from .base import SpotifyControllerBase
from .models import TrackInfo
from .exceptions import AppleScriptError


class MacOSSpotifyController(SpotifyControllerBase):
    """
    macOS-specific Spotify controller using AppleScript and System Events.
    
    This implementation uses:
    - Native Spotify AppleScript commands for playback control
    - System Events for UI automation (keyboard input, navigation)
    """
    
    def _run_applescript(self, script: str) -> str:
        """Execute an AppleScript and return the output."""
        if self.debug:
            print(f"[AppleScript] {script[:100]}...")
        
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise AppleScriptError(f"AppleScript failed: {result.stderr}")
        
        return result.stdout.strip()
    
    # =========================================================================
    # Key Codes (macOS-specific)
    # =========================================================================
    
    def _get_return_key_code(self) -> int:
        return 36
    
    def _get_escape_key_code(self) -> int:
        return 53
    
    def _get_tab_key_code(self) -> int:
        return 48
    
    def _get_down_arrow_key_code(self) -> int:
        return 125
    
    def _get_up_arrow_key_code(self) -> int:
        return 126
    
    def _get_space_key_code(self) -> int:
        return 49
    
    def _get_command_modifier(self) -> str:
        return "command"
    
    # =========================================================================
    # Application Control
    # =========================================================================
    
    def launch(self, wait: bool = True, delay: Optional[float] = None) -> None:
        """Launch the Spotify application."""
        self._run_applescript('tell application "Spotify" to activate')
        if wait:
            time.sleep(delay or self.DEFAULT_LAUNCH_DELAY)
    
    def quit(self) -> None:
        """Quit the Spotify application."""
        self._run_applescript('tell application "Spotify" to quit')
    
    def is_running(self) -> bool:
        """Check if Spotify is currently running."""
        script = '''
        tell application "System Events"
            return (name of processes) contains "Spotify"
        end tell
        '''
        result = self._run_applescript(script)
        return result.lower() == "true"
    
    def bring_to_front(self) -> None:
        """Bring the Spotify window to the front."""
        self._run_applescript('tell application "Spotify" to activate')
        time.sleep(self._ui_delay)
    
    # =========================================================================
    # Playback Controls
    # =========================================================================
    
    def play(self) -> None:
        """Start or resume playback."""
        self._run_applescript('tell application "Spotify" to play')
    
    def pause(self) -> None:
        """Pause playback."""
        self._run_applescript('tell application "Spotify" to pause')
    
    def play_pause(self) -> None:
        """Toggle between play and pause."""
        self._run_applescript('tell application "Spotify" to playpause')
    
    def next_track(self) -> None:
        """Skip to the next track."""
        self._run_applescript('tell application "Spotify" to next track')
    
    def previous_track(self) -> None:
        """Go back to the previous track."""
        self._run_applescript('tell application "Spotify" to previous track')
    
    def set_volume(self, level: int) -> None:
        """Set the Spotify volume (0-100)."""
        if not 0 <= level <= 100:
            raise ValueError("Volume must be between 0 and 100")
        self._run_applescript(f'tell application "Spotify" to set sound volume to {level}')
    
    def get_volume(self) -> int:
        """Get the current Spotify volume."""
        result = self._run_applescript('tell application "Spotify" to sound volume')
        return int(result)
    
    # =========================================================================
    # Playback State
    # =========================================================================
    
    def get_player_state(self) -> str:
        """Get the current player state (playing, paused, stopped)."""
        result = self._run_applescript('tell application "Spotify" to player state as string')
        return result.lower()
    
    def get_player_position(self) -> float:
        """Get the current playback position in seconds."""
        result = self._run_applescript('tell application "Spotify" to player position')
        return float(result)
    
    def set_player_position(self, position: float) -> None:
        """Set the playback position."""
        self._run_applescript(f'tell application "Spotify" to set player position to {position}')
    
    # =========================================================================
    # Track Information
    # =========================================================================
    
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get information about the currently playing track."""
        script = '''
        tell application "Spotify"
            if player state is stopped then
                return "STOPPED"
            end if
            set trackName to name of current track
            set trackArtist to artist of current track
            set trackAlbum to album of current track
            set trackDuration to duration of current track
            set trackURL to spotify url of current track
            return trackName & "|||" & trackArtist & "|||" & trackAlbum & "|||" & trackDuration & "|||" & trackURL
        end tell
        '''
        result = self._run_applescript(script)
        
        if result == "STOPPED":
            return None
        
        parts = result.split("|||")
        if len(parts) != 5:
            return None
        
        return TrackInfo(
            name=parts[0],
            artist=parts[1],
            album=parts[2],
            duration_ms=int(parts[3]),
            spotify_url=parts[4]
        )
    
    def get_track_name(self) -> str:
        """Get the name of the current track."""
        return self._run_applescript('tell application "Spotify" to name of current track')
    
    def get_track_artist(self) -> str:
        """Get the artist of the current track."""
        return self._run_applescript('tell application "Spotify" to artist of current track')
    
    def get_track_album(self) -> str:
        """Get the album of the current track."""
        return self._run_applescript('tell application "Spotify" to album of current track')
    
    # =========================================================================
    # Play by URI
    # =========================================================================
    
    def play_track(self, spotify_uri: str) -> None:
        """Play a specific track or playlist by its Spotify URI."""
        self._run_applescript(f'tell application "Spotify" to play track "{spotify_uri}"')
    
    # =========================================================================
    # Shuffle and Repeat
    # =========================================================================
    
    def is_shuffling(self) -> bool:
        """Check if shuffle is enabled."""
        result = self._run_applescript('tell application "Spotify" to shuffling')
        return result.lower() == "true"
    
    def is_repeating(self) -> bool:
        """Check if repeat is enabled."""
        result = self._run_applescript('tell application "Spotify" to repeating')
        return result.lower() == "true"
    
    def set_shuffling(self, enabled: bool) -> None:
        """Set shuffle mode."""
        value = "true" if enabled else "false"
        self._run_applescript(f'tell application "Spotify" to set shuffling to {value}')
    
    def set_repeating(self, enabled: bool) -> None:
        """Set repeat mode."""
        value = "true" if enabled else "false"
        self._run_applescript(f'tell application "Spotify" to set repeating to {value}')
    
    # =========================================================================
    # UI Automation
    # =========================================================================
    
    def _keystroke(self, key: str, modifiers: Optional[list] = None) -> None:
        """Send a keystroke to Spotify."""
        using_clause = ""
        if modifiers:
            modifier_str = ", ".join(f"{m} down" for m in modifiers)
            using_clause = f" using {{{modifier_str}}}"
        script = f'''
        tell application "System Events"
            tell process "Spotify"
                keystroke "{key}"{using_clause}
            end tell
        end tell
        '''
        self._run_applescript(script)
        time.sleep(self.DEFAULT_KEYSTROKE_DELAY)

    def _key_code(self, code: int, modifiers: Optional[list] = None) -> None:
        """Send a key code to Spotify."""
        using_clause = ""
        if modifiers:
            modifier_str = ", ".join(f"{m} down" for m in modifiers)
            using_clause = f" using {{{modifier_str}}}"
        script = f'''
        tell application "System Events"
            tell process "Spotify"
                key code {code}{using_clause}
            end tell
        end tell
        '''
        self._run_applescript(script)
        time.sleep(self.DEFAULT_KEYSTROKE_DELAY)
    
    def _type_text(self, text: str, delay_per_char: float = 0.02) -> None:
        """Type text into Spotify."""
        escaped = text.replace('\\', '\\\\').replace('"', '\\"')
        script = f'''
        tell application "System Events"
            tell process "Spotify"
                keystroke "{escaped}"
            end tell
        end tell
        '''
        self._run_applescript(script)
        time.sleep(len(text) * delay_per_char + self._ui_delay)
    
    # =========================================================================
    # Utility
    # =========================================================================
    
    def get_spotify_uri_from_clipboard(self) -> str:
        """Get a Spotify URI from the clipboard."""
        return self._run_applescript('the clipboard as text')
