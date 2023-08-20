import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from dotenv import load_dotenv

PATH= os.getcwd()

# Gets API key
load_dotenv()
API_KEY = os.getenv("DISCORD_API_KEY")

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix = "w/", intents = intents)
        
    async def setup_hook(self):
        await self.tree.sync(guild = discord.Object(id = 783415814342574151))
            

client = Client()

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await client.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await client.start(API_KEY)

if __name__ == "__main__":
    asyncio.run(main())




