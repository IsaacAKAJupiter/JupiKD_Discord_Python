import discord
from discord.ext import commands

import aiohttp

import functions, config, databasefunctions

class GeneralCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def twitch(self, ctx):
        """Command which links my twitch."""

        if await functions.MemberPermCommandCheck(ctx.guild, ctx.author.id, "twitch") == False:
            await ctx.send("Incorrect Permission")
            return

        await ctx.send("https://twitch.tv/jups")

    @commands.command()
    async def updatetest(self, ctx, old_value = None, new_value = None):
        if await databasefunctions.UpdateDatabase(ctx.guild, "twitter_notifications", "users", add=True, new_value=old_value, old_value=None) == True:
            await ctx.send("Updated Database.")
        else:
            await ctx.send("Failed to update database.")
        
        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "moderators", add=False, new_value=str(ctx.message.mentions[0].id), old_value=None) == True:
            await ctx.send("Updated Database.")
        else:
            await ctx.send("Failed to update database.")

        if await databasefunctions.UpdateDatabase(ctx.guild, "join_leave_messages", "join_message", add=True, new_value=new_value, old_value=None) == True:
            await ctx.send("Updated Database.")
        else:
            await ctx.send("Failed to update database.")

    @commands.command()
    async def test(self, ctx, name):
        if await databasefunctions.DeleteServerDefaultCommandPermission(ctx.guild, name) == True:
            await ctx.send("Success")
        else:
            await ctx.send("Error")

def setup(bot):
    bot.add_cog(GeneralCommands(bot))