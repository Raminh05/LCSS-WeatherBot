import requests, json
from bs4 import BeautifulSoup as soup
from datetime import datetime
from urllib.request import urlopen as uRequest 
import discord

api_key = "b4f6dd2094bdd5048ce9025a901553df"
api_key_geo = "pk.eyJ1IjoiY2Fubm9saSIsImEiOiJja21udzZpN3AxeXJmMm9zN3BuZGR3aTE0In0.w62dorEJ-QKwtJSswhRVaQ"
base_url_city = "http://api.openweathermap.org/data/2.5/weather?"
base_url_geocode = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

def get_cords(city_name, country):
    complete_url_geo = base_url_geocode + city_name + ".json?country=" + country + "&access_token=" + api_key_geo
    return complete_url_geo

def get_response_city(complete_url_city):
    response = requests.get(complete_url_city) # API call
    x = response.json() # Converts json to python-understanable format stuff
    return x

def get_response_geo(complete_url_geo):
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

def parse_response_geo(response_geocoded):
    y = response_geocoded["main"]
    z = response_geocoded["weather"]
    w = response_geocoded["sys"]
    cords = response_geocoded["coord"]

    country_code = w["country"]
    condition = z[0]["description"]
    icon = z[0]["icon"]
    temp = str(y["temp"]) + chr(176) + "C"
    full_icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
    
    return condition, temp, full_icon_url, country_code, cords
    
def parse_response_city(x):
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

def get_high_low_london():
    data_url = "https://weather.gc.ca/city/pages/on-137_metric_e.html"
    uClient = uRequest(data_url)
    page_html = uClient.read()
    
    page_soup = soup(page_html, "html.parser") # Actually parses the HTML elements using BeautifulSoup
    container = page_soup.find("div",{"id":"container"}) # Finds container div (where all the data is stored(inspect element of find out more))

    high_temp = container.find("span",{"class":"high wxo-metric-hide"}).text
    low_temp = container.find("span",{"class":"low wxo-metric-hide"}).text
    
    return low_temp, high_temp


def embed_london():
    now = datetime.now() # Gets time
    current_time = now.strftime("%H:%M") # Parses time to only be in hours and minutes
    x = get_response_city("http://api.openweathermap.org/data/2.5/weather?q=London,%20CA&units=metric&appid=b4f6dd2094bdd5048ce9025a901553df") # API call
    data = parse_response_city(x) # Parses json data from API call

    
    condition = data[0] # Gets weather condition from json data
    temp = data[1] # Gets temperature from json data
    image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)
    temp_low = get_high_low_london()[0]
    temp_high = get_high_low_london()[1]

    embedVar = discord.Embed(title="Weather for London, Ontario", description="Source: OpenWeatherMap/Environment Canada", color=0x0000ff) # Moved from test embed function
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url=image_url)
    embedVar.add_field(name="Condition", value=condition, inline=False)
    embedVar.add_field(name="High for Today:", value=temp_high, inline=False)
    embedVar.add_field(name="Low for Today:", value=temp_low, inline=False)
    embedVar.set_footer(text="Data retreived at: " + current_time + " London, ON time.")

    return embedVar, temp 

def embed_everywhere_else(city_arg, country_arg):
    # Gets all the variables needed
    if country_arg == "":
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        x = get_response_geo("https://api.mapbox.com/geocoding/v5/mapbox.places/" + city_arg + ".json?access_token=" + "pk.eyJ1IjoiY2Fubm9saSIsImEiOiJja21udzZpN3AxeXJmMm9zN3BuZGR3aTE0In0.w62dorEJ-QKwtJSswhRVaQ")
        print(x)
        data = parse_response_geo(x)
    else:
        now = datetime.now() # Gets time
        current_time = now.strftime("%H:%M") # Parses time to only be in hours and minutes
        complete_url = get_cords(city_arg, country_arg) # Calls the get_city and fills it in with the command arguement from the user
        x = get_response_geo(complete_url) # API call
        print(x)
        data = parse_response_geo(x) # Parses json data from API call
       
    condition = data[0] # Gets weather condition from json data
    temp = data[1] # Gets temperature from json data
    image_url = data[2] # calls get_icon to get weather icon according to the condition (Update 03/18)
    country_code = data[3]
    cords = data[4]
    
    embedVar = discord.Embed(title="Weather for " + city_arg + ", " + country_code, description="Source: OpenWeatherMap", color=0x0000ff) # Moved from test embed function   
    embedVar.add_field(name="Temperature", value=temp, inline=False)
    embedVar.set_image(url=image_url)
    embedVar.add_field(name="Condition", value=condition, inline=False)
    embedVar.add_field(name="Coordinates:", value=cords, inline=False)
    embedVar.set_footer(text="Data retreived at: " + current_time + " London, ON local time.")

    return embedVar

get_high_low_london()







# For debugging
#response_geocoded = get_response_geo("https://api.mapbox.com/geocoding/v5/mapbox.places/vancouver,%20CA.json?access_token=pk.eyJ1IjoiY2Fubm9saSIsImEiOiJja21udzZpN3AxeXJmMm9zN3BuZGR3aTE0In0.w62dorEJ-QKwtJSswhRVaQ")
#data = parse_response_geo(response_geocoded)
#print(data)





        
    
    


    
    





    






