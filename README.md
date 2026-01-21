# Discord Music Bot

A feature-rich Discord music bot that plays music from YouTube with basic playback controls.

## Features

- 🎵 Play music from YouTube URLs or search terms
- 🎤 Join and leave voice channels
- ⏸️ Pause, resume, and stop playback
- ⏭️ Skip current song
- 📋 Command help system
- 🎨 Beautiful embed messages

## Setup

### Prerequisites

1. Python 3.8 or higher
2. FFmpeg installed on your system
3. Discord Bot Token
4. YouTube API Key (optional but recommended)

### Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install FFmpeg:
   - **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html) and add to PATH
   - **MacOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg` or `sudo yum install ffmpeg`

4. Create a Discord Bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to "Bot" tab and create a bot
   - Enable "Message Content Intent" and "Voice State Intent"
   - Copy the bot token

5. Configure the bot:
   - Rename `.env` file and update with your credentials:
     ```
     DISCORD_TOKEN=your_actual_discord_bot_token
     PREFIX=!
     YOUTUBE_API_KEY=your_youtube_api_key
     ```

6. Invite the bot to your server:
   - In Discord Developer Portal, go to "OAuth2" → "URL Generator"
   - Select scopes: `bot` and `applications.commands`
   - Select permissions: Connect, Speak, Read Message History, Send Messages
   - Copy the generated URL and invite the bot

## Commands

| Command | Description |
|---------|-------------|
| `!join` | Join the voice channel you're in |
| `!leave` | Leave the voice channel |
| `!play <url/search>` | Play a song from YouTube URL or search term |
| `!pause` | Pause the current song |
| `!resume` | Resume the paused song |
| `!stop` | Stop the current song |
| `!skip` | Skip the current song |
| `!help` | Show all available commands |

## Usage Examples

```
!play https://www.youtube.com/watch?v=dQw4w9WgXcQ
!play never gonna give you up
!pause
!resume
!skip
!leave
```

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**
   - Make sure FFmpeg is installed and added to your system PATH

2. **Bot doesn't respond to commands**
   - Check that the bot has proper permissions
   - Verify the Discord token is correct in `.env`

3. **"You're not in a voice channel" error**
   - Make sure you're in a voice channel before using music commands

4. **YouTube playback issues**
   - Some videos may be restricted or unavailable
   - Consider adding a YouTube API key for better reliability

## Future Enhancements

- [ ] Song queue system
- [ ] Volume control
- [ ] Lyrics display
- [ ] Playlist support
- [ ] Radio stations
- [ ] Music statistics

## License

This project is open source and available under the MIT License.
