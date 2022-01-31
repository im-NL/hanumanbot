from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import discord
import textwrap

from matplotlib.pyplot import fill

class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command()
    async def meme(self, ctx, *args):
        msg = ' '.join(arg for arg in args)
        bottom_text = None
        if '|' in msg:
            top_text = msg.split('|')[0]
            try:
                bottom_text = msg.split('|')[1]
            except:
                pass
        else:
            top_text = msg
        url = ctx.message.attachments[0]
        await url.save("temp.png")
        img = Image.open("temp.png")
        height = img.height
        width = img.width
        meme = ImageDraw.Draw(img)
        meme.text((width//2, height//10), text=top_text, fill=(255, 255, 255), font=ImageFont.truetype("Impact.ttf", 80), anchor="mm")
        if bottom_text is not None:
            meme.text((width//2, height-height//10), text=bottom_text, fill=(255, 255, 255), font=ImageFont.truetype("Impact.ttf", 80), anchor="mm")
        img.save("temp.png")
        await ctx.send(file=discord.File(r"temp.png"))
