import os
import random, datetime, asyncio

import discord
from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
  guild = discord.utils.get(bot.guilds, name=GUILD)
  print (f'{bot.user} is connected on {guild}')

#Basic greetings and replies
@bot.event 
async def on_message(message):
    username = str(message.author.display_name)
    channel = str(message.channel.name)
    user_message = str(message.content).lower()

    if message.author == bot.user:
        return

    #hello, bye, and birthday
    helloGreetings = [
        f"Hello {username}!", f"Hi {username}!", f"Hai {username}!",
    ]
    byeGreetings = [
        f"goodbye {username}!", f"bai {username}!", f"bye {username}!",
    ]
 
    if user_message.startswith("hello") or user_message.startswith("hi") or user_message.startswith("hai"):
        await message.channel.send(random.choice(helloGreetings))
    elif user_message.startswith("goodbye") or user_message.startswith("bye") or user_message.startswith("bai"):
        await message.channel.send(random.choice(byeGreetings))
    
    if "happy birthday" in user_message:
        await message.channel.send(f"Happy birthday!!!!")
    
    #father/son recognization lol
    if user_message.startswith("son") and message.author.id == 690712947659374673:
        await message.channel.send("father!")
    elif user_message.startswith("son") and message.author.id != 690712947659374673:
        await message.channel.send("you are not my father >:(")
        
    await bot.process_commands(message)

@bot.listen()
async def on_message(message):
    username = str(message.author.display_name)
    channel = str(message.channel.name)
    user_message = str(message.content)

    if message.author == bot.user:
        return
    if "i'm" in user_message:
        await message.channel.send(f'test')
        return
    await bot.process_commands(message)

@bot.command()
async def ping(ctx,arg):
    await ctx.send(arg)
    

bot.run(TOKEN)
