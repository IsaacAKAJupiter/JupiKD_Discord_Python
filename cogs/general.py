import discord
from discord.ext import commands

import aiohttp, datetime

import functions, config, databasefunctions

class GeneralCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def twitch(self, ctx):
        """Command which links to my twitch."""

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
        """Command which links to my website."""

        embed = await functions.CreateEmbed(
            title="Website",
            description="This is the link to the owners website.", 
            image=self.bot.user.avatar_url_as(format="png"), 
            url="https://twitch.tv/jups",
        )
        embed.add_field(name="[WIP] Root", value="[https://jups.xyz](https://jups.xyz)", inline=True)
        embed.add_field(name="[WIP] Bot Page", value="[https://jups.xyz/JupiKD_Discord](https://jups.xyz/JupiKD_Discord)", inline=True)
        embed.add_field(name="[WIP] Bot Commands", value="[https://jups.xyz/JupiKD_Discord/commands/](https://jups.xyz/JupiKD_Discord/commands/)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def github(self, ctx):
        """Command which links to the bots Github."""

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
        """Command which displays how many guilds the bot is currently in."""

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png")
        )
        embed.add_field(name="Guild Count", value=len(self.bot.guilds), inline=True)
        await ctx.send(embed=embed)
  
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["commands"])
    async def commandcount(self, ctx):
        """Command which displays link to command page and amount of commands the bot currently has."""

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, "https://cdn-images-1.medium.com/max/230/1*OoXboCzk0gYvTNwNnV4S9A@2x.png")
        )
        embed.add_field(name="Command Count", value=len(self.bot.commands), inline=True)
        embed.add_field(name="Bot Commands", value="[Commands Link](https://jups.xyz/JupiKD_Discord/commands/)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["checkpermission"])
    async def permissioncheck(self, ctx, command):
        """Command which displays the permission for a command."""

        for i in self.bot.commands:
            if command in i.aliases:
                command = i.name
        permission = await functions.GetPermissionForCommand(ctx, command)

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
        """Command which displays information about the current guild."""

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
        embed.add_field(name="Name", value=ctx.message.author.guild.name, inline=True)
        embed.add_field(name="ID", value=ctx.message.author.guild.id, inline=True)
        embed.add_field(name="Owner", value=ctx.message.author.guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=ctx.message.author.guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(ctx.message.author.guild.roles) - 1, inline=True)
        embed.add_field(name="Text Channels", value=len(ctx.message.author.guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(ctx.message.author.guild.voice_channels), inline=True)
        embed.add_field(name="Text Channels", value=len(ctx.message.author.guild.text_channels), inline=True)
        embed.add_field(name="Channels + Categories", value=len(ctx.message.author.guild.channels), inline=True)
        embed.add_field(name="Emojis", value=len(ctx.message.author.guild.emojis), inline=True) 
        await ctx.send(embed=embed)
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["bot", "botinformation", "info", "information"])
    async def botinfo(self, ctx):
        """Command which displays information about the bot."""

        start_time = datetime.datetime.strptime(config.start_time, "%Y-%m-%d %H:%M:%S")
        uptime = (datetime.datetime.now()) - start_time

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            footer=(f"Ping: {round(self.bot.latency * 1000)}ms | Uptime: {uptime.seconds // 86400} days, {uptime.seconds // 3600} hours, {(uptime.seconds % 3600) // 60} minutes, {uptime.seconds % 60} seconds.", discord.Embed.Empty)
        )
        embed.add_field(name="Creator", value="Isaac™#1240", inline=True)
        embed.add_field(name="Library", value=f"discord.py rewrite v{discord.__version__}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Invite", value="[Discord Link](https://discordapp.com/oauth2/authorize?client_id=362346139569094666&scope=bot&permissions=2146958591)", inline=True)
        embed.add_field(name="Website", value="[Jups Link](https://jups.xyz/JupiKD_Discord)", inline=True)
        embed.add_field(name="Github", value="[Github Link](https://github.com/IsaacAKAJupiter/JupiKD_Discord_Python)", inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands))
        embed.add_field(name="Guilds", value=len(self.bot.guilds))
        embed.add_field(name="Members", value=len(list(self.bot.get_all_members())))
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def invite(self, ctx):
        """Command which sends the bot invite link."""

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
            image="https://jups.xyz/cgi-bin/invite.gif"
        )
        embed.add_field(name="Click the link below to invite me to your guild!", value="[Discord Invite Link](https://discordapp.com/oauth2/authorize?client_id=362346139569094666&scope=bot&permissions=2146958591)", inline=True)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["ping"])
    async def latency(self, ctx):
        """Command which gets the latency of the bot."""

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
        """Command which displays all the mods in the channel."""

        members = await functions.GetMemberObjects(ctx.guild, "moderators")
        mentions = ""
        for member in members:
            mentions += f"{member.mention}, "
        
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
        """Command which displays all the admins in the channel."""

        members = await functions.GetMemberObjects(ctx.guild, "admins")
        mentions = ""
        for member in members:
            mentions += f"{member.mention}, "
        
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
        """Command which displays the top 10 commands by usage."""

        url = "http://localhost/API/jupikd_discord/top10usedcommands.php"
        params = {
            "key": config.jupsapikey
        }
        json = await functions.PostRequest(url, params)
        
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )

        count = 1
        if not "success" in json:
            for i in json:
                if count % 2 == 0:
                    embed.add_field(name="\u200b", value="\u200b", inline=True)
                embed.add_field(name=i["name"], value=f"Uses: {i['uses']}", inline=True)
                count += 1

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))