from discord.ext import commands
import discord
import youtube_dl 
from ..funcs.spotifyfuncs import * 
from ..funcs.ytscrape import get_song_link, get_song_details
import threading

class MusicPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot 
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.queue = []
        self.display_queue = []
        self.current_track = 0

    def threadqueue(self, args):
        print("Thread Started")
        names = get_playlist_names(args)
        for name in names:
            try:
                self.queue.append(get_song_link(name))
                self.display_queue.append(str(name.encode('utf-8')))
            except:
                pass

    async def play_song(self, ctx):
        voice = ctx.guild.voice_client
        self.current_track += 1
        try:
            url = self.queue[self.current_track]
            with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS, executable='ffmpeg.exe')
                voice.play(source, after=lambda e: self.segue(ctx))
        except IndexError:
            await ctx.send("Queue over!")

    def segue(self, ctx):
        self.bot.loop.create_task(self.play_song(ctx))
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(self.play_song(ctx))

    @commands.command(pass_context = True)
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        await channel.connect()
        await ctx.send('I joined the voice channel **{}**'.format(channel.name))

    @commands.command(aliases=['dc', 'disconnect'])
    async def leave(self, ctx):
        channel = ctx.guild.voice_client.channel
        self.queue = []
        self.display_queue = []
        await ctx.guild.voice_client.disconnect()
        await ctx.send('I have left **{}**'.format(channel.name))
        
    @commands.command(aliases=["p"])
    async def play(self, ctx, *args):
        voice = ctx.guild.voice_client
        print(voice)
        if voice == None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send('I joined the voice channel **{}**'.format(channel.name))
            voice = ctx.guild.voice_client

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        YDL_OPTIONS = {'format': 'bestaudio'}
        # YDL_OPTIONS = {'format': 'beataudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]}
        if len(args)==1 and 'https://www.youtube.com' in args[0]:
            url = args[0]
        elif len(args)==1 and 'https://open.spotify.com/track' in args[0]:
            url = get_spotify_track(args[0])
        elif len(args)==1 and 'https://open.spotify.com/playlist' in args[0]:
            threading.Thread(target=self.threadqueue, args=[args[0]]).start()
            url = spotify.playlist_tracks(args[0])
            url = url['items'][0]['track']['name'] + ' ' + url['items'][0]['track']['artists'][0]['name']
            url = get_song_link(url)
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
                    self.display_queue.append(get_song_details(url)[0])
                    voice.play(source, after=lambda e: self.segue(ctx))
        else:
            self.queue.append(url)
            self.display_queue.append(get_song_details(url)[0])
            await ctx.send('Added song to queue!')


    @commands.command(aliases=["q"])
    async def queue(self, ctx, *args):
        if len(args) != 0:
            if len(args)==1 and 'https://www.youtube.com' in args[0]:
                self.queue.append(args[0])
                self.display_queue.append(get_song_details(args[0])[0])
            elif len(args)==1 and 'https://open.spotify.com/track' in args[0]:
                url = get_spotify_track(args[0])
                self.queue.append(url)
                self.display_queue.append(get_song_details(url)[0])
            elif len(args)==1 and 'https://open.spotify.com/playlist' in args[0]:
                details = get_playlist_tracks(args[0])
                for link, name in zip(details["links"], details["names"]):
                    self.queue.append(link)
                    self.display_queue.append(name)
            else:
                link = get_song_link(''.join(arg for arg in args))
                self.queue.append(link)
                self.display_queue.append(get_song_details(link)[0])
                await ctx.send('song queued!')
        else:
            if len(self.queue)!=0:
                msg = '```'+'\n'.join(f"{num}. {song[2:-1]}" for song, num in zip(self.display_queue, range(1,len(self.display_queue)+1)))+'```'
                if len(msg.split('\n'))>20:
                    curr_q = msg.split('\n')[:20]
                    sent = await ctx.send('\n'.join(line for line in curr_q)+'```')
                    back = "⬅️"
                    forw = "➡️"
                    await sent.add_reaction(back)
                    await sent.add_reaction(forw)
                    looper = 20
                    msg = msg[3:-3]
                    while True:
                        try:
                            reaction, y = await self.bot.wait_for('reaction_add', timeout=20.0)
                            if "➡️" in str(reaction):
                                edited = '```' + "\n".join(line for line in msg.split('\n')[looper:looper+20]) + '```'
                                await sent.edit(content=edited)
                                if looper+20<len(msg.split('\n')):
                                    looper += 20
                                else:
                                    looper=0
                            else:
                                if looper-20>=0:
                                    edited = '```' + "\n".join(line for line in msg.split('\n')[looper-20:looper]) + '```'
                                    await sent.edit(content=edited)
                                    looper -=20

                        except Exception as e:
                            print(e)
                            break
                else:
                    await ctx.send(msg)
            else:
                await ctx.send('The queue is empty')
                    
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.guild.voice_client
        voice.pause()
        await ctx.send('paused current track')

    @commands.command(aliases=["next", "fs"])
    async def skip(self, ctx):
        voice = ctx.guild.voice_client
        voice.stop()

    @commands.command()
    async def np(self, ctx):
        try:
            await ctx.send(f"{self.queue[self.current_track]} is playing, {self.current_track+1} is the index in queue")
        except IndexError:
            await ctx.send(f"{self.current_track}")

    @commands.command()
    async def jump(self, ctx, index):
        try:
            if int(index):
                voice = ctx.guild.voice_client
                voice.stop()
                self.current_track = int(index)-2
                self.segue(ctx)
        except:
            await ctx.send("abbey chutiye number daal jump likhne ke baad", delete_after=2.5)