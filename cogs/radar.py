import discord
from discord.ext import commands 

class radar(commands.Cog):

        def __init__(self, client):
                self.client = client
        
        @commands.command()
        async def radar(self, ctx):
            await ctx.send("envcan sucks. Radar coming soon!")

def setup(client):
    client.add_cog(radar(client))

