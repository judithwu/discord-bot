import os, datetime, asyncio, json, aiohttp, random, time, base64
import discord
#from craiyon import Craiyon
#from PIL import Image
#from io import BytesIO

from discord.ext import commands

from dotenv import load_dotenv
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
        
    if user_msg.startswith("botbot"):
        await message.channel.send(username.upper()+"!!")
    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    await message.channel.send(message.author.display_name + " deleted a message: " + str(message.content))

#Send birthday ping messages (maybe in the future)
#@client.listen
#async def on_message():
    #await client.wait_until_ready()
    #now = datetime.datetime.now() #change for testing purposes
    #now = datetime.datetime(2022,11,19)

    #retrieve current month and day
   # month = now.month
  #  day = now.day
   
   # channel = await client.get_channel(839267199911067658)
    
    #while not client.is_closed:
       #with open("dates.json", "r") as f:
          #  data = json.load(f) #read in data
         #   for date in data["dates"]: #loop through dates
        #        if date["month"] == month and date["day"] == day: 
       #             await channel.send("[insert]! <@!" + str(date["entity"]) + ">")
      #              print(date["month"] + date["day"])
     #               break 
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
    emoji_options = ["❤️","💙","🧡","💗","💚","🤍","💛","🤎","💜", "💕"]

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
    embed.set_thumbnail(url="https://media3.giphy.com/media/ee72vyhtNdl5rx63n3/giphy.gif?cid=ecf05e47e6wreb4ttl7k6tgn19nlzvkxteqryb0ubtk1jav7&rid=giphy.gif&ct=s")
    message = await ctx.send(embed=embed)
    
    #add reactions
    i = 0
    while i < number_of_options:
        await message.add_reaction(react_options[i]) 
        i += 1

#Flip a coin
@client.command()
async def flip(ctx):
    possibilies = ["Heads!", "Tails!"]
    choice = random.choice(possibilies)
    embed = discord.Embed(title=choice)
  
    if choice == "Heads!":
        image = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjUFGlzYg0oo3qChB4tQoHlAWie5BFaPh4yQ&usqp=CAU"
        embed.set_thumbnail(url=image)
        await ctx.send(embed=embed)
    else:
        file = discord.File("yutatail.JPG")
        #embed = discord.Embed(title=choice)
        embed.set_thumbnail(url="attachment://yutatail.JPG")
        await ctx.send(embed=embed, file=file)

#Get affirmation from API
@client.command()
async def affirmation(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.affirmations.dev/') as r:
                    data = await r.json()
                    await ctx.send(data["affirmation"] + " 💜")

#Get gif from API
@client.command()
async def gif(ctx):
    categories = ["blush", "hug", "wink", "dance"]
    type = "sfw"
    category = random.choice(categories)
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.waifu.pics/{type}/{category}") as r:
                    data = await r.json()
                    embed = discord.Embed()
                    embed.set_image(url=data["url"])
                    await ctx.send(embed=embed)

#Get png from API
@client.command()
async def png(ctx):
    categories = ["waifu", "husbando", "neko"]
    category = random.choice(categories)
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekos.best/api/v2/{category}") as r:
                data = await r.json()
                embed = discord.Embed()
                embed.set_image(url=data["results"][0]["url"])
                await ctx.send(embed=embed)

#Get a scrapbook image
@client.command()
async def throwback(ctx):
   # s = time.perf_counter()
    attachments = []
    
    #channel = client.get_channel(1039650296273588244) for testing
    channel = client.get_channel(774788204745457724)
    async for message in channel.history(limit=1250):
        if message.attachments:
            picture = []
            picture.insert(1, message.attachments[0].url)
            picture.insert(1, message.jump_url)
            attachments.insert(1, picture)

    picture = random.choice(attachments)
    
    # Serializing json
    #json_object = json.dumps(attachments, indent=4)
 
# Writing to sample.json
  #  with open("sample.json", "w") as outfile:
   #   outfile.write(json_object)

    embed = discord.Embed()
    embed.set_image(url=str(picture[0]))
    embed.description = picture[1]

   # elapsed = time.perf_counter() - s
    embed.color = 0x1FDDF0
    await ctx.send(embed=embed)
    #await ctx.send(f"{__file__} executed in {elapsed:0.2f} seconds. (1500)")


#Eightball command
@client.command()
async def eightball(ctx, claim):
    responses = ["As I see it, yes", "Without a doubt", "Yes definitely", "Signs point to yes", "Most likely",
    "Reply hazy, try again", "Ask again later", "Cannot predict now", "Better not tell you now",
    "My sources say no", "Don't count on it", "My reply is no", "Outlook not so good", "Very doubtful"]
    response = random.choice(responses)
    output = claim + ": " + "\n" + response
    await ctx.send(output)

#spin the bottle
@client.command()
async def spin_the_bottle(ctx):
    list = []
    for member in client.get_all_members():
        list.insert(1, member.id)
    choice1 = random.choice(list)
    choice2 = random.choice(list)
    if choice1 == choice2:
        choice1 = random.choice(list)
    await ctx.send("<@!" + str(choice1) + ">" + " has to kiss " + "<@!" + 
                    str(choice2) + ">!" + " :face_with_peeking_eye: :face_with_hand_over_mouth: ")


#generate image from Craiyon
#@client.command()
#async def generate(ctx: commands.Context, *, prompt: str):
 #   ETA = int(time.time() + 60)
  #  async with ctx.channel.typing():
   #     msg = await ctx.send(f"Hold some hot potatoes- this may take some time \n Time estimate: <t:{ETA}:R>")
    #    generator = Craiyon()
     #   result = generator.generate(prompt)
      #  images = result.images
       # for i in images:
        #    image = BytesIO(base64.decodebytes(i.encode("utf-8")))
         #   return await msg.edit(content=prompt, file=discord.File(image, "image.png"))

#Help section
@client.command()
async def info(ctx):
    embed = discord.Embed(title="BotBot, your friendly neighborhood bot", description=f"<@!" + str(690712947659374673) + ">" + "'s" 
                        +" favorite son"+ "\n" + "Available commands: ", color=0xAA73FF)
    embed.set_author(name = client.get_user(690712947659374673), icon_url="https://64.media.tumblr.com/d3ecb9d2303b7c"+
                    "678058838c055414eb/c11902bfba580612-31/s1280x1920/3800d3598aa77888362fa75e366b72e467da6b97.jpg")
    embed.add_field(name="!poll- Create a poll", value="'poll_title' option1 option2 ... (max 10 options)", inline=False)
    embed.add_field(name="!flip- Flip a coin", value="No args necessary", inline=False)
    embed.add_field(name="!eightball- Get an 8-ball reply", value="'statement'", inline=False)
    embed.add_field(name="!affirmation- Get an affirmation", value="Fetched from API", inline=False)
    embed.add_field(name="!png ;)", value="Fetched from API", inline=True)
    embed.add_field(name="!gif ;)", value="Fetched from API", inline=True)
    embed.add_field(name="!info", value="Gives this message", inline=True)

    embed.set_thumbnail(url="https://media2.giphy.com/media/2vkUyaJW3gVQtSfs2I/giphy.gif?cid=790b7611def36"+
                         "a6613dd7f30588e7d0cd1d30f43783724ee&rid=giphy.gif&ct=s")
    await ctx.send(embed=embed)


#Check for command errors
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")


client.run(TOKEN)




