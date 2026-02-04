# Spotify RPA

A cross-platform Python RPA (Robotic Process Automation) solution for controlling the Spotify desktop application.

This project demonstrates UI automation techniques to interact with Spotify without using the Spotify Web API. The architecture supports multiple platforms with platform-specific implementations.

## Supported Platforms

| Platform | Status | Implementation |
|----------|--------|----------------|
| macOS    | Fully implemented | AppleScript + System Events |
| Windows  | Implemented (partial) | rpaframework-windows |
| Linux    | Not supported | - |

### Windows Limitations

Windows implementation has some limitations compared to macOS due to lack of native Spotify API:

| Feature | macOS | Windows |
|---------|-------|---------|
| Play/Pause/Next/Prev | Yes | Yes (media keys) |
| Search & Play Playlist | Yes | Yes |
| Track name/artist | Yes | Yes (from window title) |
| Album name | Yes | No |
| Duration/Position | Yes | No |
| Volume control | Yes | No |
| Shuffle/Repeat | Yes | No |

## Task

This solution implements the following RPA task:
- Open the Spotify desktop application
- Find the playlist "Göstän parhaat"
- Play the first song

## Requirements

### macOS
- **Python 3.7+**
- **Spotify desktop application** installed
- **Accessibility permissions** enabled for Terminal/IDE

### Windows
- **Python 3.9+** (required by rpaframework-windows)
- **Spotify desktop application** installed
- **rpaframework-windows** package (installed automatically via requirements.txt)

```bash
pip install -r requirements.txt
```

## macOS Setup

### Enabling Accessibility Permissions

The script uses System Events for UI automation, which requires accessibility permissions.

If you see this error:
```
Error: AppleScript failed: execution error: System Events got an error: osascript is not allowed to send keystrokes. (1002)
```

You need to grant accessibility permissions:

1. Open **System Settings** > **Privacy & Security** > **Accessibility**
   - (On older macOS: **System Preferences** > **Security & Privacy** > **Privacy** > **Accessibility**)
2. Click the lock icon and authenticate (if needed)
3. Click the **+** button and add your Terminal app:
   - **Terminal.app** (if using built-in Terminal)
   - **iTerm** (if using iTerm2)
   - **Cursor** or **Visual Studio Code** (if running from IDE terminal)
4. Ensure the checkbox next to the app is enabled
5. You may need to restart the terminal/IDE after granting permissions

## Installation

```bash
git clone https://github.com/yourusername/spotify-rpa.git
cd spotify-rpa
pip install -r requirements.txt
```

- **macOS**: No external dependencies (uses Python standard library only)
- **Windows**: Installs `rpaframework-windows` automatically

## Usage

### Run the Main Task

```bash
python spotify.py play-playlist "Göstän parhaat"
```

This will:
1. Launch Spotify (or bring it to front if already running)
2. Open the search overlay (Cmd+K on macOS, Ctrl+K on Windows)
3. Search for the playlist by name
4. Select the first search result
5. Play the first song
6. Verify playback and show current track info

### CLI Commands

```bash
# Play a playlist by name
python spotify.py play-playlist "My Playlist"

# Search for something
python spotify.py search "artist name"

# Playback controls
python spotify.py play
python spotify.py pause
python spotify.py next
python spotify.py prev

# Show current status
python spotify.py status

# Volume control
python spotify.py volume        # Show current volume
python spotify.py volume 50     # Set volume to 50%

# Enable debug output
python spotify.py --debug play-playlist "My Playlist"
```

### As a Python Library

```python
from spotify import SpotifyRPA

# Automatically detects platform and uses appropriate controller
spotify = SpotifyRPA()

# Launch Spotify
spotify.launch()

# Play a playlist by name (main task)
spotify.play_playlist_by_name("Göstän parhaat")

# Get current track info
track = spotify.get_current_track()
print(f"Now playing: {track.name} by {track.artist}")

# Playback controls
spotify.play()
spotify.pause()
spotify.next_track()
spotify.previous_track()

# Volume control
spotify.set_volume(75)
```

## Architecture

The code follows a platform-agnostic design with platform-specific implementations:

```
SpotifyRPA (Facade)
    │
    └── SpotifyControllerBase (Abstract Base Class)
            │
            ├── MacOSSpotifyController (AppleScript + System Events)
            │
            └── WindowsSpotifyController (rpaframework-windows)
```

### Key Components

- **`SpotifyControllerBase`**: Abstract base class defining the interface for all platforms
- **`MacOSSpotifyController`**: macOS implementation using AppleScript
- **`WindowsSpotifyController`**: Windows implementation using rpaframework-windows
- **`SpotifyRPA`**: Facade class that auto-detects platform and delegates to the appropriate controller
- **`create_spotify_controller()`**: Factory function for creating platform-specific controllers

## How It Works

### macOS Implementation

Uses two macOS automation technologies:

#### 1. Native Spotify AppleScript Commands

Spotify on macOS exposes a native AppleScript interface for basic playback control:

```applescript
tell application "Spotify"
    play
    pause
    next track
    set sound volume to 50
end tell
```

#### 2. System Events UI Automation

For operations not supported by Spotify's native interface (like searching), we use System Events to simulate keyboard input:

```applescript
tell application "System Events"
    tell process "Spotify"
        keystroke "k" using {command down}  -- Open search
        keystroke "playlist name"            -- Type search query
        key code 125                         -- Down arrow
        key code 36                          -- Enter
    end tell
end tell
```

### Windows Implementation

The Windows implementation uses **rpaframework-windows** for UI automation:

- **Window control**: `control_window("executable:Spotify.exe")` to find and focus Spotify
- **Media keys**: `send_keys("{MEDIA_PLAY_PAUSE}")` for playback control
- **Keyboard input**: `send_keys("{Ctrl}k")` for search, typing text
- **Track info**: Parsed from window title (format: "Artist - Song - Spotify")

### RPA Approach

This is a genuine RPA solution because it:
- Interacts with the UI like a human would (keyboard shortcuts, typing, navigation)
- Does not use the Spotify Web API or any backend services
- Works with the desktop application through UI automation
- Can be observed visually as it executes

## Limitations

- **Windows features**: Some features (volume, position, shuffle/repeat) not available on Windows
- **UI-dependent**: May break if Spotify significantly changes their UI
- **Timing-sensitive**: Uses delays to wait for UI responses
- **Accessibility required**: Needs permission to control the system (macOS)
- **Display scaling**: Windows users should use 100% display scaling for best results

## Project Structure

```
spotify-rpa/
├── spotify.py              # CLI entrypoint
├── spotify_rpa/            # Main package
│   ├── __init__.py         # Package exports
│   ├── models.py           # Data models (TrackInfo)
│   ├── exceptions.py       # Custom exceptions
│   ├── base.py             # Abstract base controller
│   ├── macos.py            # macOS implementation
│   ├── windows.py          # Windows implementation (rpaframework-windows)
│   ├── controller.py       # Factory and SpotifyRPA facade
│   └── cli.py              # CLI commands
├── README.md               # This file
└── requirements.txt        # Dependencies (rpaframework-windows for Windows)
```

## Why Python?

Python was chosen because:
1. It's the preferred language specified in the task
2. Clean syntax for readable automation scripts
3. Excellent subprocess support for running AppleScript
4. Strong typing support with dataclasses and type hints
5. Cross-platform standard library
6. No external dependencies needed for macOS implementation

## License

MIT License
