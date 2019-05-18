import discord
from discord.ext import commands

import aiohttp, re, asyncio

import functions, config, databasefunctions

class AdminCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["moderator"])
    async def mod(self, ctx):
        """Command which makes a member a moderator. jupikdsplit->Admin"""

        if len(ctx.message.mentions) > 0:
            new_value = ctx.message.mentions[0]
        else:
            new_value = ctx.author

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "moderators", add=True, new_value=new_value.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="New Mod Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Mod Denied",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        embed.add_field(name="Mod Mention", value=new_value.mention, inline=True)
        embed.add_field(name="Mod ID", value=new_value.id, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["unmoderator"])
    async def unmod(self, ctx):
        """Command which removes a member from moderators. jupikdsplit->Admin"""

        if len(ctx.message.mentions) > 0:
            new_value = ctx.message.mentions[0]
        else:
            new_value = ctx.author

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "moderators", add=False, new_value=new_value.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="Removed Mod Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="Removed Mod Denied",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        embed.add_field(name="Mod Mention", value=new_value.mention, inline=True)
        embed.add_field(name="Mod ID", value=new_value.id, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["botprefix", "changeprefix"])
    async def prefix(self, ctx, prefix):
        """Command which changes the bots prefix for the guild. jupikdsplit->Admin"""

        #Don't need to check the new prefix length since its going to just fail if it's over.
        #Get current prefix.
        current_prefix = await functions.GetGuildPrefix(ctx.guild.id)

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "bot_prefix", add=False, new_value=prefix, old_value=current_prefix) == True:
            embed = await functions.CreateEmbed(
                title="New Prefix Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Prefix Denied.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )

        new_prefix = await functions.GetGuildPrefix(ctx.guild.id)

        embed.add_field(name="Old Prefix", value=current_prefix, inline=True)
        embed.add_field(name="New Prefix", value=new_prefix, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["autorole"])
    async def joinrole(self, ctx, *, role):
        """Command which gives a member a role upon joining the guild. jupikdsplit->Admin"""

        role_object = None

        if len(ctx.message.role_mentions) > 0:
            role_object = ctx.message.role_mentions[0]
        
        if role_object == None:
            role_object = [r for r in ctx.guild.roles if r.name == role]
            if len(role_object) < 1:
                role_object = [r for r in ctx.guild.roles if str(r.id) == role]
                if len(role_object) < 1:
                    await ctx.send("No role found.")
                    return
            role_object = role_object[0]

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "join_role", add=True, new_value=role_object.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="New Join Role Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Join Role Denied.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        embed.add_field(name="Role Name", value=role_object.name)
        embed.add_field(name="Role ID", value=role_object.id)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["removeautorole"])
    async def removejoinrole(self, ctx):
        """Command which removes the join role. jupikdsplit->Admin"""

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "join_role", add=True, new_value=None, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="Remove Join Role Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("An error occured when trying to remove the join role from the database. Please try again.")
            return

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def ban(self, ctx, member, *, reason = None):
        """Command which bans a member from the guild. jupikdsplit->Admin"""

        #Check if the author mentioned a member.
        if len(ctx.message.mentions) < 1:
            await ctx.send("You need to mention a member to ban.")
            return
        
        #Check if the member being banned is higher/same rank as the author.
        if await functions.CheckHigherPermission(ctx, ctx.author, ctx.message.mentions[0]) == False:
            await ctx.send("You cannot kick someone of a higher rank.")
            return

        #Use a try except since the bot might error trying to ban a member it can't.
        try:
            await ctx.message.mentions[0].ban(reason=reason)
        except Exception:
            await ctx.send(f"I do not have the privilege to ban {ctx.message.mentions[0].name}. (You might be trying to ban yourself...)")
            return

        embed = await functions.CreateEmbed(
            title="Ban",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )

        embed.add_field(name="Admin", value=ctx.author.mention, inline=True)
        embed.add_field(name="Member Banned", value=f"__{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}__", inline=True)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        try:
            await ctx.message.mentions[0].send(f"You have been banned from the guild \"{ctx.guild.name}\" with the reason: \"{reason}\".")
        except:
            pass

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def hardban(self, ctx, member, *, reason = None):
        """Command which bans a member from the guild and removes 7 days worth of messages. jupikdsplit->Admin"""

        #Check if the author mentioned a member.
        if len(ctx.message.mentions) < 1:
            await ctx.send("You need to mention a member to hardban.")
            return
        
        #Check if the member being banned is higher/same rank as the author.
        if await functions.CheckHigherPermission(ctx, ctx.author, ctx.message.mentions[0]) == False:
            await ctx.send("You cannot kick someone of a higher rank.")
            return

        #Use a try except since the bot might error trying to ban a member it can't.
        try:
            await ctx.message.mentions[0].ban(reason=reason, delete_message_days=7)
        except Exception:
            await ctx.send(f"I do not have the privilege to ban {ctx.message.mentions[0].name}. (You might be trying to ban yourself...)")
            return

        embed = await functions.CreateEmbed(
            title="Ban",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )

        embed.add_field(name="Admin", value=ctx.author.mention, inline=True)
        embed.add_field(name="Member Banned", value=f"__{ctx.message.mentions[0].name}#{ctx.message.mentions[0].discriminator}__", inline=True)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        try:
            await ctx.message.mentions[0].send(f"You have been banned from the guild \"{ctx.guild.name}\" with the reason: \"{reason}\".")
        except:
            pass

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def unban(self, ctx, member_id, *, reason = None):
        """Command which unbans a member from the guild. jupikdsplit->Admin"""

        member_object = await self.bot.get_user_info(int(member_id))

        if member_object == None:
            await ctx.send("There is no member with the ID sent.")
            return

        for ban in await ctx.guild.bans():
            if ban.user.id == member_object.id:
                await ctx.guild.unban(member_object, reason=reason)
                await ctx.send(f"Unbanned {member_object.name} from the guild.")
                return
        
        await ctx.send("There is no member banned with that ID.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["setmutedrole"])
    async def mutedrole(self, ctx, role):
        """Command which sets the guild's muted role. jupikdsplit->Admin"""

        role_object = None

        if len(ctx.message.role_mentions) > 0:
            role_object = ctx.message.role_mentions[0]
        
        if role_object == None:
            role_object = [r for r in ctx.guild.roles if r.name == role]
            if len(role_object) < 1:
                role_object = [r for r in ctx.guild.roles if str(r.id) == role]
                if len(role_object) < 1:
                    await ctx.send("No role found.")
                    return
            role_object = role_object[0]

        if await databasefunctions.UpdateDatabase(ctx.guild, "server", "muted_role", add=True, new_value=role_object.id, old_value=None) == True:
            embed = await functions.CreateEmbed(
                title="New Muted Role Success.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        else:
            embed = await functions.CreateEmbed(
                title="New Muted Role Denied.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            )
        embed.add_field(name="Role Name", value=role_object.name)
        embed.add_field(name="Role ID", value=role_object.id)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["createmuterole"])
    async def createmutedrole(self, ctx, colour = None, *, name = "Muted"):
        """Command which sets the guild's muted role. jupikdsplit->Admin"""

        default_muted_colour = "#030303"

        if colour == None:
            colour = default_muted_colour

        original_hex = colour

        if colour.startswith("#"):
            colour = colour[1:]

        if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', colour):
            await ctx.send(f"The HEX Colour Code of {original_hex} is invalid, using the default value of {default_muted_colour}.")
            colour = default_muted_colour[1:]
            original_hex = default_muted_colour

        actual_hex_colour = int(colour, 16)
        permissions = discord.Permissions()
        permissions.use_voice_activation = True
        permissions.read_message_history = True
        permissions.read_messages = True
        muted_role = await ctx.guild.create_role(name=name, permissions=permissions, colour=discord.Colour(actual_hex_colour))

        for channels in ctx.guild.text_channels:
            await channels.set_permissions(muted_role, send_messages=False)

        await ctx.send(f"I have created the role {muted_role.name} with the colour {original_hex}. I also changed the permissions in the channels I had access to to not allow them to send messages. The only thing that might be a problem is that you cannot change the position of the role on the hierarchy. This means the role is situated above the everybody role and if you wanted to mute a role above this, it would not work for certain channels. Move the role higher if needed.")
        await databasefunctions.UpdateDatabase(ctx.guild, "server", "muted_role", add=True, new_value=muted_role.id, old_value=None)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def changepermission(self, ctx, command, *, permission):
        """Command which changes the permission for a command. jupikdsplit->Admin"""

        #Check if the command exists.
        if await functions.CommandExist(self.bot, command) == False:
            await ctx.send(f"The command {command} does not exist.")
            return

        if permission == "Owner" or permission == "Admin" or permission == "Mod" or permission == "Member":
            is_normal_permission = True
        else:
            is_normal_permission = False
        
        custom_permissions = await functions.GetGuildInfo(ctx.guild, "custom_permissions")
        is_custom_permission = False
        if custom_permissions != None:
            for i in custom_permissions:
                if i["name"] == permission:
                    is_custom_permission = True

        if is_custom_permission == False and is_normal_permission == False:
            await ctx.send("The permission needs to be Admin, Mod, Owner, Member or a custom permission.")
            return
        
        await databasefunctions.DeleteServerDefaultCommandPermission(ctx.guild, command)
        await databasefunctions.CreateServerDefaultCommandPermission(ctx.guild, command, permission)
        await ctx.send(f"Changed permission for {command} to {permission}.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def resetpermission(self, ctx, command):
        """Command which resets the permission for a command. jupikdsplit->Admin"""

        #Check if the command exists.
        if await functions.CommandExist(self.bot, command) == False:
            await ctx.send(f"The command {command} does not exist.")
            return

        await databasefunctions.DeleteServerDefaultCommandPermission(ctx.guild, command)
        await ctx.send(f"Reset permission for {command}.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def createrole(self, ctx, colour, *, name):
        """Command which creates a role with the given colour and name. jupikdsplit->Admin"""

        def check_message(m):
            return m.content.lower() == "yes" or m.content.lower() == "no" and m.channel == ctx.channel and m.author == ctx.author

        original_hex = colour

        if colour.startswith("#"):
            colour = colour[1:]

        if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', colour):
            await ctx.send(f"The HEX Colour Code of {original_hex} is invalid, please use a valid HEX Colour Code. Example: #42d9f4")
            return

        actual_hex_colour = int(colour, 16)
        hoist = False
        mentionable = False
        await ctx.send("Would you like this role to be displayed seperately in the member list (hoist)? yes/no")
        try:
            await_message = await self.bot.wait_for("message", check=check_message, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Since you didn't answer, this role will not be displayed seperately.")
        else:
            if await_message.content.lower() == "yes":
                hoist = True

        await ctx.send("Would you like this role to be mentionable? yes/no")
        try:
            await_message = await self.bot.wait_for("message", check=check_message, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Since you didn't answer, this role will not be displayed seperately.")
        else:
            if await_message.content.lower() == "yes":
                mentionable = True

        await ctx.guild.create_role(name=name, colour=discord.Colour(actual_hex_colour), hoist=hoist, mentionable=mentionable)
        embed = await functions.CreateEmbed(
            title="Create Role",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Role Name", value=name)
        embed.add_field(name="Role Colour", value=original_hex)
        embed.add_field(name="Displayed Seperately", value=hoist)
        embed.add_field(name="Mentionable", value=mentionable)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["createcustomemoji"])
    async def createemoji(self, ctx, name, image = None):
        """Command which creates a custom emoji for the guild. jupikdsplit->Admin"""

        async def get_request(url):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        read = await resp.read()
                        session.close()
                        return read
            except Exception:
                return None

        #Check if the name is over 2 characters.
        if len(name) < 2:
            await ctx.send("The name of the emoji needs to be at least 2 characters.")
            return

        if len(ctx.message.attachments) > 0:
            image = await get_request(ctx.message.attachments[0].url)
        else:
            image = await get_request(image)
            
        if image == None:
            await ctx.send("You didn't send an image attachment and your link was either blank or not a link to an image.")
            return False

        if type(image) != bytes:
            image = image.tobytes()

        try:
            emoji = await ctx.guild.create_custom_emoji(name=name, image=image)
        except Exception:
            await ctx.send("Either you provided an image with a file not supported or the image was too large. Supported image extensions are .png, .jpg, and .jpeg.")
            return
        
        embed = await functions.CreateEmbed(
            title="Create Custom Emoji",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            image=emoji.url
        )
        embed.add_field(name="Emoji Name", value=f":{emoji.name}:")
        embed.add_field(name="Emoji ID", value=emoji.id)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["deleteemoji"])
    async def removeemoji(self, ctx, emoji):
        """Command which deletes a custom emoji from the guild. jupikdsplit->Admin"""

        #Since custom emojis cannot have "<" or ">" in their name, we can check if it is a custom emoji with this.
        #Get the ID by getting the colons then from the last colon to the end should be the name (+1 | -1)
        if "<" in emoji and ">" in emoji:
            colons = [e for e, chars in enumerate(emoji) if chars == ":"]
            emoji_id = emoji[colons[1] + 1: -1]
        else:
            await ctx.send("Please use the actual emoji to delete it.")
            return

        emoji_object = discord.utils.find(lambda e: e.id == int(emoji_id), ctx.guild.emojis)

        if emoji_object == None:
            await ctx.send("Couldn't find the emoji specified.")
            return

        try:
            await emoji_object.delete()
        except Exception:
            await ctx.send("I do not have permission to delete this emoji.")
            return

        embed = await functions.CreateEmbed(
            title="Delete Custom Emoji",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            image=emoji_object.url
        )
        embed.add_field(name="Emoji Name", value=f":{emoji_object.name}:")
        embed.add_field(name="Emoji ID", value=emoji_object.id)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def blacklist(self, ctx, word):
        """Command which blacklists a word for specific channel(s) for a guild. jupikdsplit->Admin"""

        #Set the channels object so I don't have to make 2 seperate loops.
        if len(ctx.message.channel_mentions) > 0:
            channels = ctx.message.channel_mentions
        else:
            channels = ctx.guild.text_channels

        #Make a channels string so I can put it into the embed later.
        channels_string = ""

        #Loop through channels object and set the blacklisted word.
        for channel in channels:
            await databasefunctions.CreateBlacklistedWord(ctx.guild, channel.id)
            await databasefunctions.UpdateBlacklistedWord(ctx.guild, channel.id, True, word)
            channels_string += f"#{channel.name}, "

        channels_string = channels_string[:-2]

        #Send the embed.
        embed = await functions.CreateEmbed(
            title="Blacklist Word",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )
        embed.add_field(name="Word", value=word)
        embed.add_field(name="Channels", value=channels_string)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def unblacklist(self, ctx, word):
        """Command which unblacklists a word for specific channel(s) for a guild. jupikdsplit->Admin"""

        #Set the channels object so I don't have to make 2 seperate loops.
        if len(ctx.message.channel_mentions) > 0:
            channels = ctx.message.channel_mentions
        else:
            channels = ctx.guild.text_channels

        #Make a channels string so I can put it into the embed later.
        channels_string = ""

        #Loop through channels object and set the blacklisted word.
        for channel in channels:
            await databasefunctions.UpdateBlacklistedWord(ctx.guild, channel.id, False, word)
            channels_string += f"#{channel.name}, "

        channels_string = channels_string[:-2]

        #Send the embed.
        embed = await functions.CreateEmbed(
            title="Unblacklist Word",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )
        embed.add_field(name="Word", value=word)
        embed.add_field(name="Channels", value=channels_string)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def unblacklistall(self, ctx, channels = None):
        """Command which unblacklists all words for specific channel(s) for a guild. jupikdsplit->Admin"""

        #Set the channels object so I don't have to make 2 seperate loops.
        if len(ctx.message.channel_mentions) > 0:
            channels = ctx.message.channel_mentions
        else:
            channels = ctx.guild.text_channels

        #Make a channels string so I can put it into the embed later.
        channels_string = ""

        #Loop through channels object and set the blacklisted word.
        for channel in channels:
            await databasefunctions.DeleteBlacklistedWord(ctx.guild, channel.id)
            channels_string += f"#{channel.name}, "

        channels_string = channels_string[:-2]

        #Send the embed.
        embed = await functions.CreateEmbed(
            title="Unblacklist All Words",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )
        embed.add_field(name="Channels", value=channels_string)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCommands(bot))