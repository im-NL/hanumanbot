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
    game = discord.Game("music vc time cereal killers fr")
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

@bot.command()
async def setstatus(ctx, *args):
    text = ' '.join(arg for arg in args)
    game = discord.Game(text)
    await bot.change_presence(activity=game, status=discord.Status.idle)
    await ctx.send("Changed status to {}".format('**'+text+'**'))

@bot.command()
async def purge(ctx, limit:int):
    await ctx.channel.purge(limit=limit)

bot.add_cog(MusicPlayer(bot))
bot.add_cog(ImageManipulation(bot))
bot.add_cog(TTS(bot))
bot.run(token)