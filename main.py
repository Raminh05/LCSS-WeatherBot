import discord
from get_data import get_temp, get_condition, get_data
from discord.ext import commands
import os

client = commands.Bot(command_prefix = 'w/', description="") # Defines the command prefix to be "w/"

# Gets API key
with open(".env", encoding="utf-8") as f:
    api_key = f.read()
    f.close()

@client.event
async def on_ready(): # When the bot and the Discord API are ready, print this command...
    await client.change_presence(activity=discord.Game(name="with the weather"))
    print('Bot is on!')

@client.command()
async def ping(ctx): # ctx = context, the function name IS THE context. So in this function: "ping" IS the context. So, the user must do "w/ping" to activate this command. Same applies for the rest.
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def hello(ctx):
    await ctx.send('***Hi there! I am WeatherBot.***')
 
@client.command()
async def embed(ctx): # W.I.P. This is only for testing the embed functionality. 
    container = get_data() 
    temp = get_temp(container)
    condition = get_condition(container)
    embedVar = discord.Embed(title="Weather for London, ON", description="Source: Environment Canada", color=0x00ff00)
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url="https://weather.gc.ca/weathericons/30.gif")
    embedVar.add_field(name="Condition", value=condition, inline=False)
    await ctx.send(embed=embedVar)

@client.command()
@commands.is_owner()
async def shutdown(ctx): # Shutdown command for the bot to logout of discord
    await ctx.send("Shutting down...")
    await ctx.bot.logout()

@client.command()
async def temp(ctx): # "w/temp"
    container = get_data() # Calls the get_data function in the get_data file
    temp = get_temp(container) # Calls to get the temperature data from the get_data file
    condition = get_condition(container) # Calls to get weather condition

    if condition == "Mostly Cloudy":
        await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition + " with a chance of meatballs") # Just for movie fun!
    else:
        await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition)

client.run(api_key)