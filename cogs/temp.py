import discord
from discord.ext import commands, tasks
from discord import app_commands
import os, sys

sys.path.append(os.getcwd() + "/utils")
from TemperatureUtilites import make_embed

# -- Variable declaration -- #
embed = () # Declaring embed variable for caching London,CA data

# --- Start of commands section --- #
class temp(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    # w/temp. embeds weather data.
    @commands.hybrid_command(name = "temp", description = "Gathers current weather information for a specified location.")
    @app_commands.guilds(discord.Object(id = 783415814342574151))
    async def temp(self, ctx, city_arg, country_arg=""):
        if country_arg == "":
            await ctx.send("No country argument! The location may be incorrect as a result.")
           
        try:
            data_pack = make_embed(city_arg, country_arg) # tuple for city_name, embedVar, response_code
        except:
            print("Failed to receive data pack from make_embed")
        finally:
            city_name = data_pack[1]

            # -- Let's user know if the bot couldn't find location. -- #
            if city_arg.lower() in city_name.lower():
                await ctx.send("Sucessfully found the location.")
            else:
                await ctx.send("Hm, I couldn't find that location...Falling back to somewhere else that's as close as possible.")

            await ctx.send(embed=data_pack[0]) # sends embed
            await ctx.send("Another day another ~~dollar~~ weather request!")

            print("Sucessful!")
    
    # Makes London,CA embed every 30 minutes for caching
    @tasks.loop(seconds=1800.0)
    async def test(self):
        print("[Loop] Making London,CA Embed...")
        global embed 
        embed = make_embed("", "CA")

        # Changes channel name to display temperature stats readily only if requested city is London, ON (new feature: 03/12)
        print("[Loop] Changing Channel Status")
        channel = self.client.get_channel(822198652398600242)
        await channel.edit(name=str(embed[1]) + chr(176) + "C" + " | " + str(embed[2]))
      
    # Error for missing city argument.
    @temp.error
    async def temp_error(self, ctx, error):
        # If loop hasn't been started yet...detects by checking if embed is there
        if embed == ():
            print("[London] Loop hasn't been started yet! Starting...")
            self.test.start()
        else:
            print("[London] Loop is already on! Sending latest fetched data!")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Wouldn't you like to know, Weather Boi? Wait, aren't I the Weather Boi?")
            await ctx.send(embed=embed[0]) # sends cached embed

            print("Sucessfully sent cached embed!")
    
async def setup(client):
    await client.add_cog(temp(client))

