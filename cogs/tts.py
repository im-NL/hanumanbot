import discord
from discord.ext import commands
from gtts import gTTS
from io import BytesIO
from funcs.FFmpegPCMAudioGTTS import FFmpegPCMAudioGTTS

class tts(commands.Cog):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot 
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
        
    @commands.command()
    async def tts(self, ctx, *args):
        voice = ctx.guild.voice_client
        if voice is None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        voice = ctx.guild.voice_client
        text = ' '.join(arg for arg in args)
        tts = gTTS(text=text, lang="en")
        tts.save('temp/temp.mp3')
        voice.play(discord.FFmpegPCMAudio('temp/temp.mp3'))

    @commands.command()
    async def stop(self, ctx):
        voice = ctx.guild.voice_client
        if voice.is_playing():
            voice.stop()
        else:
            await ctx.send('no audio is playing!')


async def setup(bot):
    await bot.add_cog(tts(bot))