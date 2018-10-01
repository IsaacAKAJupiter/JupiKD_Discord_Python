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
            await ctx.send("You cannot kick someone of a higher rank.")
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

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def mute(self, ctx, member):
        """Command which gives a member a muted role. jupikdsplit->Mod"""

        #To speed up the command, we aren't going to get the guild info until after we check if the author even mentioned a member.
        if len(ctx.message.mentions) < 1:
            await ctx.send("Please mention the member you would like to mute.")
            return

        server = await functions.GetGuildInfo(ctx.guild, "server")

        #Check if the guild has a muted role set.
        if server[0]["muted_role"] == None:
            await ctx.send("The guild doesn't have a muted role set. Use createmutedrole to create a muted role OR mutedrole [role] to set a role manually.")
            return

        for role in ctx.guild.roles:
            if role.id == server[0]["muted_role"]:
                try:
                    await ctx.message.mentions[0].add_roles(role, reason=f"{ctx.author.name} used the mute command.")
                except Exception:
                    await ctx.send("I do not have the correct permission to mute this member.")
                    return

                await ctx.send(f"{ctx.message.mentions[0].name} has been muted.")
                return
        
        await ctx.send("Couldn't find the muted role in the guild. Please set the muted role again before using this command.")
        await databasefunctions.UpdateDatabase(ctx.guild, "server", "muted_role", add=True, new_value=None, old_value=None)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def unmute(self, ctx, member):
        """Command which removes a muted role from a member. jupikdsplit->Mod"""

        #To speed up the command, we aren't going to get the guild info until after we check if the author even mentioned a member.
        if len(ctx.message.mentions) < 1:
            await ctx.send("Please mention the member you would like to mute.")
            return

        server = await functions.GetGuildInfo(ctx.guild, "server")

        #Check if the guild has a muted role set.
        if server[0]["muted_role"] == None:
            await ctx.send("The guild doesn't have a muted role set. Use createmutedrole to create a muted role OR mutedrole [role] to set a role manually.")
            return

        for role in ctx.message.mentions[0].roles:
            if role.id == server[0]["muted_role"]:
                await ctx.message.mentions[0].remove_roles(role, reason=f"{ctx.author.name} used the unmute command.")
                await ctx.send(f"{ctx.message.mentions[0].name} was unmuted.")
                return

        await ctx.send(f"{ctx.message.mentions[0].name} was not muted.")

def setup(bot):
    bot.add_cog(ModCommands(bot))