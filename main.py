import discord
from get_data import get_temp, get_condition, get_data
from discord.ext import commands

client = commands.Bot(command_prefix = 'w/') # Defines the command prefix to be "w/"

@client.event
async def on_ready(): # When the bot and the Discord API are ready, print this command...
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
    container = get_data() # Calls the get_data function in the get_data file
    temp = get_temp(container) # Calls to get the temperature data from the get_data file
    condition = get_condition(container) # Calls to get weather condition
    if condition == "Mostly Cloudy":
        await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition + " with a chance of meatballs") # Just for movie fun!
    else:
        await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition)

client.run('') # Token (if re-gen, plz replace it.)
