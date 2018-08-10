import discord
from discord.ext import commands

import aiohttp

import functions, config, databasefunctions

class ModCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["prune"])
    async def purge(self, ctx, amount):
        """Command which purges/deletes a certain amount of messages in a channel. jupikdsplit->Mod"""

        try:
            amount = int(amount)
        except Exception:
            await ctx.send("The amount needs to be an integer.")
            return
        
        if amount > 100:
            amount = 100

        deleted_messages = await ctx.channel.purge(limit=amount)

        embed = await functions.CreateEmbed(
            title="Purge",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            footer=(f"Channel: #{ctx.channel.name}", discord.Embed.Empty)
        )

        embed.add_field(name="Purge-r", value=ctx.author.mention, inline=True)
        embed.add_field(name="Amount", value=len(deleted_messages), inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(ModCommands(bot))