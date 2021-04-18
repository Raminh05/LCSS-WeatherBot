import discord
from discord.ext import commands
import os

class non_weather_commands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # On-ready event.
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="with the weather")) # Bot ready > print message / send online message
        channel = self.client.get_channel(789619349903507456)
        await channel.send("I love and the weather.") 
        print('Bot is on!')
    
    # w/ping. Returns latency time.
    @commands.command()
    async def ping(self, ctx): # ctx = context, the function name == context. Applies elsewhere.
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    # w/hello. Prints hello message
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('***Hi there! I am WeatherBot.***')

    # w/shutdown. Shutdown bot.
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx): 
        await ctx.send("Shutting down...")
        await ctx.bot.logout()
    
    # w/refresh. Refresh cogs after modications.
    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.client.unload_extension(f'cogs.{filename[:-3]}')
                self.client.load_extension(f'cogs.{filename[:-3]}')
                print("Refreshed cog")
                
        await ctx.send("All cogs reloaded!")
    

def setup(client):
    client.add_cog(non_weather_commands(client))
        