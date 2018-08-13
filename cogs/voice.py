import discord
from discord.ext import commands

import youtube_dl

import os, sys, pathlib, aiohttp, asyncio
import functions, config

class VoiceCommands:

    def __init__(self, bot):
        self.bot = bot

    #Set youtube_dl options.
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
            'preferredquality': '192',
            },
            {'key': 'FFmpegMetadata'},
        ],
    }

    #Since you cannot use await in after when playing songs, use run_coroutine_threadsafe
    def my_after(self, e, ctx, song):
        coro = ctx.send(f"Finished playing song with ID: {song}.")
        coro2 = self.NextSong(ctx, song)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        fut2 = asyncio.run_coroutine_threadsafe(coro2, self.bot.loop)
        try:
            fut.result()
            fut2.result()
        except:
            pass

    #This will deal with moving onto the next song or leaving when the queue is over.
    async def NextSong(self, ctx, last_song):
        #Delete the song that just played from the database if it's in it.
        url = "http://localhost/API/jupikd_discord/deletesongfromqueue.php"
        params = {
            "key": config.jupsapikey,
            "serverid": ctx.guild.id,
            "songid": last_song
        }
        await functions.PostRequest(url, params)

        #Get the new song queue and check if it's empty.
        song_queue = await functions.GetSongQueue(ctx.guild)

        if song_queue and "success" in song_queue:
            if song_queue["success"] == False and song_queue["error"] == "No queue.":
                await ctx.send("End of queue, leaving voice channel.")
                await ctx.voice_client.disconnect()
                return

        #Get the video info from youtube_dl.
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            song_info = ydl.extract_info(f"https://www.youtube.com/watch?v={song_queue[0]['video_id']}", download=False)

        await ctx.send(f"Playing: {song_info['title']}")
        ctx.voice_client.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"]), after=lambda e: self.my_after(e, ctx, song_queue[0]['video_id']))
        return True
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def summon(self, ctx):
        """Command which summons the bot to the members voice channel. jupikdsplit->Member"""

        if ctx.author.voice == None:
            await ctx.send("You are not in a voice channel.")
            return

        await ctx.author.voice.channel.connect()

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def stop(self, ctx):
        """Command which removes the bot from the voice channel. jupikdsplit->Member"""

        if ctx.voice_client != None:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Not connected to a voice channel.")

        url = "http://localhost/API/jupikd_discord/deleteallsongsfromqueue.php"
        params = {
            "key": config.jupsapikey,
            "serverid": ctx.guild.id
        }
        await functions.PostRequest(url, params)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def pause(self, ctx):
        """Command which pauses the currently playing music. jupikdsplit->Member"""

        if ctx.voice_client != None:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                await ctx.send("Paused the current song.")
                return

        await ctx.send("I am not playing music.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def resume(self, ctx):
        """Command which resumes the currently playing music. jupikdsplit->Member"""

        if ctx.voice_client != None:
            if not ctx.voice_client.is_playing():
                ctx.voice_client.resume()
                await ctx.send("Resumed the current song.")
                return

        await ctx.send("I am already playing music.")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def play(self, ctx, *, song):
        """Command which plays a song in a voice channel. jupikdsplit->Member"""
                
        #Check if the bot is already in a channel.
        voice_client = ctx.voice_client
        if not voice_client:
            if ctx.author.voice == None:
                await ctx.send("Neither of us are in a voice channel.")
                return

            voice_client = await ctx.author.voice.channel.connect()

        #Search for a video to play.
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": config.youtubeapikey,
            "q": song,
            "type": "video",
            "maxResults": 5,
            "part": "snippet"
        }
        jsonURL = await functions.GetRequest(url, params)

        #Check if there were no results, then return.
        if jsonURL != None:
            if jsonURL["pageInfo"]["totalResults"] < 1:
                await ctx.send(f"Couldn't find a song/video named: {song}.")
                return

        #If the amount of results was just 1, then just play that, and don't give options.
        #If it's greater, than have 5 options.
        if jsonURL["pageInfo"]["totalResults"] != 1:
            bot_prefix = await functions.GetGuildPrefix(ctx.guild.id)

            embed = await functions.CreateEmbed(
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
                title=f"Type {bot_prefix}choose [choice] to make a selection. (Number beside choice)"
            )

            for e, i in enumerate(jsonURL["items"]):
                embed.add_field(name=f"{e + 1}. {i['snippet']['channelTitle']}", value=f"{i['snippet']['title']}")

            await ctx.send(embed=embed)

            def check_message(m):
                return f"{bot_prefix}choose" in m.content and m.channel == ctx.channel and m.author == ctx.author

            try:
                await_message = await self.bot.wait_for("message", check=check_message, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.mention} Since you didn't give me a response, I will not play a song.")
                return
            else:
                try:
                    choice = int(await_message.content[-1:])
                except:
                    await ctx.send("Error, incorrect selection.")

            song = jsonURL["items"][choice - 1]["id"]["videoId"]
        else:
            song = jsonURL["items"][0]["id"]["videoId"]

        #Get the video info from youtube_dl.
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            song_info = ydl.extract_info(f"https://www.youtube.com/watch?v={song}", download=False)

        #Check if the duration is 0 (livestream) or over 600 seconds (10 minutes).
        #If not, play the song normally.
        if song_info["duration"] > 0 and song_info["duration"] <= 601:
            url = "http://localhost/API/jupikd_discord/addsongtoqueue.php"
            params = {
                "key": config.jupsapikey,
                "serverid": ctx.guild.id,
                "videoid": song
            }
            jsonURL = await functions.PostRequest(url, params)

            if jsonURL != None:
                if jsonURL["success"] == True:
                    await ctx.send(f"Added {song_info['title']} to the queue.")

            if not voice_client.is_playing():
                await ctx.send(f"Playing: {song_info['title']}")
                voice_client.play(discord.FFmpegPCMAudio(song_info["formats"][0]["url"]), after=lambda e: self.my_after(e, ctx, song))
        else:
            await ctx.send("Don't play livestreams or videos over 10 minutes.") 

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def skip(self, ctx):
        """Command which skips the currently playing music. jupikdsplit->Member"""

        ctx.voice_client.stop()

def setup(bot):
    bot.add_cog(VoiceCommands(bot))