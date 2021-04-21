import discord
from discord.ext import commands
import os
import requests, json
from bs4 import BeautifulSoup as soup
from datetime import datetime
from urllib.request import urlopen as uRequest 
import sys
sys.path.insert(1, '/home/pi/Desktop/Test/WeatherBot') # Importing modules from other directories

api_key = "b4f6dd2094bdd5048ce9025a901553df"
api_key_geo = "pk.eyJ1IjoiY2Fubm9saSIsImEiOiJja21udzZpN3AxeXJmMm9zN3BuZGR3aTE0In0.w62dorEJ-QKwtJSswhRVaQ"
base_url_city = "http://api.openweathermap.org/data/2.5/weather?"
base_url_geocode = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

# -- Fetches cords for cities -- #
def get_cords(city_name, country):
    complete_url_geo = base_url_geocode + city_name + ".json?country=" + country + "&access_token=" + api_key_geo
    return complete_url_geo

# -- Requests a response from OpenWeatherMap -- #
def get_response_london(complete_url_city):
    response = requests.get(complete_url_city) # API call
    x = response.json() # Converts json to python-understanable format stuff
    return x

# -- Geocoding response > Weather request response -- #
def get_response(complete_url_geo):
    response = requests.get(complete_url_geo)
    x_geo = response.json()
    main_geo_info = x_geo["features"]
    main_cords = main_geo_info[0]["center"]
    longitude = main_cords[0]
    latitude = main_cords[1]
    complete_weather_geo_url = "http://api.openweathermap.org/data/2.5/weather?" + "lat=" + str(latitude) + "&lon=" + str(longitude) + "&units=metric" "&appid=" + api_key
    response_geocoded = requests.get(complete_weather_geo_url)
    geo_weather_data = response_geocoded.json()
    return geo_weather_data

# -- Parses OpenWeatherMap response for geocoded locations -- #
def parse_response(response_geocoded):
    y = response_geocoded["main"]
    z = response_geocoded["weather"]
    w = response_geocoded["sys"]
    cords = response_geocoded["coord"]
    city_name = response_geocoded["name"]

    country_code = w["country"]
    condition = z[0]["description"]
    icon = z[0]["icon"]
    temp = str(y["temp"]) + chr(176) + "C"
    full_icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
    
    return condition, temp, full_icon_url, country_code, cords, city_name
    
# -- Parses OpenWeatherMap for London, ON -- #
def parse_response_london(x):
    if x["cod"] != "404":
        y = x["main"]
        z = x["weather"]

        condition = z[0]["description"]
        icon = z[0]["icon"]
        temp = str(y["temp"]) + chr(176) + "C"
        temp_low = str(y["temp_min"]) + chr(176) + "C"
        temp_high = str(y["temp_max"]) + chr(176) + "C"

        full_icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"

        return condition, temp, full_icon_url, temp_low, temp_high

    else:
        print("City not found...Falling back to cords.")

# -- Fetches high and low temperature for London, ON -- #
def get_high_low_london():
    data_url = "https://weather.gc.ca/city/pages/on-137_metric_e.html"
    uClient = uRequest(data_url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser") # Parses the HTML elements 
    container = page_soup.find("div",{"id":"container"}) # Finds container div 

    high_temp = container.find("span",{"class":"high wxo-metric-hide"}).text # Span
    low_temp = container.find("span",{"class":"low wxo-metric-hide"}).text # Span
    
    return low_temp, high_temp

# -- Produces embed from data -- #
def embed_london():
    # Variable declaration
    now = datetime.now() 
    current_time = now.strftime("%H:%M") # Full time > "Hour:Minute"
    hour = now.strftime("%H") 
    x = get_response_london("http://api.openweathermap.org/data/2.5/weather?q=London,%20CA&units=metric&appid=b4f6dd2094bdd5048ce9025a901553df") # API call
    data = parse_response_london(x) # Converts json data

    condition = data[0] # Gets weather condition from json data
    temp = data[1] # Gets temperature from json data
    image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)
    temp_low = get_high_low_london()[0]
    temp_high = get_high_low_london()[1]

    # -- Essembles embed from data -- #
    embedVar = discord.Embed(title="Weather for London, Ontario", description="Source: OpenWeatherMap/Environment Canada", color=0x0000ff) # Moved from test embed function
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url=image_url)
    embedVar.add_field(name="Condition", value=condition, inline=False)

    # -- Conditionnal embed headers (time of day) -- #
    if int(hour) >= 16 and int(hour) > 0:
        embedVar.add_field(name="High for Tomorrow:", value=temp_high, inline=False)
    else:
        embedVar.add_field(name="High for Today:", value=temp_high, inline=False)

    embedVar.add_field(name="Low for Today:", value=temp_low, inline=False)
    embedVar.set_footer(text="Data retreived at: " + current_time + " London, ON time.")

    return embedVar, temp 

# -- Produces embed from data -- #
def embed_everywhere_else(city_arg, country_arg):
    # Variable declaration

    if country_arg == "":
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        x = get_response("https://api.mapbox.com/geocoding/v5/mapbox.places/" + city_arg + ".json?access_token=" + "pk.eyJ1IjoiY2Fubm9saSIsImEiOiJja21udzZpN3AxeXJmMm9zN3BuZGR3aTE0In0.w62dorEJ-QKwtJSswhRVaQ")
        print(x)
        data = parse_response(x)
    else:
        now = datetime.now() # Gets time
        current_time = now.strftime("%H:%M") # Parses time to only be in hours and minutes
        complete_url = get_cords(city_arg, country_arg) # Calls the get_city and fills it in with the command arguement from the user
        x = get_response(complete_url) # API call
        print(x)
        data = parse_response(x) # Parses json data from API call
       
    condition = data[0] # Gets weather condition from json data
    temp = data[1] # Gets temperature from json data
    image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)
    country_code = data[3]
    cords = data[4]
    city_name = data[5]

    
    

    embedVar = discord.Embed(title="Weather for " + city_name + ", " + country_code, description="Source: OpenWeatherMap", color=0x0000ff) # Moved from test embed function   
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url=image_url)
    embedVar.add_field(name="Condition", value=condition, inline=False)
    embedVar.add_field(name="Coordinates:", value=cords, inline=False)
    embedVar.set_footer(text="Data retreived at: " + current_time + " London, ON local time.")

    return embedVar, city_name

# --- Start of commands section --- #
class weather_commands(commands.Cog):

    def __init__(self, client):
        self.client = client

    # w/temp. embeds weather data.
    @commands.command()
    async def temp(self, ctx, city_arg, country_arg=""): 
        if country_arg == "":
            await ctx.send("No country argument! The location may be incorrect as a result.")
        
        embedVar = embed_everywhere_else(city_arg, country_arg) # calls function from get_data

        # -- Let's user know if the bot couldn't find their specified location (Update: 04/21) -- # # -- embedVar[1] = city_name -- #
        # -- Check multi-word location names / compares it with user city_arg -- #
        city_name_split = embedVar[1].split(' ')

        if city_arg in city_name_split:
            await ctx.send("Sucessfully found the location.")
        else:
            await ctx.send("Hm, I couldn't find that location...Falling back to somewhere else that's as close as possible.")


        await ctx.send(embed=embedVar[0]) # sends embed
        await ctx.send("Another day another ~~dollar~~ weather request!")

        print("Sucessful!")

    # Error for missing city argument.
    @temp.error
    async def temp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Nice try Buster...(sorry) but you need the city name if you don't want the weather for London, Ontario!")

            data_and_embed = embed_london() 
            await ctx.send(embed=data_and_embed[0]) # sends embed

            # Changes channel name to display temperature stats readily only if requested city is London, ON (new feature: 03/12) 
            channel = self.client.get_channel(822198652398600242)
            await channel.edit(name="Temperature: " + data_and_embed[1])

            print("Sucessful!")
    
def setup(client):
    client.add_cog(weather_commands(client))