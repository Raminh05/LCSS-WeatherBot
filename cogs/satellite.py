
import discord
from discord.ext import commands
import os
import sys
import wget

# --- Start of commands section --- #
class satellite(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def satellite(self, ctx):
        embedVar = discord.Embed(title="Latest Satellite Imagery", description="Source: Environment Canada/NOAA", color=0xebd834)
        wget.download("https://weather.gc.ca/data/satellite/goes_nam_1070_100.jpg", "satellite.jpg")
        file = discord.File("satellite.jpg")
        embedVar.set_image(url="attachment://satellite.jpg")
        await ctx.send(file = file, embed=embedVar)
        os.remove("satellite.jpg")
        await ctx.message.delete()
    
async def setup(client):
    await client.add_cog(satellite(client))