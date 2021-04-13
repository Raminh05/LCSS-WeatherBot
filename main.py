import discord
from get_data import embed_london, embed_everywhere_else
from discord.ext import commands
import os

client = commands.Bot(command_prefix = 'w/', description="") # Defines the command prefix to be "w/"

# Gets API key
with open(".env", encoding="utf-8") as f:
    api_key = f.read()
    f.close()

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Kelcogg's ")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# w/temp. embeds weather data.
@client.command()
async def temp(ctx, city_arg, country_arg=""): 
    if country_arg == "":
        await ctx.send("No country argument! The location may be incorrect as a result.")
    
    embedVar = embed_everywhere_else(city_arg, country_arg) # calls function from get_data

    await ctx.send(embed=embedVar) # sends embed
    await ctx.send("Another day another ~~dollar~~ weather request!")
    print("Sucessful!")

# Error for missing city argument.
@temp.error
async def temp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Nice try Buster...(sorry) but you need the city name if you don't want the weather for London, Ontario!")

        data_and_embed = embed_london() 
        await ctx.send(embed=data_and_embed[0]) # sends embed

        # Changes channel name to display temperature stats readily only if requested city is London, ON (new feature: 03/12) 
        channel = client.get_channel(822198652398600242)
        await channel.edit(name="Temperature: " + data_and_embed[1])

        
        print("Sucessful!")

# Iterates through all filenames in the cogs directory to load all cogs.
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(api_key)


# Uncomment and re-implement to def temp if need be.
 # if condition == "Mostly Cloudy":
        #await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition + " with a chance of meatballs") # Just for movie fun!
    #else:
        #await ctx.send("The temperature is " + temp + " in London, Ontario. Condition: " + condition)