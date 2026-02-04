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
        pass
    
    @abstractmethod
    def quit(self) -> None:
        """Quit the Spotify application."""
        pass
    
    @abstractmethod
    def is_running(self) -> bool:
        """Check if Spotify is currently running."""
        pass
    
    @abstractmethod
    def bring_to_front(self) -> None:
        """Bring the Spotify window to the front."""
        pass
    
    @abstractmethod
    def play(self) -> None:
        """Start or resume playback."""
        pass
    
    @abstractmethod
    def pause(self) -> None:
        """Pause playback."""
        pass
    
    @abstractmethod
    def play_pause(self) -> None:
        """Toggle between play and pause."""
        pass
    
    @abstractmethod
    def next_track(self) -> None:
        """Skip to the next track."""
        pass
    
    @abstractmethod
    def previous_track(self) -> None:
        """Go back to the previous track."""
        pass
    
    @abstractmethod
    def set_volume(self, level: int) -> None:
        """Set the Spotify volume (0-100)."""
        pass
    
    @abstractmethod
    def get_volume(self) -> int:
        """Get the current Spotify volume."""
        pass
    
    @abstractmethod
    def get_player_state(self) -> str:
        """Get the current player state (playing, paused, stopped)."""
        pass
    
    @abstractmethod
    def get_player_position(self) -> float:
        """Get the current playback position in seconds."""
        pass
    
    @abstractmethod
    def set_player_position(self, position: float) -> None:
        """Set the playback position."""
        pass
    
    @abstractmethod
    def get_current_track(self) -> Optional[TrackInfo]:
        """Get information about the currently playing track."""
        pass
    
    @abstractmethod
    def play_track(self, spotify_uri: str) -> None:
        """Play a specific track by its Spotify URI."""
        pass
    
    @abstractmethod
    def is_shuffling(self) -> bool:
        """Check if shuffle is enabled."""
        pass
    
    @abstractmethod
    def is_repeating(self) -> bool:
        """Check if repeat is enabled."""
        pass
    
    @abstractmethod
    def set_shuffling(self, enabled: bool) -> None:
        """Set shuffle mode."""
        pass
    
    @abstractmethod
    def set_repeating(self, enabled: bool) -> None:
        """Set repeat mode."""
        pass
    
    # =========================================================================
    # Abstract UI Automation Methods
    # =========================================================================
    
    @abstractmethod
    def _keystroke(self, key: str, modifiers: Optional[list] = None) -> None:
        """Send a keystroke to Spotify."""
        pass
    
    @abstractmethod
    def _key_code(self, code: int, modifiers: Optional[list] = None) -> None:
        """Send a key code to Spotify."""
        pass
    
    @abstractmethod
    def _type_text(self, text: str, delay_per_char: float = 0.02) -> None:
        """Type text into Spotify."""
        pass
    
    @abstractmethod
    def _get_return_key_code(self) -> int:
        """Get platform-specific key code for Return/Enter."""
        pass
    
    @abstractmethod
    def _get_escape_key_code(self) -> int:
        """Get platform-specific key code for Escape."""
        pass
    
    @abstractmethod
    def _get_tab_key_code(self) -> int:
        """Get platform-specific key code for Tab."""
        pass
    
    @abstractmethod
    def _get_down_arrow_key_code(self) -> int:
        """Get platform-specific key code for Down Arrow."""
        pass
    
    @abstractmethod
    def _get_up_arrow_key_code(self) -> int:
        """Get platform-specific key code for Up Arrow."""
        pass
    
    @abstractmethod
    def _get_space_key_code(self) -> int:
        """Get platform-specific key code for Space."""
        pass
    
    @abstractmethod
    def _get_command_modifier(self) -> str:
        """Get the platform-specific command modifier (Cmd on Mac, Ctrl on Windows)."""
        pass
    
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
    
    def select_first_search_result(self) -> None:
        """Select the first result from the search dropdown."""
        time.sleep(0.3)
        self._press_down_arrow()
        time.sleep(0.2)
        self._press_return()
        time.sleep(self._ui_delay)
    
    def navigate_to_first_song(self) -> None:
        """Navigate to and play the first song in the current view."""
        for _ in range(3):
            self._press_tab()
            time.sleep(0.1)
        self._press_return()
    
    def play_playlist_by_name(
        self,
        playlist_name: str,
        play_first_song: bool = True,
        search_delay: float = 2.0
    ) -> None:
        """
        Find a playlist by name and play it.
        
        This is the main method for the RPA task: finding a playlist by name
        and playing it using UI automation.
        
        Args:
            playlist_name: The name of the playlist to find and play.
            play_first_song: If True, explicitly start playing the first song.
            search_delay: Time to wait for search results.
        """
        if not self.is_running():
            self.launch()
        else:
            self.bring_to_front()
        
        self.search(playlist_name, wait_for_results=False)
        time.sleep(search_delay)
        
        self.select_first_search_result()
        time.sleep(1.0)
        
        if play_first_song:
            time.sleep(0.5)
            self._press_return()
    
    def search_and_play(self, query: str) -> None:
        """Search for something and immediately play the first result."""
        self.search(query)
        self.select_first_search_result()
        time.sleep(0.5)
        self.play()
    
    def toggle_shuffle(self) -> None:
        """Toggle shuffle mode."""
        self.bring_to_front()
        self._keystroke("s", [self._get_command_modifier()])
    
    def toggle_repeat(self) -> None:
        """Toggle repeat mode."""
        self.bring_to_front()
        self._keystroke("r", [self._get_command_modifier()])
