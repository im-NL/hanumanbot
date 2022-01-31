from discord.ext import commands
from hanuman.cogs.imageManipulation import ImageManipulation
from hanuman.funcs.auth import token
from hanuman.cogs.music import MusicPlayer 
from hanuman.cogs.welcoming import Greetings
import discord 

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    game = discord.Game("ram bhajan simulator")
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=game, status=discord.Status.idle)

@bot.command()
async def penis(ctx):
    await ctx.reply('hello')

# bot.add_cog(MusicPlayer(bot))
bot.add_cog(ImageManipulation(bot))
# bot.add_cog(Greetings(bot))
bot.run(token)