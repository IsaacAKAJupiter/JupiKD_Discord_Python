import discord
from discord.ext import commands

import os, sys, pathlib

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

    #WIP
    #@commands.command(hidden=True)
    #@commands.is_owner()
    #async def restart(self, ctx):
    #    main_bot_folder = pathlib.Path(__file__).parent.parent.name
    #    os.execl(main_bot_folder + "/bot.py", *sys.argv)

def setup(bot):
    bot.add_cog(OwnerCog(bot))