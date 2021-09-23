
import discord
from discord.ext import commands
import os
import sys
import wget

# --- Start of commands section --- #
class nationwide(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nationwide(self, ctx):
        embedVar = discord.Embed(title="Canada Nationwide Conditions", description="Source: Environment Canada", color=0xebd834)
        try:
            print("[NATIONWIDE] Attempting to fetch nationwide image.")
            wget.download("https://weather.gc.ca/data/wxoimages/wocanmap0_e.jpg", "nationwide.jpg")
            file = discord.File("nationwide.jpg")
            embedVar.set_image(url="attachment://nationwide.jpg")
            await ctx.send(file = file, embed=embedVar)
            os.remove("nationwide.jpg")
            print("\nSuccessfully fetched the nationwide image.")
        except:
            print("\nFailed to fetch nationwide condition")
            await ctx.send("Couldn't fetch the nationwide conditions picture.")
        finally:
            await ctx.message.delete()
    
def setup(client):
    client.add_cog(nationwide(client))