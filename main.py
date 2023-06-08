from discord.ext import commands
import discord
import asyncio
from funcs.auth import token

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