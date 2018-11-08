import discord
from discord.ext import commands

import aiohttp, datetime, random, asyncio

import functions, config, databasefunctions

class GeneralCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def twitch(self, ctx):
        """Command which links to my twitch. jupikdsplit->Member"""

        #Send an embed with my Twitch account link.
        embed = await functions.CreateEmbed(
            description="This is the link to the owners twitch account.", 
            image="https://static-cdn.jtvnw.net/jtv_user_pictures/94ddbabc83f78038-profile_image-300x300.png", 
            author=(self.bot.user.display_name, discord.Embed.Empty, "https://static-cdn.jtvnw.net/jtv_user_pictures/twitch-profile_image-8a8c5be2e3b64a9a-300x300.png")
        )
        embed.add_field(name="Owner", value="Isaac™#1240", inline=True)
        embed.add_field(name="Link", value="[https://twitch.tv/jups](https://twitch.tv/jups)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def website(self, ctx):
        """Command which links to my website. jupikdsplit->Member"""

        #Send an embed with the main page for the website, the bot page, and the command page for the bot.
        embed = await functions.CreateEmbed(
            title="Website",
            description="This is the link to the owners website.", 
            image=self.bot.user.avatar_url_as(format="png")
        )
        embed.add_field(name="Main", value="[https://jups.xyz](https://jups.xyz)", inline=True)
        embed.add_field(name="Bot Page", value="[https://jups.xyz/discordbot](https://jups.xyz/discordbot)", inline=True)
        embed.add_field(name="Bot Commands", value="[https://jups.xyz/discordbot/commands/](https://jups.xyz/discordbot/commands/)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def github(self, ctx):
        """Command which links to the bots Github. jupikdsplit->Member"""

        #Send an embed with my username, repository name, and link to the actual repository.
        embed = await functions.CreateEmbed(
            description="This is the link to my Github page.", 
            image=self.bot.user.avatar_url_as(format="png"), 
            author=(self.bot.user.display_name, discord.Embed.Empty, "https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png")
        )
        embed.add_field(name="Username", value = "IsaacAKAJupiter")
        embed.add_field(name="Repository Name", value="JupiKD_Discord_Python", inline=True)
        embed.add_field(name="Link", value="[Github](https://github.com/IsaacAKAJupiter/JupiKD_Discord_Python)")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["guildcount", "servers", "servercount"])
    async def guilds(self, ctx):
        """Command which displays how many guilds the bot is currently in. jupikdsplit->Member"""

        #Get the amount of guilds the bot is in. (self.bot.guilds)
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png")
        )
        embed.add_field(name="Guild Count", value=len(self.bot.guilds), inline=True)
        await ctx.send(embed=embed)
  
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["commands"])
    async def commandcount(self, ctx):
        """Command which displays link to command page and amount of commands the bot currently has. jupikdsplit->Member"""

        #Get the list of non-owner commands so it's more accurate for the member.
        non_owner_commands = [command for command in self.bot.commands if command.cog_name != "OwnerCog" and command.cog_name != None]

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png")
        )
        embed.add_field(name="Command Count", value=len(non_owner_commands), inline=True)
        embed.add_field(name="Bot Commands", value="[Commands Link](https://jups.xyz/discordbot/commands/)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["checkpermission"])
    async def permissioncheck(self, ctx, command):
        """Command which displays the permission for a command. jupikdsplit->Member"""

        #Check if the member is using a command's alias, then get the actual command.
        for i in self.bot.commands:
            if command in i.aliases:
                command = i.name
        permission = await functions.GetPermissionForCommand(ctx, command)

        #If the command exists, then send an embed with the command name and the permission.
        if permission != None:
            embed = await functions.CreateEmbed(
                author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png")
            )
            embed.add_field(name="Command", value=command, inline=True)
            embed.add_field(name="Permission", value=permission, inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Command doesn't exist.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["guildinfo", "guildinformation"])
    async def guild(self, ctx):
        """Command which displays information about the current guild. jupikdsplit->Member"""

        #If the guild doesn't have an icon, then make it a Discord icon.
        if ctx.guild.icon_url != "":
            embed = await functions.CreateEmbed(
                author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png"),
                thumbnail=ctx.guild.icon_url
            )
        else:
            embed = await functions.CreateEmbed(
                author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png"),
                thumbnail="https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png"
            )
        #Get the guild name, ID, owner, members, roles, text channels, voice channels, channels with categories, and emojis for the embed.
        embed.add_field(name="Name", value=ctx.message.author.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.message.author.guild.id, inline=True)
        embed.add_field(name="Owner", value=ctx.message.author.guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=ctx.message.author.guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(ctx.message.author.guild.roles) - 1, inline=True)
        embed.add_field(name="Text Channels", value=len(ctx.message.author.guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(ctx.message.author.guild.voice_channels), inline=True)
        embed.add_field(name="Channels + Categories", value=len(ctx.message.author.guild.channels), inline=True)
        embed.add_field(name="Emojis", value=len(ctx.message.author.guild.emojis), inline=True) 
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["bot", "botinformation", "info", "information"])
    async def botinfo(self, ctx):
        """Command which displays information about the bot. jupikdsplit->Member"""

        #This gets the start time from the database, then gets the difference between the time the command was used to that.
        url = "http://localhost/API/jupikd_discord/getuptime.php"
        params = {"key": config.jupsapikey}
        jsonURL = await functions.PostRequest(url, params)
        if jsonURL != None:
            start_time = datetime.datetime.strptime(jsonURL["uptime"], "%Y-%m-%d %H:%M:%S")
            uptime = (datetime.datetime.now()) - start_time

        #Get the non-owner commands so it's more accurate for users to see how many commands.
        non_owner_commands = [command for command in self.bot.commands if command.cog_name != "OwnerCog" and command.cog_name != None]
        
        #Get the latency, uptime, creator, library, invite, website, github, commands, guilds, and members all for the embed.
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            footer=(f"Ping: {round(self.bot.latency * 1000)}ms | Uptime: {uptime.seconds // 86400} days, {uptime.seconds // 3600} hours, {(uptime.seconds % 3600) // 60} minutes, {uptime.seconds % 60} seconds.", discord.Embed.Empty)
        )
        embed.add_field(name="Creator", value="Isaac™#1240", inline=True)
        embed.add_field(name="Library", value=f"discord.py rewrite v{discord.__version__}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Invite", value="[Discord Link](https://discordapp.com/oauth2/authorize?client_id=362346139569094666&scope=bot&permissions=1275456576&redirect_uri=https://www.jups.xyz/discordbot&response_type=code)", inline=True)
        embed.add_field(name="Website", value="[Jups Link](https://jups.xyz/discordbot)", inline=True)
        embed.add_field(name="Github", value="[Github Link](https://github.com/IsaacAKAJupiter/JupiKD_Discord_Python)", inline=True)
        embed.add_field(name="Commands", value=len(non_owner_commands))
        embed.add_field(name="Guilds", value=len(self.bot.guilds))
        embed.add_field(name="Members", value=len(list(self.bot.get_all_members())))
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def invite(self, ctx):
        """Command which sends the bot invite link. jupikdsplit->Member"""

        #This command just shows a gif of how to invite the bot, with a field with the link to invite it.
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            image="https://jups.xyz/images/invite.gif"
        )
        embed.add_field(name="Click the link below to invite me to your guild!", value="[Discord Invite Link](https://discordapp.com/oauth2/authorize?client_id=362346139569094666&scope=bot&permissions=1275456576&redirect_uri=https://www.jups.xyz/discordbot&response_type=code)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["ping"])
    async def latency(self, ctx):
        """Command which gets the latency of the bot. jupikdsplit->Member"""

        #Use the built-in latency test for discord.py, then turn it into milliseconds.
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Response", value="Latency Test", inline=True)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["mods"])
    async def moderators(self, ctx):
        """Command which displays all the mods in the channel. jupikdsplit->Member"""

        #Call a function to get all the member objects for the column moderators for the guild.
        #Turn them into a string of mentions.
        members = await functions.GetMemberObjects(ctx.guild, "moderators")
        mentions = ""

        if members != None:
            for member in members:
                mentions += f"{member.mention}, "
        else:
            await ctx.send("There are no mods.")
            return
        
        mentions = mentions[:-2]

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Moderators", value=mentions, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["admins"])
    async def administrators(self, ctx):
        """Command which displays all the admins in the channel. jupikdsplit->Member"""

        #Call a function to get all the member objects for the column admins for the guild.
        #Turn them into a string of mentions.
        members = await functions.GetMemberObjects(ctx.guild, "admins")
        mentions = ""

        if members != None:
            for member in members:
                mentions += f"{member.mention}, "
        else:
            await ctx.send("There are no admins.")
            return
        
        mentions = mentions[:-2]

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Administrators", value=mentions, inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["topten", "topcommands"])
    async def top10(self, ctx):
        """Command which displays the top 10 commands by usage. jupikdsplit->Member"""

        #Call my api to get the top 10 used commands.
        url = "http://localhost/API/jupikd_discord/top10usedcommands.php"
        params = {
            "key": config.jupsapikey
        }
        json = await functions.PostRequest(url, params)
        
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )

        #Every even number becomes a blank field, to make the embed look better.
        count = 1
        if not "success" in json:
            for i in json:
                if count % 2 == 0:
                    embed.add_field(name="\u200b", value="\u200b", inline=True)
                embed.add_field(name=i["name"], value=f"Uses: {i['uses']}", inline=True)
                count += 1

        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["discordavatar"])
    async def avatar(self, ctx, member = None):
        """Command which shows the avatar of a member. jupikdsplit->Member"""

        #Use this variable to get the member object.
        #If you mentioned a user, then get their object.
        #If you used an int, get_member with the ID.
        #If you used a name, then use functions.GetMemberByName
        #If all failed, use the author.
        actual_member = None

        if len(ctx.message.mentions) > 0:
            actual_member = ctx.message.mentions[0]
        
        if actual_member == None and member != None:
            try:
                member = int(member)
            except Exception:
                actual_member = await functions.GetMemberByName(ctx.guild, member)
            else:
                actual_member = ctx.guild.get_member(member)

        if actual_member == None:
            actual_member = ctx.author

        try:
            image = actual_member.avatar_url_as(format="gif")
        except Exception:
            image = actual_member.avatar_url_as(format="png")

        embed = await functions.CreateEmbed(
            title=f"Avatar links for {actual_member.name}",
            description=f"[jpg]({actual_member.avatar_url_as(format='jpg')}) [jpeg]({actual_member.avatar_url_as(format='jpeg')}) [png]({actual_member.avatar_url_as(format='png')}) [webp]({actual_member.avatar_url_as(format='webp')})",
            image=image
        )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def spotify(self, ctx, member = None):
        """Command which shows the spotify information of a member. jupikdsplit->Member"""

        #Use this variable to get the member object.
        #If you mentioned a user, then get their object.
        #If you used an int, get_member with the ID.
        #If you used a name, then use functions.GetMemberByName
        #If all failed, use the author.
        actual_member = None

        if len(ctx.message.mentions) > 0:
            actual_member = ctx.message.mentions[0]
        
        if actual_member == None and member != None:
            try:
                member = int(member)
            except Exception:
                actual_member = await functions.GetMemberByName(ctx.guild, member)
            else:
                actual_member = ctx.guild.get_member(member)

        if actual_member == None:
            actual_member = ctx.author

        if actual_member.activity == None:
            await ctx.send("Member is not listening to spotify.")
            return

        if actual_member.activity.type == discord.ActivityType.listening:
            embed = await functions.CreateEmbed(
                title=f"Spotify Information for {actual_member.name}",
                image=actual_member.activity.album_cover_url
            )

            #Get the actual artists, instead of just 1 artist.
            artists = actual_member.activity.artists
            artists_str = ""
            for artist in artists:
                artists_str += f"{artist}, "
            artists_str = artists_str[:-2]

            #Dealing with song duration.
            duration = actual_member.activity.duration.total_seconds()
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)

            #Check if seconds is less than 10 so it shows 3:09 instead of 3:9
            if seconds < 10:
                seconds = str(f"0{seconds}")
            #Check if the song is longer than an hour so it can show time with hours.
            if hours < 1:
                duration_value = f"{minutes}:{seconds}"
            else:
                duration_value = f"{hours}:{minutes}:{seconds}"
            
            #Add the embed fields.
            embed.add_field(name="Song Name", value=actual_member.activity.title)
            embed.add_field(name="Artists", value=artists_str)
            embed.add_field(name="Album", value=actual_member.activity.album)
            embed.add_field(name="Duration", value=duration_value)
            await ctx.send(embed=embed)
            return

        await ctx.send("Member is not listening to spotify. (or they aren't in the guild.)")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["guildmemberinfo"])
    async def guildmembers(self, ctx):
        """Command which shows the guild member information. jupikdsplit->Member"""

        #Everything is in the context object, so just create the embed right away and fill with 1 line lists.
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            thumbnail=ctx.message.author.guild.icon_url_as(format="png")
        )
        embed.add_field(name="People", value=len([m for m in ctx.message.author.guild.members if m.bot is False]))
        embed.add_field(name="Bots", value=len([m for m in ctx.message.author.guild.members if m.bot is True]))
        embed.add_field(name="Members Online", value=len([m for m in ctx.message.author.guild.members if m.status is not discord.Status.offline]))
        embed.add_field(name="Total", value=ctx.message.author.guild.member_count)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def steam(self, ctx, steamuser):
        """Command which shows the steam information for a user. jupikdsplit->Member"""

        #Check if the member is using a customURL and then turn it into an ID.
        url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
        params = {
            "key": config.steamapikey,
            "vanityurl": steamuser
        }
        jsonURL = await functions.GetRequest(url, params)

        if jsonURL != None:
            if "steamid" in jsonURL["response"]:
                steamuser = jsonURL["response"]["steamid"]

        #Get the player summaries/user information from another steam API via ID.
        url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
        params = {
            "key": config.steamapikey,
            "steamids": steamuser
        }
        jsonURL = await functions.GetRequest(url, params)
       
        #Make an embed with the information from the API if a user was found.
        if len(jsonURL["response"]["players"]) > 0:
            embed = await functions.CreateEmbed(
                title="Steam Profile",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
                image=jsonURL["response"]["players"][0]["avatarfull"]
            )
            embed.add_field(name="Name", value=jsonURL["response"]["players"][0]["personaname"], inline=True)
            embed.add_field(name="Last Logoff", value=datetime.datetime.fromtimestamp(int(jsonURL["response"]["players"][0]["lastlogoff"])).strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.set_footer(text=f"Profile Link: {jsonURL['response']['players'][0]['profileurl']}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Steam user not found. You can use CustomURL or Steam64ID.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["cinfo", "chelp", "commandhelp"])
    async def commandinfo(self, ctx, command):
        """Command which shows information about a command. jupikdsplit->Member"""

        #Check if the member searched for an alias of a command.
        for i in self.bot.commands:
            if command in i.aliases or command == i.name:
                command = i

        if isinstance(command, str):
            await ctx.send(f"Cannot find command: \"{command}\".")
            return

        #Get the current permission and uses.
        current_permission = await functions.GetPermissionForCommand(ctx, command.name)
        uses = await functions.GetDefaultCommandPermissions()
        for i in uses:
            if i["name"] == command.name:
                uses = i["uses"]

        desc_permission = command.help.split(" jupikdsplit->")
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )
        embed.add_field(name="Command", value=command.name, inline=False)
        embed.add_field(name="Description", value=desc_permission[0], inline=False)
        embed.add_field(name="Default Permission", value=desc_permission[1], inline=True)
        embed.add_field(name="Current Permission", value=current_permission, inline=True)
        embed.add_field(name="Uses", value=uses, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))