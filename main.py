import discord
from get_data import get_city, get_response, parse_response
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
async def temp(ctx, city_arg): # "w/temp"
    # Gets all the variables needed
    now = datetime.now() # Gets time
    current_time = now.strftime("%H:%M") # Parses time to only be in hours and minutes
    complete_url = get_city(city_arg) # Calls the get_city and fills it in with the command arguement from the user
    x = get_response(complete_url) # API call
    data = parse_response(x) # Parses json data from API call

    condition = data[0] # Gets weather condition from json data
    temp = data[1] # Gets temperature from json data

    if city_arg == "London, CA":     # Changes channel name to display temperature stats readily only if requested city is London, ON (new feature: 03/12) 
        channel = client.get_channel(822198652398600242)
        await channel.edit(name="Temperature: " + temp)

    image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)

    embedVar = discord.Embed(title="Weather for " + city_arg, description="Source: OpenWeatherMap", color=0x0000ff) # Moved from test embed function
    
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url=image_url)
    embedVar.add_field(name="Condition", value=condition, inline=False)
    embedVar.set_footer(text="Data retreived at: " + current_time)

    await ctx.send(embed=embedVar)
    print("Sucessful!")

@temp.error
async def temp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguement: Please type in the City Name! Defaulting to London, Ontario...")

        now = datetime.now() # Gets time
        current_time = now.strftime("%H:%M") # Parses time to only be in hours and minutes
        x = get_response("http://api.openweathermap.org/data/2.5/weather?q=London,%20CA&units=metric&appid=b4f6dd2094bdd5048ce9025a901553df") # API call
        data = parse_response(x) # Parses json data from API call

        condition = data[0] # Gets weather condition from json data
        temp = data[1] # Gets temperature from json data

           # Changes channel name to display temperature stats readily only if requested city is London, ON (new feature: 03/12) 
        channel = client.get_channel(822198652398600242)
        await channel.edit(name="Temperature: " + temp)

        image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)

        embedVar = discord.Embed(title="Weather for London, Ontario", description="Source: OpenWeatherMap", color=0x0000ff) # Moved from test embed function
        
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