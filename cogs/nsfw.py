import discord
from discord.ext import commands

import aiohttp, random

import functions, config, databasefunctions

class NSFWCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.is_nsfw()
    @commands.command(aliases=["boobs"])
    async def tits(self, ctx):
        """Command which gets a random picture of boobs. jupikdsplit->Member"""

        r_num = random.randint(0, 12085)
        url = f"http://api.oboobs.ru/boobs/{r_num}"
        jsonURL = await functions.GetRequest(url, None)

        if jsonURL != None:
            embed = await functions.CreateEmbed(
                image=f"http://media.oboobs.ru/{jsonURL[0]['preview']}"
            )

            embed.add_field(name="Insta Link", value=f"http://media.oboobs.ru/{jsonURL[0]['preview']}")
            await ctx.send(embed=embed)
            return
    
        await ctx.send("An error occured.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.is_nsfw()
    @commands.command(aliases=["butt"])
    async def ass(self, ctx):
        """Command which gets a random picture of butts. jupikdsplit->Member"""

        r_num = random.randint(0, 5992)
        url = f"http://api.obutts.ru/butts/{r_num}"
        jsonURL = await functions.GetRequest(url, None)

        if jsonURL != None:
            embed = await functions.CreateEmbed(
                image=f"http://media.obutts.ru/{jsonURL[0]['preview']}"
            )

            embed.add_field(name="Insta Link", value=f"http://media.obutts.ru/{jsonURL[0]['preview']}")
            await ctx.send(embed=embed)
            return
    
        await ctx.send("An error occured.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.is_nsfw()
    @commands.command(aliases=["gayporn"])
    async def gayp(self, ctx):
        """Command which gets a random gifs/pictures of gayp. jupikdsplit->Member"""

        subs = ["blackdicks", "gayporn", "menkissing", "massivecock", "gaybrosgonewild", "penis", "mengonewild", "gaygifs", "gaynsfw"]
        r_num = random.randint(0, 8)

        jsonURL, image = await functions.RedditPost(ctx, subs[r_num], "random")
        if jsonURL == None and image == None:
            await ctx.send("An error occured.")
            return

        embed = await functions.RedditDefaultEmbed(jsonURL, image, self.bot)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.is_nsfw()
    @commands.command(aliases=["lesbianporn"])
    async def lesbian(self, ctx):
        """Command which gets a random gifs/pictures of lesbians. jupikdsplit->Member"""

        subs = ["strapon", "lesbians", "scissoring", "girlskissing", "lesbos", "vagina"]
        r_num = random.randint(0, 5)

        jsonURL, image = await functions.RedditPost(ctx, subs[r_num], "random")
        if jsonURL == None and image == None:
            await ctx.send("An error occured.")
            return

        embed = await functions.RedditDefaultEmbed(jsonURL, image, self.bot)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.is_nsfw()
    @commands.command(aliases=["randomnsfw"])
    async def randnsfw(self, ctx):
        """Command which gets a random gifs/pictures from random NSFW subreddits. jupikdsplit->Member"""

        jsonURL, image = await functions.RedditPost(ctx, "randnsfw", "random")
        if jsonURL == None and image == None:
            await ctx.send("An error occured.")
            return

        embed = await functions.RedditDefaultEmbed(jsonURL, image, self.bot)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(NSFWCommands(bot))