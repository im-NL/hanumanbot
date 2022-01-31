from discord.ext import commands

class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command()
    async def meme(self, ctx):
        url = ctx.message.attachments[0].url
        if url == None:
            await ctx.send("I don't see a photo")
            await ctx.send("chutiya")
        else:
            await ctx.send(f'```{url}```')