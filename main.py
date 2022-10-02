import discord
import asyncio
import os
from discord.ext import commands
from dotenv import dotenv_values


TOKEN = dotenv_values('.env')['TOKEN']
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '!',intents = intents)

@bot.event
async def on_ready():
    print('online')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user or message.content.startswith('!'):
        return
    await message.channel.send(f'olá {message.author.name} Eu sou o Trellinho seu amiguinho vamos configurar?, basta digitar !config')


async def load():
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')


async def main():
    await load()
    await bot.start(TOKEN)

asyncio.run(main())
