from urllib.request import urlopen as uRequest 
from bs4 import BeautifulSoup as soup

def get_data():
    myUrl = 'https://weather.gc.ca/city/pages/on-137_metric_e.html' # Environment Canada URL
    uClient = uRequest(myUrl)
    page_html = uClient.read() # Reads the HTML source from the URL and puts it to a variable
    uClient.close()

    # parses html code into a variable
    page_soup = soup(page_html, "html.parser") # Actually parses the HTML elements using BeautifulSoup
    container = page_soup.find("div",{"id":"container"}) # Finds container div (where all the data is stored(inspect element of find out more))
    return container

def get_temp(container):
    temp = container.find("span",{"class":"wxo-metric-hide"}).text # Gets temp data from appropiate element
    return temp

def get_condition(container):
    condition = container.findAll("dd",{"class":"mrgn-bttm-0"}) # Gets weather condition from appropitate element
    return condition[2].text

def get_date_of_data(container):
    pass # W.I.P. (find the appropiate element for the date somewhere on the site later)

def get_icon(container): # Conditional weather icons. Added to replace stupid if-else statement. Now gets weather icon from html elements
    prefex_url = "https://weather.gc.ca/"
    icon = container.find("img",{"class":"center-block mrgn-tp-md"})
    icon_url = prefex_url + icon["src"]
    return icon_url
   




    






