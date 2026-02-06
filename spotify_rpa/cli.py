"""Command-line interface for Spotify RPA."""

import argparse
import sys
import time

from .controller import SpotifyRPA, get_platform
from .exceptions import AutomationError, PlatformNotSupportedError


def print_status(spotify: SpotifyRPA) -> None:
    """Print current playback status and track info."""
    state = spotify.get_player_state()
    print(f"Status: {state}")
    
    if state != "stopped":
        track = spotify.get_current_track()
        if track:
            print(f"Track:  {track.name}")
            print(f"Artist: {track.artist}")
            print(f"Album:  {track.album}")
            position = spotify.get_player_position()
            duration = track.duration_seconds
            print(f"Time:   {position:.0f}s / {duration:.0f}s")
            print(f"URL:    {track.web_url}")


def verify_playback(spotify: SpotifyRPA, timeout: float = 3.0) -> bool:
    """
    Verify that playback has started.

    Args:
        spotify: SpotifyRPA instance.
        timeout: Maximum time to wait for playback to start.

    Returns:
        True if playing, False otherwise.
    """
    start = time.time()
    while time.time() - start < timeout:
        if spotify.is_playing():
            return True
        time.sleep(0.3)
    return False


def require_running(spotify: SpotifyRPA) -> bool:
    """Check if Spotify is running, print error if not. Returns True if running."""
    if not spotify.is_running():
        print("Error: Spotify is not running.")
        return False
    return True


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_play_playlist(args, spotify: SpotifyRPA) -> int:
    """Execute the play-playlist command."""
    playlist_name = args.name
    
    print("Launching Spotify...")
    if not spotify.is_running():
        spotify.launch()
    else:
        spotify.bring_to_front()
    print("Spotify is ready.")
    
    print(f"Searching for playlist: {playlist_name}")
    spotify.play_playlist_by_name(playlist_name)
    
    print("Waiting for playback to start...")
    time.sleep(2.0)
    
    if verify_playback(spotify):
        print("Playback started successfully!")
        print()
        print_status(spotify)
        return 0
    else:
        print("Warning: Could not verify playback started.")
        print("The playlist may still be loading. Check Spotify manually.")
        return 1


def cmd_search(args, spotify: SpotifyRPA) -> int:
    """Execute the search command."""
    query = args.query
    
    if not spotify.is_running():
        print("Launching Spotify...")
        spotify.launch()
    else:
        spotify.bring_to_front()
    
    print(f"Searching for: {query}")
    spotify.search(query)
    print("Search results should now be visible in Spotify.")
    return 0


def cmd_play(args, spotify: SpotifyRPA) -> int:
    """Execute the play command."""
    if not require_running(spotify):
        return 1
    spotify.play()
    print("Playback started.")
    time.sleep(0.5)
    print_status(spotify)
    return 0


def cmd_pause(args, spotify: SpotifyRPA) -> int:
    """Execute the pause command."""
    if not require_running(spotify):
        return 1
    spotify.pause()
    print("Playback paused.")
    return 0


def cmd_next(args, spotify: SpotifyRPA) -> int:
    """Execute the next track command."""
    if not require_running(spotify):
        return 1
    spotify.next_track()
    print("Skipped to next track.")
    time.sleep(0.5)
    print_status(spotify)
    return 0


def cmd_prev(args, spotify: SpotifyRPA) -> int:
    """Execute the previous track command."""
    if not require_running(spotify):
        return 1
    spotify.previous_track()
    print("Went to previous track.")
    time.sleep(0.5)
    print_status(spotify)
    return 0


def cmd_status(args, spotify: SpotifyRPA) -> int:
    """Execute the status command."""
    if not spotify.is_running():
        print("Spotify is not running.")
        return 0
    
    print_status(spotify)
    return 0


def cmd_volume(args, spotify: SpotifyRPA) -> int:
    """Execute the volume command."""
    if not require_running(spotify):
        return 1
    if args.level is None:
        print(f"Current volume: {spotify.get_volume()}")
    else:
        spotify.set_volume(args.level)
        print(f"Volume set to: {args.level}")
    return 0


# =============================================================================
# Main Entry Point
# =============================================================================

def main() -> int:
    """Main entry point for the CLI."""
    # Global arguments (must appear before the subcommand)
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug output"
    )
    
    parser = argparse.ArgumentParser(
        prog="spotify",
        description="Spotify RPA - Control Spotify desktop app using UI automation.",
        epilog="Example: python spotify.py play-playlist \"Göstän parhaat\"",
        parents=[parent_parser]
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # play-playlist command
    p_playlist = subparsers.add_parser(
        "play-playlist",
        help="Find and play a playlist by name"
    )
    p_playlist.add_argument("name", help="Name of the playlist to play")
    p_playlist.set_defaults(func=cmd_play_playlist)
    
    # search command
    p_search = subparsers.add_parser(
        "search",
        help="Search for songs, artists, or playlists"
    )
    p_search.add_argument("query", help="Search query")
    p_search.set_defaults(func=cmd_search)
    
    # play command
    p_play = subparsers.add_parser("play", help="Start/resume playback")
    p_play.set_defaults(func=cmd_play)
    
    # pause command
    p_pause = subparsers.add_parser("pause", help="Pause playback")
    p_pause.set_defaults(func=cmd_pause)
    
    # next command
    p_next = subparsers.add_parser("next", help="Skip to next track")
    p_next.set_defaults(func=cmd_next)
    
    # prev command
    p_prev = subparsers.add_parser("prev", help="Go to previous track")
    p_prev.set_defaults(func=cmd_prev)
    
    # status command
    p_status = subparsers.add_parser("status", help="Show current playback status")
    p_status.set_defaults(func=cmd_status)
    
    # volume command
    p_volume = subparsers.add_parser("volume", help="Get or set volume (0-100)")
    p_volume.add_argument(
        "level",
        nargs="?",
        type=int,
        help="Volume level (0-100). Omit to show current volume."
    )
    p_volume.set_defaults(func=cmd_volume)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Detect platform and show info
    current_platform = get_platform()
    if args.debug:
        print(f"[Platform] Detected: {current_platform}")
    
    # Initialize SpotifyRPA
    try:
        spotify = SpotifyRPA(debug=args.debug)
    except PlatformNotSupportedError as e:
        print(f"Error: {e}")
        return 1
    
    # Execute the command
    try:
        return args.func(args, spotify)
    except (AutomationError, NotImplementedError) as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
