import os, aiohttp, requests

import config

async def GetGuildPrefix(guild_id):
    try:
        url = "http://localhost/API/jupikd_discord/getguildprefix.php"
        params = {
            "key": config.jupsapikey,
            "serverid": guild_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=params) as resp:
                jsonURL = await resp.json()
                session.close()

        if jsonURL["success"] == True:
            return jsonURL["bot_prefix"]

    except Exception as e:
        print(f"Error: {e}")

async def GetGuildInfo(guild, table):
    try:
        url = "http://localhost/API/jupikd_discord/getguildinfo.php"
        params = {
            "key": config.jupsapikey,
            "serverid": guild.id,
            "table": table
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=params) as resp:
                jsonURL = await resp.json()
                session.close()

        if not "success" in jsonURL:
            return jsonURL

    except Exception as e:
        print(f"Error: {e}")

async def GetDefaultCommandPermissions():
    try:
        url = "http://localhost/API/jupikd_discord/getdefaultcommandpermissions.php"
        params = {
            "key": config.jupsapikey
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=url, data=params) as resp:
                jsonURL = await resp.json()
                session.close()

        if not "success" in jsonURL:
            return jsonURL

    except Exception as e:
        print(f"Error: {e}")

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

    except Exception as e:
        print(f"Error: {e}")

#TODO: AddGuildIntoDatabase

async def CheckPermission(guild, member_id, permission):
    if permission == "Member":
        return True
    elif permission == "Mod":
        json = await GetGuildInfo(guild, "server")
        if str(member_id) in json[0]["moderators"]:
            return True
        else:
            return False
    elif permission == "Admin":
        json = await GetGuildInfo(guild, "server")
        if str(member_id) in json[0]["admins"]:
            return True
        else:
            return False
    elif permission == "Owner":
        json = await GetGuildInfo(guild, "server")
        if member_id == json[0]["owner"]:
            return True
        else:
            return False
    else:
        json = await GetGuildInfo(guild, "custom_permissions")
        if json != None and json != "":
            for i in json:
                if i["name"] == permission:
                    if str(member_id) in i["users"]:
                        return True
        return False

async def UserPermCommandCheck(guild, member_id, command):
    if member_id == guild.owner.id or member_id == config.bot_owner:
        return True

    json = await GetGuildInfo(guild, "server_default_command_permissions")
    if json != None:
        for i in json:
            if i["name"] == command:
                check = await CheckPermission(guild, member_id, i["permission"])
                if check == True:
                    return True
                else:
                    return False

    json = await GetDefaultCommandPermissions()
    for i in json:
        if i["name"] == command:
            check = await CheckPermission(guild, member_id, i["permission"])
            if check == True:
                return True
            else:
                return False

#TODO: UpdateTable
async def UpdateDatabase(guild, table, row, new_value, old_value = None, add = True):
    if table == "server" and (row == "moderators" or row == "admins"):
        json = await GetGuildInfo(guild, "server")
        if row == "moderators":
            old_mods = json[0]["moderators"]
            current_mods = old_mods
            if add == True:
                if not str(new_value) in current_mods:
                    current_mods += f",{new_value}"
            else:
                if str(new_value) in current_mods:
                    current_mods = current_mods.split(",")
                    current_mods[:] = [mod for mod in current_mods if not mod == str(new_value)]

                    current_mods_string = ""
                    for i in current_mods:
                        current_mods_string += f"{i},"
                    current_mods = current_mods_string[:-1]

            try:
                url = "http://localhost/API/jupikd_discord/updatedatabase.php"
                params = {
                    "key": config.jupsapikey,
                    "serverid": guild.id,
                    "table": table,
                    "row": row,
                    "new_value": current_mods,
                    "old_value": old_mods
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url=url, data=params) as resp:
                        jsonURL = await resp.json()
                        session.close()

                if not "success" in jsonURL:
                    return jsonURL

            except Exception as e:
                print(f"Error: {e}")
                    
        #elif row == "admins":
        #TODO: Try to clean up mods to combine with admins.


async def CheckIfBlacklistedWord(message):
    json = await GetGuildInfo(message.guild, "blacklisted_words")

    if json != None:
        for i in json:
            if i["channel"] == message.channel.id:
                words = i["words"].split(",")
                for word in words:
                    if word.lower() in message.content.lower():
                        return True

    return False

async def OnMemberRemoveCheck(member):
    if await CheckPermission(member.guild, member.id, "Mod"):
        #TODO: Update Database Table
        print(f"Member: {member.name} was a mod.")

    if await CheckPermission(member.guild, member.id, "Admin"):
        #TODO: Update Database Table
        print(f"Member: {member.name} was an admin.")

    custom_permissions = await GetGuildInfo(member.guild, "custom_permissions")
    for i in custom_permissions:
        name = i["name"]
        users = i["users"].split(",")
        for user in users:
            if user == str(member.id):
                #TODO: Update Database Table
                print(f"Member: {member.name} was in the custom permission: {name}.")

    join_leave_messages = await GetGuildInfo(member.guild, "join_leave_messages")
    for i in join_leave_messages:
        if i["leave_enabled"] == True:
            if i["leave_message"] != None or i["leave_message"] != "":
                if i["leave_channel"] != None or i["leave_channel"] != "":
                    leave_message = i["leave_message"]
                    leave_message = leave_message.replace(f"{{user}}", member.mention)
                    leave_message = leave_message.replace(f"{{member}}", member.mention)
                    leave_message = leave_message.replace(f"{{usercount}}", str(len(member.guild.members)))
                    leave_message = leave_message.replace(f"{{membercount}}", str(len(member.guild.members)))
                    return leave_message, i["leave_channel"]
        else:
            return None, None

async def OnMemberJoinCheck(member):
    join_leave_messages = await GetGuildInfo(member.guild, "join_leave_messages")
    for i in join_leave_messages:
        if i["join_enabled"] == True:
            if i["join_message"] != None or i["join_message"] != "":
                if i["join_channel"] != None or i["join_channel"] != "":
                    leave_message = i["join_message"]
                    leave_message = leave_message.replace(f"{{user}}", member.mention)
                    leave_message = leave_message.replace(f"{{member}}", member.mention)
                    leave_message = leave_message.replace(f"{{usercount}}", str(len(member.guild.members)))
                    leave_message = leave_message.replace(f"{{membercount}}", str(len(member.guild.members)))
                    return leave_message, i["join_channel"]
        else:
            return None, None