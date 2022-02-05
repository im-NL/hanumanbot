from discord.ext import commands
from hanuman.cogs.imageManipulation import ImageManipulation
from hanuman.funcs.auth import token
from hanuman.cogs.music import MusicPlayer
from hanuman.cogs.tts import TTS
import discord 
import asyncio 

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    game = discord.Game("ram bhajan simulator")
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=game, status=discord.Status.idle)

# @bot.event
# async def on_member_join(member):
#     def check(msg):
#         try:
#             int(msg)
#             return True
#         except:
#             return False

#     channel = discord.utils.get(member.guild.channels, name="laat")
#     await channel.send("How long till we kick the new member?")
#     timer = await bot.wait_for("message", check=check)
#     timer = timer*60*60
#     asyncio.sleep(int(timer))
#     await member.guild.kick(member)

@bot.command()
async def echo(ctx, *args):
    msg = ' '.join(arg for arg in args)
    await ctx.send(msg)

bot.add_cog(MusicPlayer(bot))
bot.add_cog(ImageManipulation(bot))
bot.add_cog(TTS(bot))
bot.run(token)