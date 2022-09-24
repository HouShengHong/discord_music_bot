import config
import discord
from discord import app_commands
from discord.ext import commands
from discord import FFmpegAudio
import asyncio
import os
import random

intents =  discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.',intents=intents ,application_id ='1017824016498696243')

@bot.event
async def on_ready():
    print('Online.')

async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')

async def main():
    await load()
    await bot.start(config.TOKEN)

asyncio.run(main())