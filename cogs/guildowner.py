import discord
from discord.ext import commands

import aiohttp

import functions, config, databasefunctions

class GuildOwnerCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["administrator"])
    async def admin(self, ctx):
        """Command which makes a member an administrator. jupikdsplit->Owner"""

        if len(ctx.message.mentions) > 0:
            new_value = ctx.message.mentions[0]
        else:
            new_value = ctx.author

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "admins", add=True, new_value=new_value.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="New Admin Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Admin Denied",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        embed.add_field(name="Admin Mention", value=new_value.mention, inline=True)
        embed.add_field(name="Admin ID", value=new_value.id, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["unadministrator"])
    async def unadmin(self, ctx):
        """Command which removes a member from administrators. jupikdsplit->Owner"""

        if len(ctx.message.mentions) > 0:
            new_value = ctx.message.mentions[0]
        else:
            new_value = ctx.author

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "admins", add=False, new_value=new_value.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="Removed Admin Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="Removed Admin Denied",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        embed.add_field(name="Admin Mention", value=new_value.mention, inline=True)
        embed.add_field(name="Admin ID", value=new_value.id, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GuildOwnerCommands(bot))