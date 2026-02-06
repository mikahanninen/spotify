"""Abstract base class for platform-specific Spotify controllers."""

import time
from abc import ABC, abstractmethod
from typing import Optional

from .models import TrackInfo


class SpotifyControllerBase(ABC):
    """
    Abstract base class for platform-specific Spotify controllers.
    
    All platform implementations must inherit from this class and implement
    the abstract methods.
    """
    
    # Default delays for UI operations (in seconds)
    DEFAULT_LAUNCH_DELAY = 2.0
    DEFAULT_UI_DELAY = 0.5
    DEFAULT_SEARCH_DELAY = 1.5
    DEFAULT_KEYSTROKE_DELAY = 0.1
    
    def __init__(self, debug: bool = False):
        """
        Initialize the controller.
        
        Args:
            debug: If True, print debug information during execution.
        """
        self.debug = debug
        self._ui_delay = self.DEFAULT_UI_DELAY
    
    # =========================================================================
    # Abstract Methods - Must be implemented by platform-specific classes
    # =========================================================================
    
    @abstractmethod
    def launch(self, wait: bool = True, delay: Optional[float] = None) -> None:
        """Launch the Spotify application."""
    
    @abstractmethod
    def quit(self) -> None:
        """Quit the Spotify application."""
    
    @abstractmethod
    def is_running(self) -> bool:
        """Check if Spotify is currently running."""
    
    @abstractmethod
    def bring_to_front(self) -> None:
        """Bring the Spotify window to the front."""
    
    @abstractmethod
    def play(self) -> None:
        """Start or resume playback."""
    
    @abstractmethod
    def pause(self) -> None:
        """Pause playback."""
    
    @abstractmethod
    def play_pause(self) -> None:
        """Toggle between play and pause."""
    
    @abstractmethod
    def next_track(self) -> None:
        """Skip to the next track."""
    
    @abstractmethod
    def previous_track(self) -> None:
        """Go back to the previous track."""
    
    @abstractmethod
    def set_volume(self, level: int) -> None:
        """Set the Spotify volume (0-100)."""
    
    @abstractmethod
    def get_volume(self) -> int:
        """Get the current Spotify volume."""
    
    @abstractmethod
    def get_player_state(self) -> str:
        """Get the current player state (playing, paused, stopped)."""
    
    @abstractmethod
    def get_player_position(self) -> float:
        """Get the current playback position in seconds."""
    
    @abstractmethod
    def set_player_position(self, position: float) -> None:
        """Set the playback position."""
    
    @abstractmethod
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get information about the currently playing track."""
    
    @abstractmethod
    def play_track(self, spotify_uri: str) -> None:
        """Play a specific track by its Spotify URI."""
    
    @abstractmethod
    def is_shuffling(self) -> bool:
        """Check if shuffle is enabled."""
    
    @abstractmethod
    def is_repeating(self) -> bool:
        """Check if repeat is enabled."""
    
    @abstractmethod
    def set_shuffling(self, enabled: bool) -> None:
        """Set shuffle mode."""
    
    @abstractmethod
    def set_repeating(self, enabled: bool) -> None:
        """Set repeat mode."""
    
    # =========================================================================
    # Abstract UI Automation Methods
    # =========================================================================
    
    @abstractmethod
    def _keystroke(self, key: str, modifiers: Optional[list] = None) -> None:
        """Send a keystroke to Spotify."""
    
    @abstractmethod
    def _key_code(self, code: int, modifiers: Optional[list] = None) -> None:
        """Send a key code to Spotify."""
    
    @abstractmethod
    def _type_text(self, text: str, delay_per_char: float = 0.02) -> None:
        """Type text into Spotify."""
    
    @abstractmethod
    def _get_return_key_code(self) -> int:
        """Get platform-specific key code for Return/Enter."""
    
    @abstractmethod
    def _get_escape_key_code(self) -> int:
        """Get platform-specific key code for Escape."""
    
    @abstractmethod
    def _get_tab_key_code(self) -> int:
        """Get platform-specific key code for Tab."""
    
    @abstractmethod
    def _get_down_arrow_key_code(self) -> int:
        """Get platform-specific key code for Down Arrow."""
    
    @abstractmethod
    def _get_up_arrow_key_code(self) -> int:
        """Get platform-specific key code for Up Arrow."""
    
    @abstractmethod
    def _get_space_key_code(self) -> int:
        """Get platform-specific key code for Space."""
    
    @abstractmethod
    def _get_command_modifier(self) -> str:
        """Get the platform-specific command modifier (Cmd on Mac, Ctrl on Windows)."""
    
    # =========================================================================
    # Concrete Methods - Shared across platforms
    # =========================================================================
    
    def is_playing(self) -> bool:
        """Check if Spotify is currently playing."""
        return self.get_player_state() == "playing"
    
    def wait(self, seconds: float) -> None:
        """Wait for a specified number of seconds."""
        time.sleep(seconds)
    
    def set_ui_delay(self, delay: float) -> None:
        """Set the default delay for UI operations."""
        self._ui_delay = delay
    
    def _press_return(self) -> None:
        """Press the Return/Enter key."""
        self._key_code(self._get_return_key_code())
    
    def _press_escape(self) -> None:
        """Press the Escape key."""
        self._key_code(self._get_escape_key_code())
    
    def _press_tab(self) -> None:
        """Press the Tab key."""
        self._key_code(self._get_tab_key_code())
    
    def _press_down_arrow(self) -> None:
        """Press the Down Arrow key."""
        self._key_code(self._get_down_arrow_key_code())
    
    def _press_up_arrow(self) -> None:
        """Press the Up Arrow key."""
        self._key_code(self._get_up_arrow_key_code())
    
    def _press_space(self) -> None:
        """Press the Space key."""
        self._key_code(self._get_space_key_code())
    
    # =========================================================================
    # High-Level Methods - Shared across platforms
    # =========================================================================
    
    def open_search(self) -> None:
        """Open the quick search overlay."""
        self.bring_to_front()
        self._keystroke("k", [self._get_command_modifier()])
        time.sleep(self._ui_delay)
    
    def search(self, query: str, wait_for_results: bool = True) -> None:
        """
        Open search and type a query.
        
        Args:
            query: The search query.
            wait_for_results: If True, wait for results to load.
        """
        self.open_search()
        time.sleep(0.3)
        self._type_text(query)
        
        if wait_for_results:
            time.sleep(self.DEFAULT_SEARCH_DELAY)
    
    def play_playlist_by_name(
        self,
        playlist_name: str,
        search_delay: float = 2.0
    ) -> None:
        """
        Find a playlist by name and play it.

        This is the main RPA task: open Spotify, search for a playlist,
        and start playing the first song.

        Args:
            playlist_name: The search query (use "playlist:name" for playlists only).
            search_delay: Time to wait for search results to load.
        """
        if not self.is_running():
            self.launch()
        else:
            self.bring_to_front()

        # Search for the playlist
        self.search(playlist_name, wait_for_results=False)
        time.sleep(search_delay)

        # Play the selected result (Shift+Enter) and show it (Enter)
        if hasattr(self, 'play_selected_search_result'):
            self.play_selected_search_result()
        else:
            # Fallback: just open the result
            self._press_return()
