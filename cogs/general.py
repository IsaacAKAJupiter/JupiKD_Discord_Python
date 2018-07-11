import discord
from discord.ext import commands

import aiohttp

import functions, config

class GeneralCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def twitch(self, ctx):
        """Command which links my twitch."""

        if await functions.UserPermCommandCheck(ctx.guild, ctx.author.id, "twitch") == False:
            await ctx.send("Incorrect Permission")
            return

        await ctx.send("https://twitch.tv/jups")

    @commands.command()
    async def posttest(self, ctx, table):
        info = functions.GetGuildInfoNonAsync(ctx.guild, table)
        await ctx.send(info)

    @commands.command()
    async def dcptest(self, ctx):
        info = await functions.GetDefaultCommandPermissions()
        await ctx.send(info)

    @commands.command()
    async def replacetest(self, ctx):
        try:
            url = "http://localhost/API/jupikd_discord/test.php"
            params = {
                "key": config.jupsapikey,
                "serverid": ctx.guild.id,
                "table": "server"
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, data=params) as resp:
                    jsonURL = await resp.json()
                    session.close()

            if not "success" in jsonURL:
                await ctx.send(jsonURL)

        except Exception as e:
            print(f"Error: {e}")

    @commands.command()
    async def updatetest(self, ctx, newmod = None):
        await functions.UpdateDatabase(ctx.guild, "server", "moderators", str(ctx.message.mentions[0].id), None, False)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))