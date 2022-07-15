import discord
from discord.ext import commands, tasks
import requests, json
from datetime import datetime
from bs4 import BeautifulSoup as soup
from requests import api
from dotenv import load_dotenv
import os

# -- Variable declaration -- #
load_dotenv()
api_key = os.environ.get("OWM_API_KEY") # OWM Key
api_key_geo = os.environ.get("MAPBOX_API_KEY") # Mapbox API Key
base_url_city = "http://api.openweathermap.org/data/2.5/weather?" 
base_url_geocode = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
embed = () # Declaring embed variable for caching London,CA data

# -- Weather functions -- #

# -- Fetches cords for cities -- #
def get_cords(city_name, country):
    complete_url_geo = base_url_geocode + city_name + ".json?country=" + country + "&access_token=" + api_key_geo
    return complete_url_geo

# -- Requests a response from OpenWeatherMap -- #
def get_response_owm(complete_url_city):
    response = requests.get(complete_url_city) # API call
    x = response.json() # Converts json to python-understanable format stuff
    return x

# -- Geocoding response > Weather request response -- #
def get_response_geocode(complete_url_geo):
    response = requests.get(complete_url_geo)
    x_geo = response.json()
    main_geo_info = x_geo["features"]
    main_cords = main_geo_info[0]["center"]
    longitude = main_cords[0]
    latitude = main_cords[1]
    complete_weather_geo_url = "http://api.openweathermap.org/data/2.5/weather?" + "lat=" + str(latitude) + "&lon=" + str(longitude) + "&units=metric" "&appid=" + api_key
    print(complete_weather_geo_url)
    
    response_geocoded = requests.get(complete_weather_geo_url)
    geo_weather_data = response_geocoded.json()
    
    return geo_weather_data

# -- Parses OpenWeatherMap response for geocoded locations -- #
def parse_response(owm_response, is_london):
    y = owm_response["main"]
    z = owm_response["weather"]
    w = owm_response["sys"]
    wind = owm_response["wind"]

    # -- Wind stats -- #
    wind_speed = wind["speed"]
    wind_direction = wind["deg"]
    # wind_gust = wind["gust"] (Broken as of 05/06)

    if is_london is False:
        cords = owm_response["coord"]
        city_name = owm_response["name"]
        server_response_code = owm_response["cod"]

        # -- Get's timezone difference from London, Ontario -- #
        timezone = owm_response["timezone"]
        timezone_london = -14400

        if timezone > timezone_london:
            time_difference = -1 * (-14400 - timezone) / 3600
        elif timezone < timezone_london:
            time_difference = -1 * (timezone_london - timezone) / 3600
        else:
            time_difference = 0 # For regions with the same timezone as London, ON
            
        # -- Other variables -- #
        country_code = w["country"]
        condition = z[0]["description"]
        icon = z[0]["icon"]
        temp = y["temp"] 
        full_icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
        
        return condition, temp, full_icon_url, country_code, cords, city_name, server_response_code, time_difference, wind_speed, wind_direction
    
    else:
        condition = z[0]["description"]
        icon = z[0]["icon"]
        temp = y["temp"]
        
        full_icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"

        return condition, temp, full_icon_url, wind_speed, wind_direction # wind gust broken

# -- Fetches high and low temperature for London, ON -- #
def get_high_low_london():
    data_url = "https://weather.gc.ca/city/pages/on-137_metric_e.html"
    response = requests.get(data_url)
    page_soup = soup(response.content, "html.parser") # Parses the HTML elements 
    container = page_soup.find("div",{"id":"container"}) # Finds container div

    alert_banner = page_soup.find("div",{"class":"row alert-item bg-alerts"}) # Alert_banner element
    if alert_banner is None:
        alert_banner = page_soup.find("div",{"class":"row alert-item bg-bulletin"}) # Banner during special weather statements
    
    if alert_banner is None:
        alert_banner = page_soup.find("div",{"class":"row alert-item bg-veille"}) # Banner during weather watches

    humidity_banner = container.find("dl",{"class":"dl-horizontal wxo-conds-col3"}) # Humidity_banner element
    
    try: # -- Try to see if there is a warning from envcan -- #
        alert = alert_banner.find("div",{"class":"col-xs-10 text-center"}).text
        print(alert)
    except:
        print("No weather warnings or watches")
        alert = "No Alerts." 
    finally: # Other code goes here
        high_temp = container.find("span",{"class":"high wxo-metric-hide"}).text # Span
        low_temp = container.find("span",{"class":"low wxo-metric-hide"}).text # Span
        humidex = humidity_banner.find("dd",{"class":"mrgn-bttm-0 wxo-metric-hide"}).text

        # -- If humidex is not available (replaced with Visibility), return None -- #
        if "km" in humidex:
            humidex = "None"
        else:
            humidex = humidex + chr(176) + "C"

        return low_temp, high_temp, alert, humidex

# -- Produces embed from data -- #
def make_embed(city_arg, country_arg):

    # Variable declaration
    now = datetime.now() 
    current_time = now.strftime("%H:%M") # Full time > "Hour:Minute"
    hour = now.strftime("%H") 
    
    if city_arg == "":
        is_london = True
        x = get_response_owm("http://api.openweathermap.org/data/2.5/weather?q=London,%20CA&units=metric&appid=" + api_key)
        print("http://api.openweathermap.org/data/2.5/weather?q=London,%20CA&units=metric&appid=" + api_key)
        data = parse_response(x, is_london) # Converts json data

        condition = data[0].title() # Gets weather condition from json data
        temp = round(data[1]) # Gets temperature from json data
        image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)
        wind_spd = data[3]
        # wind_gst = data[4] # Wind gust broken
        wind_deg = data[4] # temporairly index 4 as windgust is broken
        env_can_data = get_high_low_london()
        temp_low = env_can_data[0]
        temp_high = env_can_data[1]
        alert = env_can_data[2]
        humidex = env_can_data[3]

    # -- If OWM doesn't have the city, fall back to Mapbox for geocoding. -- #
    else:
        is_london = False
        if country_arg == "":
            x = get_response_owm("http://api.openweathermap.org/data/2.5/weather?q=" + city_arg + "&units=metric&appid=" + api_key)
            if x["cod"] == "404":
                print("OWM could not find the city...falling back to Mapbox.")
                x = get_response_geocode("https://api.mapbox.com/geocoding/v5/mapbox.places/" + city_arg + ".json?access_token=" + api_key_geo)
            else:
                print("Sucessfully skipped Mapbox.")

        else:
            x = get_response_owm("http://api.openweathermap.org/data/2.5/weather?q=" + city_arg + "," + country_arg + "&units=metric&appid=" + api_key)
            if x["cod"] == "404":
                print("OMV could not find the location...falling back to Mapbox.")
                complete_url = get_cords(city_arg, country_arg) # Calls the get_city and fills it in with the command arguement from the user
                x = get_response_geocode(complete_url) # API call
            else:
                print("Sucessfully skipped Mapbox.")

        print(x)
        data = parse_response(x, False)

        condition = data[0].title() # Gets weather condition from json data
        temp = round(data[1]) # Gets temperature from json data
        image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)
        country_code = data[3]
        cords = data[4]
        city_name = data[5]
        wind_speed = data[8]
        wind_deg = data[9]

        print("All weather information is fetched!")     

    print("Attempting to calculate wind direction.")
    # -- Conditionnal wind direction variable -- #
    wind_dir = ""
    if wind_deg == 0:
        wind_dir = "N"
    elif wind_deg == 90:
        wind_dir = "E"
    elif wind_deg == 180:
        wind_dir = "S"
    elif wind_deg == 270:
        wind_dir = "W"
    elif wind_deg in range(1, 89):
        wind_dir = "NE"
    elif wind_deg in range(91, 179):
        wind_dir = "SE"
    elif wind_deg in range(181, 269):
        wind_dir = "SW"
    elif wind_deg in range(271, 359):
        wind_dir = "NW"
    
    print("Finished calculating wind direction.")
    
    print("Attempting to calculate embed colour direction.")
    # -- Conditionnal embed colour based on temperature -- #
    embed_colour = 0xffffff # Default colour
    if temp <= -20:
        embed_colour = 0xFFFAFA
    elif temp in range(-19, 1):
        embed_colour = 0x7ed4e6
    elif temp in range(1, 7):
        embed_colour = 0x0dbab1
    elif temp in range(7, 16):
        embed_colour = 0x2e8b57
    elif temp in range(16, 28):
        embed_colour = 0xffff00
    elif temp in range(28, 34):
        embed_colour = 0xff0000
    elif temp in range(34, 40):
        embed_colour = 0xb22222
    elif temp >= 40:
        embed_colour = 0x800000
    
    print("Finished calculating embed colour.")

    if is_london:
        # -- Essembles embed from data -- #
        embedVar = discord.Embed(title="Weather for London, Ontario", description="Source: OpenWeatherMap/Environment Canada", color=embed_colour) # Moved from test embed function
        
        # -- If there is an alert, direct header to Environment Canada website link
        if alert == "No Alerts.":
            embedVar.add_field(name="Weather Alert", value=alert, inline=False)
        else:
            embedVar.add_field(name="Weather Alert", value=alert + ' [More info](https://weather.gc.ca/city/pages/on-137_metric_e.html)', inline=False)
            
        embedVar.add_field(name="Temperature | Wind Chill:", value=str(temp) + chr(176) + "C" " | " + humidex, inline=False)
        embedVar.set_image(url=image_url)
        embedVar.add_field(name="Condition", value=condition, inline=False)
        embedVar.add_field(name="Current Wind Speed:", value=str(round(wind_spd * 3.6, 2)) + " km/h [" + wind_dir + "]", inline=False)
        #embedVar.add_field(name="Wind Gust:", value="Completely borked.", inline=False)
       
        # -- Conditionnal embed headers (time of day) -- #
        if int(hour) >= 15 and int(hour) > 0:
            embedVar.add_field(name="High for Tomorrow:", value=temp_high, inline=False)
        else:
            embedVar.add_field(name="High for Today:", value=temp_high, inline=False)

        embedVar.add_field(name="Low for Today:", value=temp_low, inline=False)
        embedVar.set_footer(text="Data retreived at: " + current_time + " London, ON time.")

        return embedVar, temp, condition

    # -- If not London, Ontario essemble different looking embed -- #
    else:
        # -- Essembles embed from data -- #
        print("Attempting to asssemble embed for + city_arg!")
        embedVar = discord.Embed(title="Weather for " + city_name + ", " + country_code, description="Source: OpenWeatherMap", color=embed_colour) # Moved from test embed function   
        embedVar.add_field(name="Temperature:", value=str(temp) + chr(176) + "C", inline=False)
        embedVar.set_image(url=image_url)
        embedVar.add_field(name="Condition", value=condition, inline=False)
        embedVar.add_field(name="Wind Speed:", value=str(round(wind_speed * 3.6, 2)) + " km/h " + wind_dir, inline=False)
        embedVar.add_field(name="Coordinates:", value=cords, inline=False)
        
        # -- If timezone is behind London, print "-", if ahead, print "+" -- #
        if data[7] < 0:
            embedVar.set_footer(text="Data retreived at: " + current_time + str(data[7]))
        elif data[7] > 0:
            embedVar.set_footer(text="Data retreived at: " + current_time + " + " + str(data[7]))
        elif data[7] == 0:
            embedVar.set_footer(text="Data retreived at: " + current_time) # For regions with the same timezone as London, ON

        return embedVar, city_name 

# --- Start of commands section --- #
class temp(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    # w/temp. embeds weather data.
    @commands.command()
    async def temp(self, ctx, city_arg, country_arg=""):
        if country_arg == "":
            await ctx.send("No country argument! The location may be incorrect as a result.")
           
        try:
            data_pack = make_embed(city_arg, country_arg) # tuple for city_name, embedVar, response_code
        except:
            print("Failed to receive data pack from make_embed")
        finally:
            city_name = data_pack[1]

            # -- Let's user know if the bot couldn't find location. -- #
            if city_arg.lower() in city_name.lower():
                await ctx.send("Sucessfully found the location.")
            else:
                await ctx.send("Hm, I couldn't find that location...Falling back to somewhere else that's as close as possible.")

            await ctx.send(embed=data_pack[0]) # sends embed
            await ctx.send("Another day another ~~dollar~~ weather request!")

            print("Sucessful!")
    
    # Makes London,CA embed every 30 minutes for caching
    @tasks.loop(seconds=1800.0)
    async def test(self):
        print("[Loop] Making London,CA Embed...")
        global embed 
        embed = make_embed("", "CA")

        # Changes channel name to display temperature stats readily only if requested city is London, ON (new feature: 03/12)
        print("[Loop] Changing Channel Status")
        channel = self.client.get_channel(822198652398600242)
        await channel.edit(name=str(embed[1]) + chr(176) + "C" + " | " + str(embed[2]))
      
    # Error for missing city argument.
    @temp.error
    async def temp_error(self, ctx, error):
        # If loop hasn't been started yet...detects by checking if embed is there
        if embed == ():
            print("[London] Loop hasn't been started yet! Starting...")
            self.test.start()
        else:
            print("[London] Loop is already on! Sending latest fetched data!")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Wouldn't you like to know, Weather Boi? Wait, aren't I the Weather Boi?")
            await ctx.send(embed=embed[0]) # sends cached embed

            print("Sucessfully sent cached embed!")
    
def setup(client):
    client.add_cog(temp(client))

