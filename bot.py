import discord
from discord.ext import commands

import sys, traceback, aiohttp

import config, functions, databasefunctions

async def get_prefix(bot, message):
    prefixes = ["^"]

    if not message.guild:
        return "jupikd_privatemessage"

    prefix = await functions.GetGuildPrefix(message.guild.id)
    if prefix != None:
        return commands.when_mentioned_or(prefix)(bot, message)

    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = [
    "cogs.owner",
    "cogs.general"
]

bot = commands.Bot(command_prefix=get_prefix, description="JupiKD, all purpose Discord bot. Created by: Isaac™#1240")

if __name__ in "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}. Error: {e}.", file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    game = discord.Game(name="^help | jups.xyz")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Bot Online!")
    print(f"Discord.py Version: {discord.__version__}")
    print(f"Guilds Joined: {len(bot.guilds)}")
    print(f"Commands Loaded: {len(bot.commands)}")
    print(f"Bot Name: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")

    guilds = []
    for guild in bot.guilds:
        guilds.append(guild.id)
        await functions.CheckAndAddGuild(guild)

    await functions.DeleteAllRemovedGuilds(guilds)

@bot.event
async def on_guild_join(guild):
    await functions.CheckAndAddGuild(guild)

@bot.event
async def on_guild_remove(guild):
    await functions.DeleteGuild(guild)

@bot.event
async def on_guild_update(guild_before, guild_after):
    if guild_before.name != guild_after.name:
        await databasefunctions.UpdateDatabase(guild_after, "server", "name", add=True, new_value=guild_after.name, old_value=guild_before.name)

    #TODO: Use this to check if someone deleted the twitter webhook. await guild.webhooks()

@bot.event
async def on_message(message):
    if message.webhook_id == None:
        if isinstance(message.channel, discord.TextChannel):
            if await functions.CheckIfBlacklistedWord(message) == True:
                await message.delete()
                return

    await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
    remove_message, channel = await functions.OnMemberRemoveCheck(member)
    if remove_message != None and channel != None:
        channel = member.guild.get_channel(channel)
        await channel.send(remove_message)

@bot.event
async def on_member_join(member):
    join_message, channel = await functions.OnMemberJoinCheck(member)
    if join_message != None and channel != None:
        channel = member.guild.get_channel(channel)
        await channel.send(join_message)

@bot.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CommandNotFound):
        await ctx.send(f"An error was raised: \"{error}\" | Used command: \"{ctx.message.content}\" | User: {ctx.author.mention}")

bot.run(config.token, bot=True, reconnect=True)