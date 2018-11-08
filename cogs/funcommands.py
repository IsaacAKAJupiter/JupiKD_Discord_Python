import discord
from discord.ext import commands

import aiohttp, random, emoji

import functions, config, databasefunctions

class FunCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["ud"])
    async def urbandictionary(self, ctx, *, word):
        """Command which searches up a definition on UrbanDictionary. jupikdsplit->Member"""

        #Use the urbandictionary API and search the word the member specified.
        #Display in an embed.
        url = "http://api.urbandictionary.com/v0/define"
        params = {
            "term": word
        }
        jsonURL = await functions.GetRequest(url, params)

        if jsonURL != None:
            if len(jsonURL["list"]) > 0:
                embed = await functions.CreateEmbed(
                    title="Urban Dictionary Word Lookup",
                    author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
                )
                embed.add_field(name="Word", value=word, inline=True)
                embed.add_field(name="Definition", value=jsonURL["list"][0]["definition"], inline=True)
                embed.add_field(name="Author", value=jsonURL["list"][0]["author"], inline=True)
                embed.add_field(name="Example", value=jsonURL["list"][0]["example"], inline=True)
                embed.add_field(name="Link", value=jsonURL["list"][0]["permalink"], inline=True)
                await ctx.send(embed=embed)
                return
            
        await ctx.send("No results.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["lemoji"])
    async def largeemoji(self, ctx, emojit):
        """Command which gets the actual image of the custom emoji. jupikdsplit->Member"""          

        #Check if they used a unicode emoji.
        for i in emojit:
            if i in emoji.UNICODE_EMOJI:
                await ctx.send(emojit)
                return

        emoji_id, emoji_extension, emoji_name = await functions.GetEmojiFromMessage(emojit)
        if not emoji_id or not emoji_extension or not emoji_name:
            #Check if the person just used an emoji_id.
            emoji_name = emojit
            try:
                emojit = int(emojit)
            except:
                await ctx.send("Emoji not found.")
                return

            #Try for GIF.
            url = f"https://cdn.discordapp.com/emojis/{emojit}.gif"
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as resp:
                    if resp.status != 415:
                        emoji_id = emojit
                        emoji_extension = "gif"
                    session.close()

            #Try for PNG.
            if not emoji_id and not emoji_extension:
                url = f"https://cdn.discordapp.com/emojis/{emojit}.png"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=url) as resp:
                        if resp.status != 415:
                            emoji_id = emojit
                            emoji_extension = "png"
                        session.close()

            if not emoji_id and not emoji_extension:
                await ctx.send("Emoji not found.")
                return

        embed = await functions.CreateEmbed(
            title="Large Emoji",
            description = f"Name/ID = {emoji_name}",
            image=f"https://cdn.discordapp.com/emojis/{emoji_id}.{emoji_extension}",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["regionalindicators", "ritext"])
    async def bigtext(self, ctx, *, message):
        """Command which mimics a message with regional indicators. jupikdsplit->Member"""

        #Check if the member is mentioning someone to make their last message in regional indicators.
        if len(ctx.message.mentions) > 0:
            message_obj = await functions.MemberLatestMessage(ctx.channel, ctx.message.mentions[0])
            if message_obj != None:
                message = message_obj.content

        #Make a list of characters that are able to be changed to regional indicators.
        allowed_characters = "abcdefghijklmnopqrstuvwxyz"

        regional_text_string = ""
        for letter in message:
            letter = letter.lower()
            #If the letter isn't an allowed character, check if it is a question mark or exclaimation mark to use another type of emoji.
            #Else, just use a normal character.
            if letter != " " and letter in allowed_characters:
                regional_text_string += f":regional_indicator_{letter}: "
            elif letter == "?":
                regional_text_string += ":grey_question:"
            elif letter == "!":
                regional_text_string += ":grey_exclamation:"
            elif letter == " ":
                regional_text_string += "  "
            else:
                regional_text_string += letter

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Original Text", value=message, inline=False)
        embed.add_field(name="Regional Indicators", value=regional_text_string, inline=False)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["fullcapitals"])
    async def fullcaps(self, ctx, *, message):
        """Command which mimics a message with full capital letters. jupikdsplit->Member"""

        #Check if the member is mentioning someone to transform their latest message into full caps.
        if len(ctx.message.mentions) > 0:
            message_obj = await functions.MemberLatestMessage(ctx.channel, ctx.message.mentions[0])
            if message_obj != None:
                message = message_obj.content

        #The upper function just makes every character an uppercase letter.
        caps_message = message.upper()

        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Original Text", value=message, inline=False)
        embed.add_field(name="Full Caps", value=caps_message, inline=False)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["mock"])
    async def mixedcaps(self, ctx, *, message):
        """Command which mocks a message with mixed capital letters. jupikdsplit->Member"""

        #Check if the member is mentioning someone to mock.
        if len(ctx.message.mentions) > 0:
            message_obj = await functions.MemberLatestMessage(ctx.channel, ctx.message.mentions[0])
            if message_obj != None:
                message = message_obj.content
                    
        #Since random.random() does from 0-1, make uppercase/lowercase either above or below 0.50.
        mixed_caps_string = ""
        for letter in message:
            random_number = random.random()
            if random_number < 0.50:
                mixed_caps_string += letter.lower()
            else:
                mixed_caps_string += letter.upper()

        #Should be mixed up, make the embed with original and new messages.
        embed = await functions.CreateEmbed(
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
        )
        embed.add_field(name="Original Text", value=message, inline=False)
        embed.add_field(name="Mixed Caps", value=mixed_caps_string, inline=False)
        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["rsub"])
    async def rsrandom(self, ctx, sub):
        """Command which gets a random post from a chosen subreddit. jupikdsplit->Member"""

        jsonURL, image = await functions.RedditPost(ctx, sub, "random")
        if jsonURL == None and image == None:
            await ctx.send("Subreddit not found.")
            return

        if jsonURL == "NSFW":
            await ctx.send("The random selection was NSFW, and you are not in an NSFW allowed channel.")
            return

        #embed = await functions.RedditDefaultEmbed(jsonURL, image, self.bot)
        await ctx.send(f"Image/Gif: {image}\nReddit Link: https://reddit.com{jsonURL['data']['children'][0]['data']['permalink']}\nI can't use embeds for GIF's since they are lower quality :angry:")
        #await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["rrandom"])
    async def redditrandom(self, ctx):
        """Command which gets a random post from a random subreddit. jupikdsplit->Member"""

        jsonURL, image = await functions.RedditPost(ctx, "random", "random")
        if jsonURL == None and image == None:
            await ctx.send("Subreddit not found.")
            return

        if jsonURL == "NSFW":
            await ctx.send("The random selection was NSFW, and you are not in an NSFW allowed channel.")
            return

        #embed = await functions.RedditDefaultEmbed(jsonURL, image, self.bot)
        await ctx.send(f"Image/Gif: {image}\nReddit Link: https://reddit.com{jsonURL['data']['children'][0]['data']['permalink']}\nI can't use embeds for GIF's since they are lower quality :angry:")
        #await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["rsubtop"])
    async def subtop(self, ctx, sub):
        """Command which gets the top post from a chosen subreddit. jupikdsplit->Member"""

        jsonURL, image = await functions.RedditPost(ctx, sub, "top", "?t=all")
        if jsonURL == None and image == None:
            await ctx.send("Subreddit not found.")
            return

        if jsonURL == "NSFW":
            await ctx.send("The random selection was NSFW, and you are not in an NSFW allowed channel.")
            return

        #embed = await functions.RedditDefaultEmbed(jsonURL, image, self.bot)
        await ctx.send(f"Image/Gif: {image}\nReddit Link: https://reddit.com{jsonURL['data']['children'][0]['data']['permalink']}\nI can't use embeds for GIF's since they are lower quality :angry:")
        #await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCommands(bot))