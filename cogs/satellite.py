
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
        path = os.getcwd() + "satellite.jpg"
        wget.download("https://weather.gc.ca/data/satellite/goes_nam_1070_100.jpg", path)
        file = discord.File(path, filename="image.png")
        embedVar.set_image(url="attachment://image.png")
        await ctx.send(file = file, embed=embedVar)
        os.remove(path)
        await ctx.message.delete()
    
def setup(client):
    client.add_cog(satellite(client))