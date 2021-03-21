import requests, json

api_key = "b08e7755c27079d70c07bce88cc2b385"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_city(city):
    city_name = city
    complete_url = base_url + "q=" + city_name + "&units=metric" "&appid=" + api_key
    return complete_url

def get_response(complete_url):
    response = requests.get(complete_url) # API call
    x = response.json() # Converts json to python-understanable format stuff
    return x

def parse_response(x):
    if x["cod"] != "404":
        y = x["main"]
        z = x["weather"]

        condition = z[0]["description"]
        icon = z[0]["icon"]
        temp = str(y["temp"]) + chr(176) + "C"

        full_icon_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"

    else:
        print("City not found")
    
    return condition, temp, full_icon_url





    






