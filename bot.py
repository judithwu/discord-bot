import os, discord, random, datetime, aiohttp, asyncio, json
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    #await client.change_presence(activity=discord.Activity(
        #name = "the stars~~", type = discord.ActivityType.watching))
    guild = discord.utils.get(client.guilds, name=GUILD)
    print (f'{client.user} is connected on {guild}!')
    change_status.start()
    birthday.start()

#Rotate through status "watching"
status = cycle(["the stars", "the sea", "a movie", "youtube", "people"])
@tasks.loop(minutes=5)
async def change_status():
    await client.change_presence(activity=discord.Activity(name = next(status), type = discord.ActivityType.watching))

#Check connection command
@client.command()
async def ping(ctx):
    await ctx.channel.send("<@" + str(client.user.id) + ">" + " is connected on " 
                            + str(discord.utils.get(client.guilds, name=GUILD)))

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

#Find number of messages sent by specific person
#@client.command()
#async def count(ctx, month: int):
 # now = datetime.datetime.now()
  #year = now.year
  #channel = client.get_channel(839267199911067658)
  #async for message in channel.history(after=datetime.datetime(year, month, date))



#Get a scrapbook image
@client.command()
async def throwback(ctx, a_year: int, a_month: int, a_date: 
                  int, b_year: int, b_month: int, b_date: int):
    attachments = [] #nested list of list
    
    channel = client.get_channel(774788204745457724)

    async for message in channel.history(after=datetime.datetime(a_year, a_month, a_date), 
                                            before=datetime.datetime(b_year, b_month, b_date)):
        if message.attachments: #check for messages that have attachments
            picture = [] #create empty list to be nested
            picture.insert(1, message.attachments[0].url) #insert attachment in nested list
            picture.insert(1, "Date: " + str(message.created_at.month) + "/" + 
                        str(message.created_at.day) + "/" + str(message.created_at.year)) #insert date of message in nested list
            attachments.insert(1, picture) #add list of attachment, date to outer list

    picture = random.choice(attachments) #select random choice from attachments
  

    embed = discord.Embed()
    embed.set_image(url=str(picture[0])) #set image
    embed.title = picture[1] #set the date
   
    embed.color = 0x1FDDF0
    await ctx.send(embed=embed)


#Eightball command
@client.command()
async def eightball(ctx, claim):
    responses = ["As I see it, yes", "Without a doubt", "Yes definitely", "Signs point to yes", "Most likely",
    "Reply hazy, try again", "Ask again later", "Cannot predict now", "Better not tell you now",
    "My sources say no", "Don't count on it", "My reply is no", "Outlook not so good", "Very doubtful"]
    response = random.choice(responses)
    output = claim + ": " + "\n" + response
    await ctx.send(output)

#Schedule birthday pings
@tasks.loop(seconds=86400)
async def birthday():
    now = datetime.datetime.now() #get current date

    #retrieve current month and day
    month = now.month
    day = now.day

    channel = client.get_channel(705996528581345327)

    with open("dates.json", "r") as f:
        data = json.load(f) #read in data
        for date in data["dates"]: #loop through dates
            if date["month"] == month and date["day"] == day: 
                await channel.send("happy birthday!!!! :confetti_ball: :tada: <@!" + str(date["entity"]) + ">")
                break 

#Help section
@client.command()
async def info(ctx):
    embed = discord.Embed(title="BotBot, your friendly neighborhood bot", description=f"Available commands: ", color=0xAA73FF)
    embed.set_author(name = client.get_user(690712947659374673), icon_url="https://64.media.tumblr.com/d3ecb9d2303b7c"+
                    "678058838c055414eb/c11902bfba580612-31/s1280x1920/3800d3598aa77888362fa75e366b72e467da6b97.jpg")
    embed.add_field(name="!poll- Create a poll", value="'poll_title' option1 option2 ... (max 10 options)", inline=False)
    embed.add_field(name="!flip- Flip a coin", value="No args necessary", inline=False)
    embed.add_field(name="!eightball- Get an 8-ball reply", value="'statement'", inline=False)
    embed.add_field(name="!throwback- Pull random scrapbook image", value="yr month date yr month date (format is in from to to)", inline=False)
    embed.add_field(name="!info", value="Gives this message", inline=True)

    embed.set_thumbnail(url="https://media2.giphy.com/media/2vkUyaJW3gVQtSfs2I/giphy.gif?cid=790b7611def36"+
                         "a6613dd7f30588e7d0cd1d30f43783724ee&rid=giphy.gif&ct=s")
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")



client.run(TOKEN)