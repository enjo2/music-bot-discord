import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import yt_dlp as youtube_dl
import asyncio
import nacl
from discord import FFmpegPCMAudio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX', '!')

# Bot setup
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# YouTube DL options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Bot is ready to play music!')

@bot.command(name='join', help='Join the voice channel')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send("You're not in a voice channel!")
        return
    
    channel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

@bot.command(name='leave', help='Leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='Play a song from YouTube')
async def play(ctx, *, url):
    async with ctx.typing():
        if not ctx.author.voice:
            await ctx.send("You're not in a voice channel!")
            return

        if not ctx.voice_client:
            await join(ctx)

        try:
            player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
            
            embed = discord.Embed(
                title="Now Playing",
                description=f"**{player.title}**",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='pause', help='Pause the current song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music paused ⏸️")
    else:
        await ctx.send("No music is currently playing.")

@bot.command(name='resume', help='Resume the current song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Music resumed ▶️")
    else:
        await ctx.send("Music is not paused.")

@bot.command(name='stop', help='Stop the current song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Music stopped ⏹️")
    else:
        await ctx.send("No music is currently playing.")

@bot.command(name='queue', help='Add a song to the queue')
async def queue(ctx, *, url):
    # This is a simplified version - you can extend this with a proper queue system
    await ctx.send("Queue feature coming soon! For now, use !play to play songs directly.")

@bot.command(name='skip', help='Skip the current song')
async def skip(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        await ctx.send("Song skipped ⏭️")
    else:
        await ctx.send("No music is currently playing.")

@bot.command(name='commands', help='Show all available commands')
async def help_command(ctx):
    embed = discord.Embed(
        title="Music Bot Commands",
        description="Here are all the available commands:",
        color=discord.Color.blue()
    )
    
    commands_list = [
        ("!join", "Join the voice channel"),
        ("!leave", "Leave the voice channel"),
        ("!play <url/search>", "Play a song from YouTube"),
        ("!pause", "Pause the current song"),
        ("!resume", "Resume the current song"),
        ("!stop", "Stop the current song"),
        ("!skip", "Skip the current song"),
        ("!commands", "Show this help message")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    await ctx.send(embed=embed)

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found! Use !commands to see available commands.")
    else:
        print(f"Error: {error}")

# Run the bot
if __name__ == "__main__":
    if TOKEN == "your_discord_bot_token_here":
        print("Please set your Discord bot token in the .env file!")
    else:
        bot.run(TOKEN)
