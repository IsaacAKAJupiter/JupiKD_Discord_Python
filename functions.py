import os, aiohttp, requests, discord, io

from PIL import Image, ImageFilter

import config, databasefunctions

#This function retrieves the specified guild prefix.
async def GetGuildPrefix(guild_id):
    url = "http://localhost/API/jupikd_discord/getguildprefix.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild_id
    }
    jsonURL = await PostRequest(url, params)
    #Check if jsonURL isn't None and the success key is true. If so, return the prefix.
    if jsonURL != None and jsonURL["success"] == True:
        return jsonURL["bot_prefix"]
    else:
        return None

#This function retrieves the specified guild table information from the database.
async def GetGuildInfo(guild, table):
    url = "http://localhost/API/jupikd_discord/getguildinfo.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "table": table
    }
    jsonURL = await PostRequest(url, params)
    #Check if jsonURL isn't None.
    #Since the API returns the guild info and doesn't include the key "error", check if error is in it.
    if jsonURL != None and not "error" in jsonURL:
        return jsonURL
    else:
        return None

#This function retrieves all the default commands and their permissions that are registered in the table.
async def GetDefaultCommandPermissions():
    url = "http://localhost/API/jupikd_discord/getdefaultcommandpermissions.php"
    params = {
        "key": config.jupsapikey
    }
    jsonURL = await PostRequest(url, params)
    if jsonURL != None and not "success" in jsonURL:
        return jsonURL
    else:
        return None

#This function retrieves the specified guild table information from the database. (non-async/requests lib)
def GetGuildInfoNonAsync(guild, table):
    try:
        url = "http://localhost/API/jupikd_discord/getguildinfo.php"
        params = {
            "key": config.jupsapikey,
            "serverid": guild.id,
            "table": table
        }
        resp = requests.post(url, data=params)
        jsonURL = resp.json()

        if not "success" in jsonURL:
            return jsonURL
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")


#This function checks and adds guilds in/to the database.
async def CheckAndAddGuild(guild):
    url = "http://localhost/API/jupikd_discord/addguildtodatabase.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "servername": guild.name,
        "serverowner": guild.owner.id
    }
    await PostRequest(url, params)

#This function checks and adds commands in/to the database.
#Similar to the CheckAndAddGuild function.
async def CheckAndAddCommand(command):
    #Split description and permission since permission isn't an actual thing in discord.py.
    desc_permission = command.help.split(" jupikdsplit->")

    #Get all the parameters. Check if they have any then turn into a string.
    params = ""
    if command.clean_params:
        params = command.name
        for param, _ in sorted(command.clean_params.items()):
            params += f" [{param}] "

        params = params[:-1]
    else:
        params = command.name
    
    #Turn the aliases list into a string to send to API.
    aliases = ""
    for i in command.aliases:
        aliases += f"{i}, "

    #Get rid of the last comma.
    aliases = aliases[:-2]

    url = "http://localhost/API/jupikd_discord/addcommandtodatabase.php"
    params = {
        "key": config.jupsapikey,
        "name": command.name,
        "description": desc_permission[0],
        "usage": params,
        "permission": desc_permission[1],
        "category": command.cog_name,
        "aliases": aliases
    }
    await PostRequest(url, params)

#This function deletes the guild from the database.
async def DeleteGuild(guild):
    url = "http://localhost/API/jupikd_discord/removeguildfromdatabase.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id
    }
    json = await PostRequest(url, params)
    if json["success"] == False:
        print(f"ERROR DELETING GUILD => Guild ID: {guild.id} | Guild Name: {guild.name} | Guild Owner: {guild.owner.id} | json: {json}")

async def DeleteGuildFromID(guild):
    url = "http://localhost/API/jupikd_discord/removeguildfromdatabase.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild
    }
    json = await PostRequest(url, params)
    if json["success"] == False:
        print(f"ERROR DELETING GUILD => Guild ID: {guild.id} | json: {json}")

#This function will delete guilds not supposed to be in the database.
async def DeleteAllRemovedGuilds(guilds):
    url = "http://localhost/API/jupikd_discord/getallguildsindatabase.php"
    params = {
        "key": config.jupsapikey
    }
    databaseguilds = await PostRequest(url, params)

    for guild in databaseguilds:
        if guild["server_id"] not in guilds:
            await DeleteGuildFromID(guild["server_id"])

#This function gets an emoji from a message.
async def GetEmojiFromMessage(message):
    #Since custom emojis cannot have "<" or ">" in their name, we can check if it is a custom emoji with this.
    #Get the ID by getting the colons then from the last colon to the end should be the name (+1 | -1)
    if "<" in message and ">" in message:
        colons = [e for e, chars in enumerate(message) if chars == ":"]
        emoji_id = message[colons[1] + 1: -1]
    else:
        return None, None, None

    emoji_extension = "png"
    if message.startswith("<a"):
        emoji_extension = "gif"

    return emoji_id, emoji_extension, message[colons[0] + 1 : colons[1]]

#This function will get the last message with an image attachment.
async def GetLastMessageWithImage(ctx):
    #Get the channel to search for the messages.
    async for m in ctx.channel.history(limit=100):
        if len(m.attachments) > 0:
            if m.attachments[0].height != None and m.attachments[0].width != None:
                return m

    return None

#This function gets an image from a message.
async def GetImageFromMessage(ctx, image):
    #Check if there is an attachment and if there is then save it to disk.
    #If there isn't check if the member sent an image link.
    if len(ctx.message.attachments) > 0:
        if ctx.message.attachments[0].height != None and ctx.message.attachments[0].width != None:
            await ctx.message.attachments[0].save(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")
            image = Image.open(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")
        else:
            return False
    elif len(ctx.message.mentions) > 0:
        image = await ImageRequest(ctx.message.mentions[0].avatar_url_as(format="png"))
    else:
        original_image = image
        #Check if the author wrote a ^ to get the last image as an attachment.
        if image == "^":
            image = await GetLastMessageWithImage(ctx)
            await image.attachments[0].save(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")
            image = Image.open(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")
            return image

        #Check if the message is for an emoji.
        emoji_id, emoji_extension, emoji_name = await GetEmojiFromMessage(original_image)
        if emoji_id and emoji_extension and emoji_name:
            image = await ImageRequest(f"https://cdn.discordapp.com/emojis/{emoji_id}.{emoji_extension}")
        else:
            image = None
        
        #Check if image is still None then check if it's a member.
        if image == None:
            image = await GetMemberByName(ctx.guild, original_image)
            if image != None:
                image = await ImageRequest(image.avatar_url)
        
        #Check if image is still None then check if the original_image is just a link to an image.
        if image == None:
            image = await ImageRequest(original_image)
        
    #After checking all of those, check if image is None, then return False/image.
    if image == None:
        return False
    else:
        return image

#This function will deal with the template image manipulation commands.
async def TemplateImageManipulate(ctx, image, width, height, x, y, path):
    #Get the image from the function above.
    image = await GetImageFromMessage(ctx, image)
    if image == False:
        await ctx.send("You didn't send an image attachment and your link was either blank or not a link to an image.")
        return False
    
    #Crop the new image onto the template.
    bottom_image = Image.open(f"../../JupiKD_Discord_Python/images/{path}.png")
    image = image.resize((width, height))
    bottom_image.paste(image, (x, y))
    bottom_image.save(f"../../JupiKD_Discord_Python/images/{ctx.author.id}-{ctx.message.id}.png")

    return True

#This function will return an embed with the default settings.
async def CreateEmbed(title = None, description = None, footer = None, image = None, thumbnail = None, url = None, author = None):
    embed = discord.Embed()
    embed.colour = 0xf1c40f

    #Check if the other parameters are None, and if not, set.
    if title != None:
        embed.title = title

    if description != None:
        embed.description = description

    if footer != None:
        embed.set_footer(text=footer[0], icon_url=footer[1])

    if image != None:
        embed.set_image(url=image)
    
    if thumbnail != None:
        embed.set_thumbnail(url=thumbnail)
    
    if url != None:
        embed.url = url

    if author != None:
        embed.set_author(name=author[0], url=author[1], icon_url=author[2])

    #Return the final embed.
    return embed

#This function will look for a member based on a name and return the closest member.
async def GetMemberByName(guild, name):
    #Loop through members in the guild.
    #Check if the name is in members name or nickname (in because should work without full name.)
    for member in guild.members:
        if member.nick != None:
            if name.lower() in member.name.lower() or name.lower() in member.nick.lower():
                return member
        else:
            if name.lower() in member.name.lower():
                return member
    
    return None

#This function will get the latest message from a member that isn't an embed.
async def MemberLatestMessage(channel, member):
    #Loop through 100 messages in the channel.
    #Return message object that doesn't have an embed.
    async for m in channel.history(limit=100):
        if m.author == member and len(m.embeds) < 1:
            return m

#This function will return the member objects for mods, admins or the owner.
async def GetMemberObjects(guild, column):
    server = await GetGuildInfo(guild, "server")

    #Get the right column and make sure it's not None/empty.
    #Split into list, loop through list and return all the member objects.
    if server != None and server[0][column] != None and server[0][column] != "":
        id_list = server[0][column].split(",")
        members = []
        for member in id_list:
            members.append(guild.get_member(int(member)))

        return members

#This function adds to the usage of a command in the database.
async def AddUseToCommand(ctx):
    url = "http://localhost/API/jupikd_discord/incrementusagedefaultcommands.php"
    params = {
        "key": config.jupsapikey,
        "name": ctx.command.name
    }
    jsonURL = await PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function returns the song queue for a guild.
async def GetSongQueue(guild):
    url = "http://localhost/API/jupikd_discord/getsongqueue.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id
    }
    return await PostRequest(url, params)

#This function will check to see if a command exists.
async def CommandExist(bot, command):
    for i in bot.commands:
        if not i.cog_name == None and not i.cog_name == "OwnerCog":
            if i.name == command:
                return True

    return False

#This function will get a post from Reddit with the filter/sub.
async def RedditPost(ctx, sub, sfilter, params = ""):
    #Use the Reddit API with the sub and the filter (random/top/etc).
    url = f"http://www.reddit.com/r/{sub}/{sfilter}/.json{params}"
    params = {
        "after": "t3_1ubf3e"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, data=params) as resp:
                jsonURL = await resp.json()
                session.close()

        if sfilter == "random":
            jsonURL = jsonURL[0]

        #Check if the Reddit post was NSFW and if the channel the message was sent in was NSFW. If not return False.
        if jsonURL["data"]["children"][0]["data"]["over_18"] == True and ctx.channel.is_nsfw() == False:
            return "NSFW", None

        image = jsonURL["data"]["children"][0]["data"]["url"]

        #For each of the image/gif providers, return the gif URL.
        #if "supload" in image:
        #    image = image[19:-5]
        #    image = f"https://i.supload.com/{image}-hd.gif"

        #if "gfycat" in image and not "thumbs" in image:
        #    if "gifs" in image and not "detail" in image:
        #        image = image[23:]
        #    elif "gifs" in image and "detail" in image:
        #        image = image[30:]
        #    elif not "gifs" in image and not "detail" in image:
        #        image = image[18:]
        #    image = image.replace("/", "")
        #    async with aiohttp.ClientSession() as session:
        #        async with session.get(url=f"https://api.gfycat.com/v1/gfycats/{image}", data={"Authorization": f"Bearer {config.gfycatapikey}"}) as resp2:
        #            jsonURL2 = await resp2.json()
        #            session.close()

        #    image = jsonURL2["gfyItem"]["gifUrl"]

        #if "imgur" in image and not "i.imgur" in image:
        #    imgur_id = image[-8:]
        #    imgur_id = imgur_id.replace("/", "")
        #    image = f"https://i.imgur.com/{imgur_id}.gif"
        
        #if "v.redd.it" in image:
        #    image = f"{image}/DASH_9_6_M"

        #if ".gifv" in image:
        #    image = image[:-1]

        return jsonURL, image

    except Exception:
        return None, None

#This function is for the basic Reddit return embed.
async def RedditDefaultEmbed(jsonURL, image, bot):
    #Maybe change this to include other sites, but this just checks if the URL is the Reddit link, or if it's Youtube, don't show an image.
    if ("youtu.be" in image or "youtube" in image) or jsonURL["data"]["children"][0]["data"]["permalink"] in jsonURL["data"]["children"][0]["data"]["url"]:
        embed = await CreateEmbed(
            author=(bot.user.display_name, discord.Embed.Empty, bot.user.avatar_url_as(format="png")),
            footer=("Due to Reddit's native video/gif implementation, some of the gifs/videos won't show. Also some hosts use .gifv which is not supported by Discord Embeds.", discord.Embed.Empty)
        )
    else:
        embed = await CreateEmbed(
            author=(bot.user.display_name, discord.Embed.Empty, bot.user.avatar_url_as(format="png")),
            #image=image,
            footer=("Due to Reddit's native video/gif implementation, some of the gifs/videos won't show. Also some hosts use .gifv which is not supported by Discord Embeds.", discord.Embed.Empty)
        )

    #Set the rest of the embed then return.
    embed.add_field(name="Title", value=jsonURL["data"]["children"][0]["data"]["title"])
    embed.add_field(name="Author", value=jsonURL["data"]["children"][0]["data"]["author"], inline=False)
    if not jsonURL["data"]["children"][0]["data"]["permalink"] in jsonURL["data"]["children"][0]["data"]["url"]:
        embed.add_field(name="Insta Link", value=image, inline=False)
    embed.add_field(name="URL", value=f"https://reddit.com{jsonURL['data']['children'][0]['data']['permalink']}", inline=False)

    return embed

#This function will check if a member has higher permissions than another member.
async def CheckHigherPermission(ctx, first_member, second_member):
    #Check the main permissions you cannot kick. (Owner and Admin).
    if await CheckPermission(ctx.guild, first_member.id, "Owner") == True:
        return True

    if await CheckPermission(ctx.guild, first_member.id, "Admin") == True and await CheckPermission(ctx.guild, second_member.id, "Admin") == False and await CheckPermission(ctx.guild, second_member.id, "Owner") == False:
        return True

    #Get the command permission so the author can't kick the same permission.
    permission = GetPermissionForCommand(ctx, ctx.command.name)
    if await CheckPermission(ctx.guild, first_member.id, permission) == True and await CheckPermission(ctx.guild, second_member.id, permission) == False and await CheckPermission(ctx.guild, second_member.id, "Admin") == False and await CheckPermission(ctx.guild, second_member.id, "Owner") == False:
        return True

    #If the checks fail, return False.
    return False

#This function checks if a member has a specific permission.
async def CheckPermission(guild, member_id, permission):
    #Check if the permission was one of the main permissions (Member, Mod, Admin, Owner).
    json = await GetGuildInfo(guild, "server")
    if permission == "Member":
        return True

    elif permission == "Mod":
        if json[0]["moderators"] != None:
            if str(member_id) in json[0]["moderators"]:
                return True
        if json[0]["admins"] != None:
            if str(member_id) in json[0]["admins"]:
                return True

    elif permission == "Admin":
        if json[0]["admins"] != None:
            if str(member_id) in json[0]["admins"]:
                return True

    elif permission == "Owner":
        if member_id == json[0]["owner"]:
            return True
    else:
        #Check if the permission exists in custom_permissions table.
        #If it does and the member specified is in it, then return True.
        json = await GetGuildInfo(guild, "custom_permissions")
        if json != None and json != "":
            for i in json:
                if i["name"] == permission:
                    if i["users"] != None:
                        if str(member_id) in i["users"]:
                            return True
    return False

#This function checks if the member has permission to use a command.
async def MemberPermCommandCheck(ctx):
    #If the member is the bot owner or the guild owner, return True.
    if ctx.author.id == ctx.guild.owner.id or ctx.author.id == config.bot_owner:
        return True

    permission = await GetPermissionForCommand(ctx, ctx.command.name)
    if permission != None:
        check = await CheckPermission(ctx.guild, ctx.author.id, permission)
        if check == True:
            return True
        else:
            return False

#This function will check if a guild is premium.
async def CheckGuildPremium(ctx):
    #Send a request to my API to see if the guild is premium.
    url = "http://localhost/API/jupikd_discord/checkifguildpremium.php"
    params = {
        "key": config.jupsapikey,
        "serverid": ctx.guild.id
    }
    jsonURL = await PostRequest(url, params)

    if jsonURL != None:
        if jsonURL["success"] == True:
            return True
    
    return False

#This function gets the permission for a command.
async def GetPermissionForCommand(ctx, command):
    #Check if the guild modified the permission for the command.
    json = await GetGuildInfo(ctx.guild, "server_default_command_permissions")
    if json != None:
        for i in json:
            if i["name"] == command:
                return i["permission"]

    #If they didn't modify, check default command permissions.
    json = await GetDefaultCommandPermissions()
    for i in json:
        if i["name"] == command:
            return i["permission"]
     
#This function checks if a message includes a blacklisted word.
async def CheckIfBlacklistedWord(message):
    #Check if bot owner or guild owner then return False.
    if message.author.id == message.guild.owner.id or message.author.id == config.bot_owner:
        return False

    #Get the table from the database (just the specific guild entries).
    json = await GetGuildInfo(message.guild, "blacklisted_words")

    #Make sure the json isn't None/empty.
    #Then loop through each entry and check if the channel matches.
    if json != None:
        for i in json:
            if i["channel"] == message.channel.id:
                words = i["words"].split(",")
                for word in words:
                    if word.lower() in message.content.lower():
                        return True

    return False

#This function deals with when a member gets removed a guild. (removes permissions, check for leave message)
async def OnMemberRemoveCheck(member, user):
    #Check if the user was either a mod or an admin. Then remove them.
    if await CheckPermission(member.guild, member.id, "Mod"):
        await databasefunctions.UpdateDatabase(member.guild, "server", "moderators", add=False, new_value=member.id, old_value=None)
        print(f"Member: {member.name} was a mod.")

    if await CheckPermission(member.guild, member.id, "Admin"):
        await databasefunctions.UpdateDatabase(member.guild, "server", "admins", add=False, new_value=member.id, old_value=None)
        print(f"Member: {member.name} was an admin.")

    #Check if the user object was None when passed, then return.
    if user == None:
        return None, None

    #Get the user's name and descriminator to pass to the f string.
    user_replace = f"__{user.name}#{user.discriminator}__" 

    #Get the table from the database (just the specific guild entries).
    #Make sure the variable isn't None/empty, then check through each custom permission.
    custom_permissions = await GetGuildInfo(member.guild, "custom_permissions")
    if custom_permissions != None and custom_permissions != "":
        for i in custom_permissions:
            name = i["name"]
            #Check if the member has the permission. Then update the database.
            if i["users"] != None:
                if str(member.id) in i["users"]:
                    await databasefunctions.UpdateCustomPermission(member.guild, name, "users", add=False, old_value=None, new_value=member.id)
                    print(f"Member: {member.name} was in the custom permission: {name}.")

    #Get the table from the database (just the specific guild entries).
    #Make sure the variable isn't None/empty.
    join_leave_messages = await GetGuildInfo(member.guild, "join_leave_messages")
    if join_leave_messages != None and join_leave_messages != "":
        #Shouldn't have to loop through the variable since there should only be 1 entry per guild.
        if join_leave_messages[0]["leave_enabled"] == True:
            if join_leave_messages[0]["leave_message"] != None or join_leave_messages[0]["leave_message"] != "":
                if join_leave_messages[0]["leave_channel"] != None or join_leave_messages[0]["leave_channel"] != "":
                    #After checks for None/empty and making sure it's enabled, get the leave message.
                    #Replace dynamic message options to work correctly, then return the message and channel.
                    leave_message = join_leave_messages[0]["leave_message"]
                    leave_message = leave_message.replace(f"{{user}}", user_replace)
                    leave_message = leave_message.replace(f"{{member}}", user_replace)
                    leave_message = leave_message.replace(f"{{usercount}}", str(len(member.guild.members)))
                    leave_message = leave_message.replace(f"{{membercount}}", str(len(member.guild.members)))
                    return leave_message, join_leave_messages[0]["leave_channel"]
        else:
            return None, None

#This function deals with the join message when a member joins a guild.
async def OnMemberJoinCheck(member):
    #Get the table from the database (just the specific guild entries).
    server = await GetGuildInfo(member.guild, "server")
    #Check to see if the member should be getting a role upon joining.
    if server[0]["join_role"] != None:
        join_role = [r for r in member.guild.roles if r.id == server[0]["join_role"]]
        if join_role:
            try:
                await member.add_roles(join_role[0], reason="Automatic Join Role")
            except Exception:
                pass
        else:
            #If the role is messed up, remove it from the database.
            await databasefunctions.UpdateDatabase(member.guild, "server", "join_role", add=True, new_value=None, old_value=None)
    #Make sure the variable isn't None/empty, then check through each custom permission.
    join_leave_messages = await GetGuildInfo(member.guild, "join_leave_messages")
    if join_leave_messages != None and join_leave_messages != "":
        #Shouldn't have to loop through the variable since there should only be 1 entry per guild.
        if join_leave_messages[0]["join_enabled"] == True:
            if join_leave_messages[0]["join_message"] != None or join_leave_messages[0]["join_message"] != "":
                if join_leave_messages[0]["join_channel"] != None or join_leave_messages[0]["join_channel"] != "":
                    #After checks for None/empty and making sure it's enabled, get the leave message.
                    #Replace dynamic message options to work correctly, then return the message and channel.
                    join_message = join_leave_messages[0]["join_message"]
                    join_message = join_message.replace(f"{{user}}", member.mention)
                    join_message = join_message.replace(f"{{member}}", member.mention)
                    join_message = join_message.replace(f"{{usercount}}", str(len(member.guild.members)))
                    join_message = join_message.replace(f"{{membercount}}", str(len(member.guild.members)))
                    return join_message, join_leave_messages[0]["join_channel"]
        else:
            return None, None

#This function is a central hub for post requests with aiohttp. (json response only)
async def PostRequest(url, params):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=params) as resp:
                jsonURL = await resp.json()
                session.close()

        #Check to see if something broke AKA if jsonURL is None.
        #This will also error if the page isn't in json.
        if jsonURL != None:
            return jsonURL
        else:
            return None

    #Catch exception, print, and return None.
    except Exception as e:
        print(f"Error: {e}")
        return None

#This function is a central hub for get requests with aiohttp. (json response only)
async def GetRequest(url, params):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, params=params) as resp:
                jsonURL = await resp.json()
                session.close()

        #Check to see if something broke AKA if jsonURL is None.
        #This will also error if the page isn't in json.
        if jsonURL != None:
            return jsonURL
        else:
            return None

    #Catch exception, print, and return None.
    except Exception as e:
        print(f"Error: {e}")
        return None

async def ImageRequest(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                image = Image.open(io.BytesIO(await resp.read()))
                session.close()
                return image
    except Exception:
        return None