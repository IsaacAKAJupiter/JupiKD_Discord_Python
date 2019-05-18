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
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["sap"])
    async def sendapic(self, ctx, image = None):
        """Command which overlays the given image into the SAP template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 356, 364, 163, 131, "sendapic") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["spat", "discordmeme"])
    async def severalpeoplearetyping(self, ctx, image = None):
        """Command which overlays the given image into the SPAT template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 400, 300, 67, 35, "severalpeoplearetyping") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["television"])
    async def tv(self, ctx, image = None):
        """Command which overlays the given image into the TV template. jupikdsplit->Member"""
        
        if await functions.TemplateImageManipulate(ctx, image, 221, 149, 168, 15, "tv") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["erectiledysfunction"])
    async def ed(self, ctx, image = None):
        """Command which overlays the given image into the ED template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 450, 250, 15, 82, "erectiledysfunction") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["stupidmotherfucker"])
    async def smf(self, ctx, image = None):
        """Command which overlays the given image into the SMF template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 576, 513, 32, 233, "stupidmotherfucker") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["sonofabitch"])
    async def soab(self, ctx, image = None):
        """Command which overlays the given image into the SOAB template. jupikdsplit->Member"""

        if await functions.TemplateImageManipulate(ctx, image, 136, 187, 0, 0, "sonofabitch") == True:
            #Send the new image then delete on disk.
            await ctx.send(file=discord.File(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png"))
            os.remove(f"JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

def setup(bot):
    bot.add_cog(ImageCommands(bot))