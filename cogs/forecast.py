
import discord
from discord.ext import commands
import os
import sys
import requests, json
from disputils import BotEmbedPaginator

# -- Fetches cords for cities -- #
def get_cords(city_name, country):
    complete_url_geo = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + city_name + ".json?country=" + country + "&access_token=" + "" # Put Mapbox API key in quotes
    return complete_url_geo

# --- Start of commands section --- #
class forecast(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def forecast(self, ctx, city, country):
        # -- OWM API KEY -- #
        api_key = "b4f6dd2094bdd5048ce9025a901553df"
        # -- Get cords -- #
        try:
            complete_url_geo = get_cords(city, country)
            print(complete_url_geo)
            print("[FORECAST] Sucessful fetch of Geo Weather Data")
        except:
            await ctx.send("Failed to fetch coordinates.")

        try:
            print("Parsing geo data...")
            geo = requests.get(complete_url_geo)
            x_geo = geo.json()
            main_geo_info = x_geo["features"]
            main_cords = main_geo_info[0]["center"]
            longitude = main_cords[0]
            latitude = main_cords[1]
            place_name = main_geo_info[0]["place_name"]
            print("[FORECAST] Sucessful parsing of geo data...")
        except:
            await ctx.send("[FORECAST] Failed to parse geo data...")
            print("[FORECAST] Failed to parse geo data...")

        try:
            print("Fetching forecast data...")
            forecast_data_url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + str(latitude) + "&lon=" + str(longitude) + "&exclude=hourly,minutely,current,alerts&units=metric&appid=" + api_key
            print(forecast_data_url)
            response = requests.get(forecast_data_url)
            await print(response)
        except:
            print("Failed to fetch forecast data...")
        
        try:
            x = response.json()
            forecast = x["daily"]
            #ac_city = x["city"]["name"] # Actual city
            #ac_country = x["city"]["country"] # Actual country
        except:
            print("Failed to parse forecast data...")
            await ctx.send("Failed to parse forecast data...")

        embedList = []
        
        from datetime import datetime
        for period in forecast:
            unix_time = float(period['dt'])
            time = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d') # Converts Unix Timestamp to datetime format
            max_temp = str(round(period['temp']['max'])) + chr(176) + "C"
            min_temp = str(round(period['temp']['min'])) + chr(176) + "C"
            condition = period['weather'][0]['description'].title()
            icon_url = "http://openweathermap.org/img/wn/" + period['weather'][0]['icon'] + "@2x.png" 
            
            embed = discord.Embed (
                title = "Weather for: " + place_name + " at " + time,
                description = "Condition: " + condition + " | " + "Max Temp: " + max_temp + " | " + "Min Temp: " + min_temp,
                colour = discord.Colour.orange()
            )
            embed.set_image(url=icon_url)
            embedList.append(embed)
        
        paginator = BotEmbedPaginator(ctx, embedList)
        await paginator.run()
    
    # Error for missing city argument.
    @forecast.error
    async def forecast_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("No location name / country code detected! No forecast is fetched.")
    
def setup(client):
    client.add_cog(forecast(client))
