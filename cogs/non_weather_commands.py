import discord
from discord.ext import commands
import os, sys

class non_weather_commands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # On-ready event.
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="with the weather")) # Bot ready > print message / send online message
        channel = self.client.get_channel(789619349903507456) # Sends message to #bot-commands
        await channel.send("Online and ready to take commands.") 
        print('Bot is on!')
    
    # w/ping. Returns latency time.
    @commands.command()
    async def ping(self, ctx): # ctx = context, the function name == context. Applies elsewhere.
        await ctx.message.delete()
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    # w/hello. Prints hello message
    @commands.command()
    async def hello(self, ctx):
        await ctx.send('***Hi there! I am WeatherBot.***')
        await ctx.message.delete()

    # w/shutdown. Shutdown bot.
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx): 
        await ctx.send("Shutting down...")
        await ctx.message.delete()
        await ctx.bot.logout()
    
    # About me command -- host info and specs
    @commands.command()
    async def aboutme(self, ctx):
        import platform
        platform_text = platform.platform()
        

        # -- embed variable -- #
        embedVar = discord.Embed(title="About Me:", description="MINIMUM WAGE BABY!!! Jk, I don't get paid.", color=0x0dbab1)

        embedVar.add_field(name="OS:", value=platform_text, inline=False)
        embedVar.set_footer(text="My social security number is 420696969696969")
      
        await ctx.send(embed=embedVar)

    # w/refresh. Refresh cogs after modications.
    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx):
        try:
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    self.client.unload_extension(f'cogs.{filename[:-3]}')
                    self.client.load_extension(f'cogs.{filename[:-3]}')
                    print("Refreshed cog")
            
            await ctx.message.delete()
            await ctx.send("All cogs reloaded!")
        except:
            await ctx.send("Unable to refresh cogs. An error has occured.")

def setup(client):
    client.add_cog(non_weather_commands(client))
        
