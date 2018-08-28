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

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def kick(self, ctx, member, *, reason = None):
        """Command which kicks a member from the guild. jupikdsplit->Mod"""

        #Check if the author mentioned a member.
        if len(ctx.message.mentions) < 1:
            await ctx.send("You need to mention a member to kick.")
            return
        
        #Check if the member being kicked is higher/same rank as the author.
        if await functions.CheckHigherPermission(ctx, ctx.author, ctx.message.mentions[0]) == False:
            await ctx.send("You cannot kick someone of a higher rank. (Bot Admins/Guild Owner cannot be kicked)")
            return

        #Use a try except since the bot might error trying to kick a member it can't.
        try:
            await ctx.message.mentions[0].kick(reason=reason)
        except Exception:
            await ctx.send(f"I do not have the privilege to kick {ctx.message.mentions[0].name}. (You might be trying to kick yourself...)")
            return

        embed = await functions.CreateEmbed(
            title="Kick",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )

        embed.add_field(name="Mod", value=ctx.author.mention, inline=True)
        embed.add_field(name="Member Kicked", value=f"__{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}__", inline=True)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        try:
            await ctx.message.mentions[0].send(f"You have been kicked from the guild \"{ctx.guild.name}\" with the reason: \"{reason}\".")
        except:
            pass

def setup(bot):
    bot.add_cog(ModCommands(bot))