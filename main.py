from discord.ext import commands
import discord
import json 
import datetime
import asyncio
from funcs.auth import token
from cogs.imageManipulation import imageManipulation
from cogs.music import music
from cogs.tts import tts

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    game = discord.Game("RANDEEB")
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=game, status=discord.Status.idle)

@bot.event
async def on_member_join(member):
    channel = await discord.utils.get(member.guild.channels, name="laat")
    await channel.send("How long till we kick the new member? [tell in hours] \
        type 'grant' to give permission to stay")
    timer = await bot.wait_for("message")
    try:
        if float(timer):
            with open('kickers.json', 'r+') as file:
                content = file.read()
                content = json.loads(content)
                data = {
                    "jointime": datetime.datetime.now(),
                    "timeallowed": timer*60*60
                }
                content[member.guild][member.id] = data
    except:
        if timer != 'grant':
            member.guild.kick(member)

@bot.command()
async def echo(ctx, *args):
    msg = ' '.join(arg for arg in args)
    await ctx.channel.purge(limit=1)
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

async def main():
    async with bot:
        await bot.load_extension('cogs.music')
        await bot.load_extension('cogs.imageManipulation')
        await bot.load_extension('cogs.tts')
        await bot.start(token)

asyncio.run(main())