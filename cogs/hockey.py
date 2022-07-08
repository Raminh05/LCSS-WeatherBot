import discord
from discord.ext import commands
from disputils import BotEmbedPaginator
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# -- API KEYS -- #
load_dotenv()
SPORTS_KEY = os.getenv("SPORTS_API_KEY")
now = datetime.now()
date = now.strftime("%Y-%m-%d")

def bruh(SPORTS_KEY):
    url = "https://v1.hockey.api-sports.io/games?league=57&season=2021&date=" + date + "&timezone=America/Toronto"

    payload={}
    headers = {
    'x-rapidapi-key': SPORTS_KEY,
    'x-rapidapi-host': 'v1.hockey.api-sports.io'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    x = response.json()

    data = x["response"]
    embedList = []
    embed_title = "Hockey Matches for Today"

    for game in data:
        game_title = game['teams']['home']['name'] + " vs. " + game['teams']['away']['name']
        game_status = "(" + game['status']['long'] + ")"
        scores = game['scores']
        time = game['time']
        home_team_logo = game['teams']['home']['logo']
        away_team_logo = game['teams']['away']['logo']
        

        embed = discord.Embed (
                title = embed_title,
                description = game_title + " " + game_status,
                colour = discord.Colour.blue()
            )

        embed.add_field(name="Score:", value=scores, inline=False)
        embed.set_footer(text="Game starts at: " + time + " EST")
        embed.set_image(url=home_team_logo)
        embedList.append(embed)
        
    return embedList

class hockey(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def hockey(self, ctx):
        embedList = bruh(SPORTS_KEY)
        paginator = BotEmbedPaginator(ctx, embedList)
        await paginator.run()
        await ctx.message.delete()

def setup(client):
    client.add_cog(hockey(client))

























