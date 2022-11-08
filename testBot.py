import os
import random, datetime, asyncio, json

import discord
from dotenv import load_dotenv

from discord.ext import commands



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#Startup
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(
        name = "the stars~~", type = discord.ActivityType.watching))
    guild = discord.utils.get(client.guilds, name=GUILD)
    print (f'{client.user} is connected on {guild}!')
    

#Basic greetings and replies
@client.event 
async def on_message(message):
    await client.wait_until_ready()    
    username = str(message.author.display_name)
    user_msg = str(message.content).lower()
    
    if message.author == client.user:
        return

    #hello and bye
    helloGreetings = [
        f"Hello {username}!", f"Hi {username}!", f"Hai {username}!"]
    byeGreetings = [
        f"goodbye {username}!", f"bai {username}!", f"bye {username}!"]
    
    if user_msg.startswith("hello") or user_msg.startswith("hi") or user_msg.startswith("hai"):
        await message.channel.send(random.choice(helloGreetings))
    elif user_msg.startswith("goodbye") or user_msg.startswith("bye") or user_msg.startswith("bai"):
        await message.channel.send(random.choice(byeGreetings))
    
    #father/son recognization
    if user_msg.startswith("son") and message.author.id == 690712947659374673:
        await message.channel.send("father!")
    elif user_msg.startswith("son") and message.author.id != 690712947659374673:
        await message.channel.send("you are not my father >:(")

    #Respond to ping
    if str(client.user.id) in user_msg:
        await message.channel.send("shhh pls don't disturb")
        
    await client.process_commands(message)



#Send birthday ping messages (maybe in the future)

#async def birthday_pings():
 #   await client.wait_until_ready()
    #now = datetime.datetime.now(2022,12,25) #change for testing purposes
  #  now = datetime.datetime(2022,11,19)

    #retrieve current month and day
   # month = now.month
    #day = now.day

    #channel = client.get_channel(839267199911067658)

    #while not client.is_closed:
     #   with open("dates.json", "r") as f:
      #      data = json.load(f) #read in data
       #     for date in data["dates"]: #loop through dates
        #        if date["month"] == month and date["day"] == day: 
         #           await channel.send("[insert]! <@!" + str(date["entity"]) + ">")
          #          print(date["month"] + date["day"])
           #         break 
        #await asyncio.sleep(86400) #wait a day

#Check connection command
@client.command()
async def ping(ctx):
    await ctx.channel.send("Pong! " + "<@" + str(client.user.id) + ">" + " is connected on " 
                            + str(discord.utils.get(client.guilds, name=GUILD)) + "!")

#Poll command
@client.command()
async def poll(ctx, question, *options):  
    #list of 10 emojis
    emoji_options = ["❤️","💙","🧡","🖤","💚","🤍","💛","🤎","💜", "💕"]

    react_options = [] #list that stores emojis to be used in the poll

    #convert options tuple to a list of strings
    poll_options = ["".join(i) for i in options] 
    
    number_of_options = len(poll_options) #get length of options in poll
    
    j = random.randint(0,10-number_of_options) #retrieve starting indice 
    i = 0
    while i < number_of_options:
        #inserts emojis of consecutive index starting from j
        react_options.insert(1, emoji_options[j+i]) 
        i += 1 

    description = " "
    i = 0
    while i < number_of_options:
        description += react_options[i] + " " + poll_options[i] + "\n" #generate description for embed
        i += 1
   
    #release poll
    embed = discord.Embed(title = question, description=description, color=0x69DFF7, timestamp=datetime.datetime.now())
    embed.set_footer(text=f"Poll made by {ctx.author.name}")
    message = await ctx.send(embed=embed)
    
    #add reactions
    i = 0
    while i < number_of_options:
        await message.add_reaction(react_options[i]) 
        i += 1

#Flip a coin command

    
  

    

    


#To do:
#Schedule birthday messages
#Add reactions/emojis

#Fetch data/media/pictures from online
#Flip a coin

#Possible:
#Weather bot

client.run(TOKEN)

#bot.loop.create_task(birthday_pings())
#bot.run(TOKEN)
    


