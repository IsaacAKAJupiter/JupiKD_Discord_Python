import discord
from discord.ext import commands

import sys, traceback, aiohttp

import config, functions

async def get_prefix(bot, message):
    prefixes = ["^"]

    if not message.guild:
        return "jupikd_privatemessage"

    try:
        url = "http://jups.xyz/API/jupikd_discord/getguildprefix.php"
        params = {
            "key": config.jupsapikey,
            "serverid": message.guild.id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=params) as resp:
                jsonURL = await resp.json()
                session.close()

        if jsonURL["success"] == True:
            return commands.when_mentioned_or(jsonURL["prefix"])(bot, message)

    except Exception:
        pass

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
    game = discord.Game(name="^help | twitch.tv/jups | jups.xyz")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("Bot Online!")
    print(f"Discord.py Version: {discord.__version__}")
    print(f"Guilds Joined: {len(bot.guilds)}")
    print(f"Commands Loaded: {len(bot.commands)}")
    print(f"Bot Name: {bot.user.name}")
    print(f"Bot ID: {bot.user.id}")

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