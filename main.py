from discord.ext import commands
from hanuman.funcs.auth import token
from hanuman.cogs.music import MusicPlayer 
from hanuman.cogs.welcoming import Greetings

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def penis(ctx):
    await ctx.reply('hello')

bot.add_cog(MusicPlayer(bot))
# bot.add_cog(Greetings(bot))
bot.run(token)