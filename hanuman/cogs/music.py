from http.client import HTTPException
from discord.ext import commands
import discord
import youtube_dl 
from ..funcs.spotifyfuncs import * 
from ..funcs.ytscrape import get_song_link
import asyncio

class MusicPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot 
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        self.queue = []
        self.current_track = 0

    @commands.command(pass_context = True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send('I joined the voice channel **{}**'.format(channel.name))

    @commands.command(aliases=['dc', 'disconnect'])
    async def leave(self, ctx):
        channel = ctx.guild.voice_client.channel
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I have left **{}**'.format(channel.name))
        
    @commands.command()
    async def play(self, ctx, *args):
        voice = ctx.guild.voice_client
        print(voice)
        if voice == None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send('I joined the voice channel **{}**'.format(channel.name))
            voice = ctx.guild.voice_client
        else:
            pass
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        if len(args)==1 and 'https://www.youtube.com' in args[0]:
            url = args[0]
        elif len(args)==1 and 'https://open.spotify.com/track' in args[0]:
            url = get_spotify_track(args[0])
        elif len(args)==1 and 'https://open.spotify.com/playlist' in args[0]:
            links = get_playlist_tracks(args[0])
            for link in links:
                self.queue.append(link)
            url = links[0]
        else:
            url = get_song_link(' '.join(arg for arg in args))
            
        if not voice.is_playing():
            if voice.is_paused():
                voice.resume()
            else:
                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable='ffmpeg.exe')
                    self.queue.append(url)
                    if len(self.queue) < 2:
                        voice.play(source)        
                    else:
                        voice.play(source, after=self.skip(ctx=ctx))
        else:
            self.queue.append(url)
            await ctx.send('Added song to queue!')


    @commands.command()
    async def queue(self, ctx, *args):
        if len(args) != 0:
            if len(args)==1 and 'https://www.youtube.com' in args[0]:
                self.queue.append(args[0])
            elif len(args)==1 and 'https://open.spotify.com/track' in args[0]:
                url = get_spotify_track(args[0])
                self.queue.append(url)
            elif len(args)==1 and 'https://open.spotify.com/playlist' in args[0]:
                links = get_playlist_tracks(args[0])
                for link in links:
                    self.queue.append(link)
            else:
                link = get_song_link(''.join(arg for arg in args))
                self.queue.append(link)
                await ctx.send('song queued!')
        else:
            if len(self.queue)!=0:
                await ctx.send('```'+'\n'.join(song for song in self.queue)+'```')
            else:
                await ctx.send('The queue is empty')\
                    
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        voice.pause()
        await ctx.send('paused current track')

    @commands.command()
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        voice.resume()
        await ctx.send('paused current track')

    @commands.command()
    async def skip(self, ctx):
        voice = ctx.guild.voice_client
        voice.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        self.current_track += 1
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(self.queue[self.current_track], download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS, executable='ffmpeg.exe')
        print('skip play')
        voice.play(source)

    @commands.command()
    async def np(self, ctx):
        await ctx.send(f"{self.queue[self.current_track]} is playing")