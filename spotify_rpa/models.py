"""Data models for Spotify RPA."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TrackInfo:
    """Information about a Spotify track."""
    name: str
    artist: str
    album: str
    duration_ms: int
    spotify_url: str  # URI format: spotify:track:id

    @property
    def duration_seconds(self) -> float:
        """Get duration in seconds."""
        return self.duration_ms / 1000

    @property
    def web_url(self) -> Optional[str]:
        """
        Get shareable web URL for the track.
        
        Converts spotify:track:id to https://open.spotify.com/track/id
        """
        if not self.spotify_url:
            return None
        
        # Parse URI format: spotify:type:id
        parts = self.spotify_url.split(":")
        if len(parts) == 3 and parts[0] == "spotify":
            item_type = parts[1]  # track, album, playlist, etc.
            item_id = parts[2]
            return f"https://open.spotify.com/{item_type}/{item_id}"
        
        return None
