import discord
from discord.ext import commands

import aiohttp, requests

import functions, config, databasefunctions

class UtilCommands():
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["scan"])
    async def virustotal(self, ctx, link):
        """Command which scans links with VirusTotal. jupikdsplit->Member"""

        #Send a post request to the virustotal API.
        url = "http://www.virustotal.com/vtapi/v2/url/report"
        params = {
            "resource": link,
            "scan": 1,
            "apikey": config.virustotalapikey
        }
        jsonURL = await functions.PostRequest(url, params)

        #If jsonURL is None or the response_code is -1, then return with the error.
        if jsonURL == None:
            await ctx.send("An error has occured.")
            return
        
        if jsonURL["response_code"] == -1:
            await ctx.send(jsonURL["verbose_msg"])
            return
        
        #If the verbose_msg is along the lines of queuing a scan request, then give the user an embed with the link to the scanned URL.
        if jsonURL["verbose_msg"] == "Scan request successfully queued, come back later for the report":
            embed = await functions.CreateEmbed(
                title="URL Scan",
                description="VirusTotal is scanning the URL. Please click on the result URL to find results. (This only happens when a URL hasn't been scanned before). Make sure to click the file result as well if the URL had a file that automatically downloaded.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
                footer=(f"Scan Date: {jsonURL['scan_date']}", discord.Embed.Empty)
            )
            embed.add_field(name="Searched URL", value=jsonURL["resource"], inline=True)
            embed.add_field(name="Actual URL", value=jsonURL["url"], inline=True)
            embed.add_field(name="Results", value=jsonURL["permalink"], inline=True)
            await ctx.send(embed=embed)
        #Else, give the user the results with the positives and link to the results page.
        else:
            embed = await functions.CreateEmbed(
                title="URL Scan",
                description="VirusTotal has already scanned the URL. Here are the results.",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png")),
                footer=(f"Scan Date: {jsonURL['scan_date']}", discord.Embed.Empty)
            )
            embed.add_field(name="Searched URL", value=jsonURL["resource"], inline=True)
            embed.add_field(name="Actual URL", value=jsonURL["url"], inline=True)
            embed.add_field(name="Results URL", value=jsonURL["permalink"], inline=True)
            embed.add_field(name="Positives", value=f"{jsonURL['positives']}/{jsonURL['total']}", inline=True)
            
            #If there's a file attached to the URL, then send another scan for that and add it to the embed.
            if "filescan_id" in jsonURL:
                if jsonURL["filescan_id"] != None and jsonURL["filescan_id"] != "None":
                    url = "https://www.virustotal.com/vtapi/v2/file/report"
                    params = {
                        "resource": jsonURL["filescan_id"],
                        "apikey": config.virustotalapikey
                    }
                    jsonURL2 = await functions.GetRequest(url, params)

                    #If the verbose_msg has a queued result, then give the member the link, else give the member the positives and the link.
                    if jsonURL2 != None:
                        if jsonURL2["verbose_msg"] == "Scan request successfully queued, come back later for the report" or jsonURL2["verbose_msg"] == "Your resource is queued for analysis":
                            embed.add_field(name="File Scan URL", value=jsonURL2["permalink"])
                        else:
                            embed.add_field(name="File Scan URL", value=jsonURL2["permalink"])
                            embed.add_field(name="File Positives", value=f"{jsonURL2['positives']}/{jsonURL2['total']}")

            await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command(aliases=["tinyurl", "shortenurl", "shorturl"])
    async def shorten(self, ctx, link):
        """Command which creates shortened links with TinyURL. jupikdsplit->Member"""

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url="https://tinyurl.com/api-create.php", params={"url": link}) as resp:
                    resp = await resp.text()
                    session.close()

            embed = await functions.CreateEmbed(
                title="URL Shorten",
                author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
            )
            embed.add_field(name="Long URL", value=link)
            embed.add_field(name="Shortened URL", value=resp, inline=False)
            await ctx.send(embed=embed)

        #Catch exception, print, and return None.
        except Exception as e:
            print(f"Error: {e}")

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(functions.MemberPermCommandCheck)
    @commands.command()
    async def unshorten(self, ctx, link):
        """Command which unshortens links. jupikdsplit->Member"""

        session = requests.Session()
        resp = session.head(link, allow_redirects=True)

        embed = await functions.CreateEmbed(
            title="URL Unshorten",
            author=(self.bot.user.display_name, discord.Embed.Empty, self.bot.user.avatar_url_as(format="png"))
        )
        embed.add_field(name="Shortened URL", value=link)
        embed.add_field(name="Actual Location", value=resp.url, inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UtilCommands(bot))