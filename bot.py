import discord
from discord.ext import commands

import sys, traceback, aiohttp, datetime

import config, functions, databasefunctions

if not discord.opus.is_loaded():
    discord.opus.load_opus("opus")

async def get_prefix(bot, message):
    prefixes = ["^"]

    if message.guild:
        prefix = await functions.GetGuildPrefix(message.guild.id)
        if prefix != None:
            return commands.when_mentioned_or(prefix)(bot, message)

    return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = [
    "cogs.owner",
    "cogs.general",
    "cogs.guildowner",
    "cogs.funcommands",
    "cogs.util",
    "cogs.admin",
    "cogs.mod",
    "cogs.image",
    "cogs.voice",
    "cogs.nsfw"
]

bot = commands.Bot(command_prefix=get_prefix, description="JupiKD, all purpose Discord bot. Created by: Isaac™#1240")

if __name__ in "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}. Error: {e}.", file=sys.stderr)
            traceback.print_exc()

@bot.check
async def block_dms(ctx):
    return ctx.guild != None

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

    #Update the database to store the bots startup time.
    url = "http://localhost/API/jupikd_discord/updatebotuptime.php"
    params = {
        "key": config.jupsapikey,
        "uptime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    jsonURL = await functions.PostRequest(url, params)

    if jsonURL == None or jsonURL["success"] == False:
        print("WARNING: Bot Uptime failed.")

    #Check to see if the guilds are in the database, and remove all the left guilds in the database.
    guilds = []
    for guild in bot.guilds:
        guilds.append(guild.id)
        await functions.CheckAndAddGuild(guild)

    await functions.DeleteAllRemovedGuilds(guilds)

    #Check to see if the commands are in the database.
    for command in bot.commands:
        if not command.cog_name == None and not command.cog_name == "OwnerCog":
            await functions.CheckAndAddCommand(command)

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
            if await functions.CheckIfBlacklistedWord(message) == True and message.author != bot.user:
                await message.delete()
                return

    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    if ctx.command.cog_name != "OwnerCog" and ctx.command.cog_name != None:
        if await functions.AddUseToCommand(ctx) == False:
            print(f"ERROR: Adding use to Command | Command used: {ctx.command.name}")

@bot.event
async def on_member_remove(member):
    #Get the user object to also pass to the function.
    user = bot.get_user(member.id)

    #Call the function to get the channel and message for the member leaving.
    remove_message, channel = await functions.OnMemberRemoveCheck(member, user)
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
    if not isinstance(error, commands.CommandNotFound) and not isinstance(error, commands.CheckFailure):
        await ctx.send(f"An error was raised: \"{error}\" | Used command: \"{ctx.message.content}\" | User: {ctx.author.mention}")
    elif isinstance(error, commands.CheckFailure):
        for i in ctx.command.checks:
            if (i.__qualname__) == "is_nsfw.<locals>.pred":
                embed = await functions.CreateEmbed(
                    author=(bot.user.display_name, discord.Embed.Empty, bot.user.avatar_url_as(format="png")),
                    image="https://jups.xyz/images/nsfw.gif"
                )
                embed.add_field(name="Error", value="You cannot use NSFW commands in a non-NSFW channel.")
                await ctx.send(embed=embed)
                return
            elif (i.__qualname__) == "CheckGuildPremium":
                await ctx.send("Your guild is not premium.")
                return
        
        await ctx.send("You do not have permission.")

bot.run(config.token, bot=True, reconnect=True)