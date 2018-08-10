import discord
from discord.ext import commands

import aiohttp

import functions, config, databasefunctions

class AdminCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["moderator"])
    async def mod(self, ctx):
        """Command which makes a member a moderator. jupikdsplit->Admin"""

        if len(ctx.message.mentions) > 0:
            new_value = ctx.message.mentions[0]
        else:
            new_value = ctx.author

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "moderators", add=True, new_value=new_value.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="New Mod Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Mod Denied",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        embed.add_field(name="Mod Mention", value=new_value.mention, inline=True)
        embed.add_field(name="Mod ID", value=new_value.id, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["unmoderator"])
    async def unmod(self, ctx):
        """Command which removes a member from moderators. jupikdsplit->Admin"""

        if len(ctx.message.mentions) > 0:
            new_value = ctx.message.mentions[0]
        else:
            new_value = ctx.author

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "moderators", add=False, new_value=new_value.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="Removed Mod Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="Removed Mod Denied",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        embed.add_field(name="Mod Mention", value=new_value.mention, inline=True)
        embed.add_field(name="Mod ID", value=new_value.id, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["botprefix", "changeprefix"])
    async def prefix(self, ctx, prefix):
        """Command which changes the bots prefix for the guild. jupikdsplit->Admin"""

        #Don't need to check the new prefix length since its going to just fail if it's over.
        #Get current prefix.
        current_prefix = await functions.GetGuildPrefix(ctx.guild.id)

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "bot_prefix", add=False, new_value=prefix, old_value=current_prefix) == True:
            embed = await functions.CreateEmbed(
                title="New Prefix Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Prefix Denied.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        new_prefix = await functions.GetGuildPrefix(ctx.guild.id)

        embed.add_field(name="Old Prefix", value=current_prefix, inline=True)
        embed.add_field(name="New Prefix", value=new_prefix, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCommands(bot))