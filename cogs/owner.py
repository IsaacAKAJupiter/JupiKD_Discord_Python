import discord
from discord.ext import commands

import os, sys, pathlib, aiohttp
import functions, config

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, cog: str):
        """Command which Loads a Module."""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"Error loading the cog: {cog}.")
            await ctx.send(e)
        else:
            await ctx.send(f"Successfully loaded the cog: {cog}.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, cog: str):
        """Command which Unloads a Module."""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f"Error unloading the cog: {cog}.")
            await ctx.send(e)
        else:
            await ctx.send(f"Successfully unloaded the cog: {cog}.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, cog: str):
        """Command which Reloads a Module."""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"Error reloading the cog: {cog}.")
            await ctx.send(e)
        else:
            await ctx.send(f"Successfully reloaded the cog: {cog}.")

    @commands.command(hidden=True, aliases=["re"])
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Command which reloads all Modules."""

        cogs_dir = "cogs"
        try:
            list_of_cogs = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if ".py" in f]
            for i in list_of_cogs:
                new_i = i.replace(".py", "")
                self.bot.unload_extension(f"{cogs_dir}.{new_i}")
                self.bot.load_extension(f"{cogs_dir}.{new_i}")
        except Exception as e:
            print(f"error: {e}")
            await ctx.send(e)
            await ctx.send("Error reloading all the cogs.")
        else:
            await ctx.send("Successfully reloaded all the cogs.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unloadall(self, ctx):
        """Command which unloads all Modules."""

        cogs_dir = "cogs"
        try:
            list_of_cogs = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if ".py" in f]
            for i in list_of_cogs:
                if i == "owner.py":
                    continue
                    
                new_i = i.replace(".py", "")
                self.bot.unload_extension(f"{cogs_dir}.{new_i}")
        except Exception as e:
            await ctx.send("Error unloading all the cogs.")
            await ctx.send(e)
        else:
            await ctx.send("Successfully unloaded all the cogs.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def loadall(self, ctx):
        """Command which loads all Modules."""

        cogs_dir = "cogs"
        try:
            list_of_cogs = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if ".py" in f]
            for i in list_of_cogs:
                new_i = i.replace(".py", "")
                self.bot.load_extension(f"{cogs_dir}.{new_i}")
        except Exception as e:
            await ctx.send("Error loading all the cogs.")
            await ctx.send(e)
        else:
            await ctx.send("Successfully loaded all the cogs.")

    @commands.command(hidden=True, aliases=["createcommand"])
    @commands.is_owner()
    async def addcommand(self, ctx, name, permission):
        """Command which adds a new command into the database."""

        url = "http://localhost/API/jupikd_discord/createdefaultcommand.php"
        params = {
            "key": config.jupsapikey,
            "name": name,
            "permission": permission
        }
        jsonURL = await functions.PostRequest(url, params)
        if jsonURL != None and jsonURL["success"] == True:
            await ctx.send("Added command.")
        else:
            await ctx.send("Failed adding command.")

    @commands.command(hidden=True, aliases=["removecommand"])
    @commands.is_owner()
    async def deletecommand(self, ctx, name):
        """Command which deletes a command from the database."""

        url = "http://localhost/API/jupikd_discord/deletedefaultcommand.php"
        params = {
            "key": config.jupsapikey,
            "name": name
        }
        jsonURL = await functions.PostRequest(url, params)
        if jsonURL != None and jsonURL["success"] == True:
            await ctx.send("Removed command.")
        else:
            await ctx.send("Failed removing command.")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def editcommand(self, ctx, name, row, new_value):
        """Command which edits a command in the database."""

        url = "http://localhost/API/jupikd_discord/updatedefaultcommand.php"
        params = {
            "key": config.jupsapikey,
            "name": name,
            "row": row, 
            "new_value": new_value
        }
        jsonURL = await functions.PostRequest(url, params)
        if jsonURL != None and jsonURL["success"] == True:
            await ctx.send("Edited command.")
        else:
            await ctx.send("Failed editing command.")

    @commands.command(hidden=True, aliases=["presence"])
    @commands.is_owner()
    async def status(self, ctx, *, newstatus):
        """Command which changes the bot's presence."""
       
        game = discord.Game(name=newstatus)
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(f"New status: \"{newstatus}\".")

    @commands.command(hidden=True, aliases=["announce"])
    @commands.is_owner()
    async def announcement(self, ctx, *, announcement):
        """Command which sends an announcement."""

        for guild in self.bot.guilds:
            for channel in guild.channels:
                if channel.name == "bot_commands" or channel.name == "bot-commands" or channel.name == "botcommands":
                    if type(channel) == discord.channel.TextChannel:
                        embed = await functions.CreateEmbed(
                            title="Announcement",
                            description="This is an announcement from the bot owner. (only sent to channels named bot_commands, bot-commands or botcommands)",
                            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
                        )
                        embed.add_field(name="Actual Announcement", value=announcement)
                        await channel.send(embed=embed)

        await ctx.send("Sent announcement channel to all channels named either bot_commands, bot-commands or botcommands")


def setup(bot):
    bot.add_cog(OwnerCog(bot))