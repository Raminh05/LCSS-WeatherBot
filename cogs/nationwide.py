
import discord
from discord.ext import commands
import os
import sys
import wget
from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

# --- Start of commands section --- #
class nationwide(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nationwide(self, ctx):
        embedVar = discord.Embed(title="Canada Nationwide Conditions", description="Source: Environment Canada", color=0xebd834)

        try:
            path = os.getcwd() + "nationwide.jpg"
            print("[NATIONWIDE] Attempting to fetch nationwide image.")
            wget.download("https://weather.gc.ca/data/wxoimages/wocanmap0_e.jpg", path)
            file = discord.File(path, filename="image.jpg")
            embedVar.set_image(url="attachment://image.jpg")
            await ctx.send(file = file, embed=embedVar)
            os.remove(path)
            print("\nSuccessfully fetched the nationwide image.")
        except:
            print("\nFailed to fetch nationwide condition")
            await ctx.send("Couldn't fetch the nationwide conditions picture.")
        finally:
            await ctx.message.delete()

    @commands.command()
    async def weatherwarns(self, ctx):
        await ctx.send("Gathering natiownide weather warnings and watches...")
        data_url = "https://weather.gc.ca/warnings/index_e.html"
        uClient = uRequest(data_url)
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser") # Parses the HTML elements 
        table = page_soup.find("table",{"class":"table table-striped table-hover table-responsive table-condensed"})
        rows = table.find_all("tr")

        for row in rows:
            await ctx.send(row.text)
        
def setup(client):
    client.add_cog(nationwide(client))