import discord
from get_data import get_temp, get_condition, get_data, get_icon
from discord.ext import commands
import os
from datetime import datetime
import time

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
@commands.is_owner()
async def shutdown(ctx): # Shutdown command for the bot to logout of discord
    await ctx.send("Shutting down...")
    await ctx.bot.logout()

@client.command()
async def temp(ctx): # "w/temp"
    # Gets all the variables needed
    now = datetime.now() # Gets time
    current_time = now.strftime("%H:%M") # Parses time to only be in hours and minutes
    container = get_data() # Calls the get_data function in the get_data file
    temp = get_temp(container) # Calls to get the temperature data from the get_data file
    condition = get_condition(container) # Calls to get weather condition

    # Changes channel name to display temperature stats readily (new feature: 03/12)
    channel = client.get_channel(822198652398600242)
    await channel.edit(name="Temperature: " + temp)

    image_url = get_icon(container) # calls get_icon to get weather icon according to the condition (Update 03/18)

    embedVar = discord.Embed(title="Weather for London, ON", description="Source: Environment Canada", color=0x0000ff) # Moved from test embed function
    
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url=image_url)
    embedVar.add_field(name="Condition", value=condition, inline=False)
    embedVar.set_footer(text="Data retreived at: " + current_time)

    await ctx.send(embed=embedVar)
    print("Sucessful!")
    

client.run(api_key)

# Uncomment and re-implement to def temp if need be.
 # if condition == "Mostly Cloudy":
        #await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition + " with a chance of meatballs") # Just for movie fun!
    #else:
        #await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition)