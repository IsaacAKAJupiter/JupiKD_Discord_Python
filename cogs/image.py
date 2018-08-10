import discord
from discord.ext import commands

from PIL import Image, ImageFilter

import aiohttp, datetime, random, asyncio, os

import functions, config, databasefunctions

class ImageCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["sis"])
    async def steppedinshit(self, ctx, image = None):
        """Command which overlays the given image into the SIS template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 68, 67, 86, 267, "steppedinshit") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["sap"])
    async def sendapic(self, ctx, image = None):
        """Command which overlays the given image into the SAP template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 356, 364, 163, 131, "sendapic") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

def setup(bot):
    bot.add_cog(ImageCommands(bot))