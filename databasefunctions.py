import config, functions

#This function is for updating 3 parts of the database.
async def UpdateDatabase(guild, table, row, add, new_value, old_value = None):
    #Check which table needs updated.
    if table == "server":
        json = await functions.GetGuildInfo(guild, "server")

    elif table == "join_leave_messages":
        json = await functions.GetGuildInfo(guild, "join_leave_messages")

    elif table == "twitter_notifications":
        json = await functions.GetGuildInfo(guild, "twitter_notifications")

    if json == None:
        return False

    old_value = json[0][row]

    #Check for if the row is either mod, admin, or users, since they are different than normal.
    if row == "moderators" or row == "admins" or row == "users":
        #Check if the value is None/Null, if so, make it an empty string.
        if old_value != None:
            current_value = old_value
        else:
            current_value = ""

        if add == True:
            #If adding, make sure it's not currently in it, then add it.
            #Also making sure to set new_value to current_value to be the same across the board.
            if not str(new_value) in current_value:
                if current_value != "":
                    current_value += f",{new_value}"
                    new_value = current_value
                
        else:
            #If not adding, make sure it's not currently in it, then remove it.
            #Split the string into a list, then make a new list, with everything except the removed value in it.
            if str(new_value) in current_value:
                current_value = current_value.split(",")
                current_value[:] = [value for value in current_value if value != str(new_value)]

                #Convert the list back into a string by looping and adding commas after the value.
                #Check if the current_value list is empty/None and get None if it is.
                if len(current_value) > 0 and current_value != None:
                    current_string = ""
                    for i in current_value:
                        current_string += f"{i},"

                    #Remove the final comma by including the whole string minus last character.
                    new_value = current_string[:-1]
                else:
                    new_value = None
            else:
                return False

    if new_value == None and old_value == None:
            return False
    
    #Call API to update database with new/old information.
    #Check if the update was successful and then return based on that.
    url = "http://localhost/API/jupikd_discord/updatedatabase.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "table": table,
        "row": row,
        "new_value": new_value,
        "old_value": old_value
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for inserting an entry into the custom_permissions table.
async def CreateCustomPermission(guild, name):
    #Call a post request to the API to create the permission.
    url = "http://localhost/API/jupikd_discord/createcustompermission.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "name": name
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for deleting an entry from the custom_permissions table.
async def DeleteCustomPermission(guild, name):
    #Call a post request to the API to delete the permission.
    url = "http://localhost/API/jupikd_discord/deletecustompermission.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "name": name
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for updating the custom_permissions table.
async def UpdateCustomPermission(guild, name, row, add, old_value, new_value):
    #Get the guild info from database, make sure it's not empty/None and set old value based on row.
    json = await functions.GetGuildInfo(guild, "custom_permissions")
    if json == None:
        return False

    old_value = None
    for i in json:
        if i["name"] == name:
            old_value = i[row]

    #Check for if the row is users, since it is different than normal.
    if row == "users":
        #Check if the value is None/Null, if so, make it an empty string.
        if old_value != None:
            current_value = old_value
        else:
            current_value = ""

        if add == True:
            #If adding, make sure it's not currently in it, then add it.
            #Also making sure to set new_value to current_value to be the same across the board.
            if not str(new_value) in current_value:
                if current_value != "":
                    current_value += f",{new_value}"
                    new_value = current_value
                
        else:
            #If not adding, make sure it's not currently in it, then remove it.
            #Split the string into a list, then make a new list, with everything except the removed value in it.
            if str(new_value) in current_value:
                current_value = current_value.split(",")
                current_value[:] = [value for value in current_value if value != str(new_value)]

                #Convert the list back into a string by looping and adding commas after the value.
                #Check if the current_value list is empty/None and get None if it is.
                if len(current_value) > 0 and current_value != None:
                    current_string = ""
                    for i in current_value:
                        current_string += f"{i},"

                    #Remove the final comma by including the whole string minus last character.
                    new_value = current_string[:-1]
                else:
                    new_value = None
            else:
                return False
    
    url = "http://localhost/API/jupikd_discord/updatecustompermission.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "name": name,
        "row": row,
        "old_value": old_value,
        "new_value": new_value
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for inserting an entry into the blacklisted_words table.
async def CreateBlacklistedWord(guild, channel):
    #Call a post request to the API to create the permission.
    url = "http://localhost/API/jupikd_discord/createblacklistedword.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "channel": channel
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for deleting an entry from the blacklisted_words table.
async def DeleteBlacklistedWord(guild, channel):
    #Call a post request to the API to delete the permission.
    url = "http://localhost/API/jupikd_discord/deleteblacklistedword.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "channel": channel
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for updating the blacklisted_words table.
async def UpdateBlacklistedWord(guild, channel, add, new_value):
    #Get the guild info from database, make sure it's not empty/None and set old value based on row.
    json = await functions.GetGuildInfo(guild, "blacklisted_words")
    if json == None:
        return False

    old_value = None
    for i in json:
        if i["channel"] == int(channel):
            old_value = i["words"]

    #Check if the value is None/Null, if so, make it an empty string.
    if old_value != None:
        current_value = old_value
    else:
        current_value = ""

    if add == True:
        #If adding, make sure it's not currently in it, then add it.
        #Also making sure to set new_value to current_value to be the same across the board.
        if not new_value in current_value:
            if current_value != "":
                current_value += f",{new_value}"
                new_value = current_value
            
    else:
        #If not adding, make sure it's not currently in it, then remove it.
        #Split the string into a list, then make a new list, with everything except the removed value in it.
        if new_value in current_value:
            current_value = current_value.split(",")
            current_value[:] = [value for value in current_value if value != str(new_value)]

            if not current_value:
                if await DeleteBlacklistedWord(guild, channel) == True:
                    return True
                else:
                    return False

            #Convert the list back into a string by looping and adding commas after the value.
            #Check if the current_value list is empty/None and get None if it is.
            if len(current_value) > 0 and current_value != None:
                current_string = ""
                for i in current_value:
                    current_string += f"{i},"

                #Remove the final comma by including the whole string minus last character.
                new_value = current_string[:-1]

            else:
                return False
        else:
            return False

    url = "http://localhost/API/jupikd_discord/updateblacklistedwords.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "channel": channel,
        "new_value": new_value
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for inserting an entry into the server_default_command_permissions table.
async def CreateServerDefaultCommandPermission(guild, name, permission):
    #Call a post request to the API to create the permission.
    url = "http://localhost/API/jupikd_discord/createserverdefaultcommandpermission.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "name": name,
        "permission": permission
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for deleting an entry from the server_default_command_permissions table.
async def DeleteServerDefaultCommandPermission(guild, name):
    #Call a post request to the API to delete the permission.
    url = "http://localhost/API/jupikd_discord/deleteserverdefaultcommandpermission.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "name": name
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL != None and jsonURL["success"] == True:
        return True
    else:
        return False

#This function is for updating the server_default_command_permissions table.
async def UpdateServerDefaultCommandPermission(guild, name, row, new_value):
    #Don't need to get the database or anything, just send information from parameters.
    url = "http://localhost/API/jupikd_discord/updateserverdefaultcommandpermission.php"
    params = {
        "key": config.jupsapikey,
        "serverid": guild.id,
        "name": name,
        "row": row,
        "new_value": new_value
    }
    jsonURL = await functions.PostRequest(url, params)
    if jsonURL["success"] == True:
        return True
    else:
        return False