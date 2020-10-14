import discord
import random
import os
import array as arr
from discord.ext import commands
from PIL import Image
print(discord.__version__)
# code = open("dCode.txt", "r")
# TOKEN = code.read()
TOKEN = os.environ.get("TOKEN")
client = commands.Bot(command_prefix='$')

"""
Event triggers
These activate based on certain events occuring
"""


# Runs on succesful load
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='AM BOT!'))


# Triggers various things on message receive
@client.event
async def on_message(message):
    author = message.author
    content = message.content
    channel = message.channel
    if author == client.user:
        return
    if message.author.bot:
        return
    if 'OWO' in content.upper() or 'UWU' in content.upper():
        role = discord.utils.get(message.guild.roles, name="I've Been A Naughty Furry :(") # autoAssigns the Naughty Furry role
        await author.add_roles(role)
        await channel.send("What's this?")
    if content.endswith('er'):
        last = content.split()
        if not last[-1].startswith('ni'):
            if random.randint(1, 100) <= 10:
                await channel.send(last[-1]+"? I barely know her!")
    if 'VOCAL PERCUSSION ON A WHOLE NOTHER LEVEL' in content.upper():
        await channel.send("COMING FROM MY MIND")
    if "IT'S LIKE A BURNING SUNRISE" in content.upper():
        await channel.send("IT'S LIKE A BURNING SUNSET")
    if "IT'S LIKE A BURNING SUNSET" in content.upper():
        await channel.send("IT'S LIKE A BURNING SUNRISE")
    if message.content.startswith('Good Morning'):
        await channel.send("Testy Boi Online!")
    if "MORRIS" in content.upper() or "BOOK" in content.upper() or "ENGLISH" in content.upper():
        emoji = discord.utils.get(author.guild.emojis, name="morris")
        await message.add_reaction(emoji)
    if ":koichipose:" in content:
        emoji = discord.utils.get(author.guild.emojis, name="koichipose")
        await channel.send(emoji)
    if "STANGG" in content.upper():
        file = discord.File("Stangg_Twin.jpg")
        await channel.send("Don't forget his brother: **STANGG TWIN**", file=file)
    if author.id == 402611787456839701:
        if random.randint(1, 10000) <= 1:
            await author.edit(nick="Knighly")
    if channel.id == 568482919706787865:
        await channel.send("Hey there! Do you want to know about Twitch Prime? Oh! You may be asking, What's Twitch Prime? Let me tell ya! When you connect your Amazon account to your Twitch account, you can get 1 free sub to ANY streamer on Twitch, every month! Yup, and along with that, get yourself some Twitch loot! With Twitch loot, you can go ahead and get yourself some exclusive Twitch gear and your favorite games! And until April 30th, you can get yourself some Fortnite skins, with Twitch loot! So go ahead! Grab your Amazon account, grab a family or friends Amazon Prime account, and link it to your Twitch account TODAY!")
    if channel.id != 393595521333329932 and channel.id != 647470471549419531 and channel.id != 499975838276517908:
        print('{}: {}: {}: {}'.format(author, content, channel.id, author.id))
    await client.process_commands(message)


# Sends original messages when messages are edited. Disabled cause it was obnoxious
'''@client.event
async def on_message_edit(before, after):
    bMessage = before.content
    aMessage = after.content
    channel = after.channel
    if channel.id != 499975838276517908 and channel.id != 393595521333329932:
        if bMessage != aMessage:
            await channel.send("You can't escape from your sins. You originally typed "+bMessage) '''

"""
Command triggers
These run actual commands that you call
"""


# Pings bot
@client.command(brief='Pings the bot')
async def ping(ctx):
    print('working')
    await ctx.send('Pong!')


# Echoes inputted words
@client.command(brief='Echos the inputted words')
async def echo(ctx, *args):
    await ctx.channel.purge(limit=1)
    output = ''
    for word in args:
        output += word
        output += ' '
    await ctx.send(output)


# removes entered number of messages
@client.command(brief='Deletes the entered amount of messages.')
async def nuke(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send('Nuked messages.')


"""
Quotebot system commands
"""


# Adds a new quote to the quote file
@client.command(brief='Adds a quote.', description = 'Please use the format: "quote here" - name here')
async def addQ(ctx, *, arg):
    if not os.path.exists("quotes.txt"):
        f = open("quotes.txt", "w+", encoding="cp1252")
        f.write(arg + " # 1")
        await ctx.send("Added " + arg + " # 1")
    else:
        f = open("quotes.txt", "r+", encoding="cp1252")
        lastLine = f.readlines()[-1]
        lastLine = str.split(lastLine, " ")
        qNum = lastLine[-1]
        qNum = int(qNum)+1
        f.write("\n{} # {}".format(arg, qNum))
        await ctx.send("Added {} # {}".format(arg, qNum))


# Deletes a quote from the quote file
@client.command(brief='Deletes entered quote')
async def delQ(ctx, arg):
    if ctx.author.guild_permissions.administrator:
        if not os.path.exists("quotes.txt"):
            await ctx.send("There are no quotes!")
        else:
            valid = False
            f = open("quotes.txt", "r", encoding="cp1252")
            lines = f.readlines()
            f.close()
            for line in lines:
                line = line.split()
                if line[-1] == arg:
                    valid = True
            if valid:
                f = open("quotes.txt", "w+", encoding="cp1252")
                for line in lines:
                    line = line.split()
                    if line[-1] != arg:
                        if int(line[-1]) > int(arg):
                            num = int(line[-1])-1
                            line[-1] = str(num)
                            line = " ".join(line)
                            f.write(line + "\n")
                        else:
                            line = "".join(line)
                            f.write(line + "\n")
                for line in lines:
                    if not line.isspace():
                        f.write(line)
                await ctx.send("Quote removed!")
            else:
                await ctx.send("That quote doesn't exist!")
    else:
        await ctx.send("You are not authorized to graduate members!")


# Returns the numbered quote
@client.command(brief='Sends entered quote')
async def findQ(ctx, arg):
    if not os.path.exists("quotes.txt"):
        await ctx.send("There are no quotes!")
    else:
        valid = False
        f = open("quotes.txt", "r", encoding="cp1252")
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.split()
            if line[-1] == arg:
                valid = True
                seperator = " "
                result = seperator.join(line)
        if valid:
            await ctx.send(result)
        else:
            await ctx.send("That quote doesn't exist!")


# Returns a random quote from the quote file
@client.command(brief='Prints a random quote.')
async def quote(ctx):
    if not os.path.exists("quotes.txt"):
        await ctx.send("There are no quotes!")
    else:
        f = open("quotes.txt", "r", encoding="cp1252")
        line = next(f)
        for num, aline in enumerate(f, 2):
            if random.randrange(num):
                continue
            line = aline
        await ctx.send("{}".format(line))


# Sends the user ALL of the quotes
@client.command(brief='Sends you ALL quotes')
async def allQuotes(ctx):
    if not os.path.exists("quotes.txt"):
        await ctx.send("There are no quotes!")
    else:
        f = open("quotes.txt", "r", encoding="cp1252")
        everything = f.read()
        if len(everything) > 2000:
            everything1 = everything[1:1000]
            everything2 = everything[1000:]
            await ctx.author.send(everything1)
            await ctx.author.send(everything2)
        else:
            await ctx.author.send(everything)


# Sends user the entire file
@client.command(brief='Sends user the file')
async def file(ctx):
    if not os.path.exists("quotes.txt"):
        await ctx.send("There are no quotes!")
    else:
        file = discord.File("quotes.txt")
        await ctx.author.send(file=file)

"""
Role Based Commands
"""


# "graduates" target
@client.command(brief='Graduates target')
async def graduate(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        roleToRemove = discord.utils.get(ctx.guild.roles, name="High School OMEGALUL")
        roleToAdd = discord.utils.get(ctx.guild.roles, name="Education System Slaves")
        await ctx.channel.purge(limit=1)
        await member.remove_roles(roleToRemove, reason="Graduated!")
        await member.add_roles(roleToAdd, reason="Graduated!")
        await ctx.send("Congratulations, " + str(member.display_name) + "! You have escaped the shackles of High School and are prepared to ascend to the wonders of College!")
        await ctx.send(":tada: :tada: :tada: :tada: :tada:")
    else:
        await ctx.send("You are not authorized to graduate members!")


# Toggles the Endicott role so people know who's there
@client.command(brief='Toggles Endicott role.')
async def Endicott(ctx):
    author = ctx.author
    role = discord.utils.get(ctx.guild.roles, name="In Endicott")
    if role in author.roles:
        await ctx.send("You have left Endicott!")
        await author.remove_roles(role, reason="Is not in Endicott!")
    else:
        await ctx.send("Welcome to Endicott!")
        await author.add_roles(role, reason="Is in Endicott!")


# removes roles
@client.command(brief='Removes role from self')
async def remove(ctx, *, arg):
    author = ctx.author
    roleToRemove = discord.utils.get(ctx.guild.roles, name=arg)
    if arg == "I've Been A Naughty Furry :(":
        await ctx.send("You are a naughty furry.")
    else:
        await author.remove_roles(roleToRemove)
        await ctx.send("Removed role")


# Adds role
@client.command(brief='Adds role to self')
async def add(ctx, *, arg):
    author = ctx.author
    valid = True
    List = ["TOTALITARIAN DICTATORS", "Hard R Game-R", "GAELIC GOONS", "Bots", "Education System Slaves", "High School OMEGALUL", "Ravnican", "THE ANNOUNCER", "Slovenian"]
    for i in List:
        if arg == i:
            valid = False
    if valid == True:
        roleToAdd = discord.utils.get(ctx.guild.roles, name=arg)
        await author.add_roles(roleToAdd)
        await ctx.send("Added Role")
    else:
        await ctx.send("You cannot add that role.")


# Adds a role to a target user. Admin only
@client.command(brief='Admin Only')
async def addT(ctx, member: discord.Member, arg):
    author = ctx.author
    if author.guild_permissions.administrator:
        roleToAdd = discord.utils.get(ctx.guild.roles, name= arg)
        await member.add_roles(roleToAdd)
        await ctx.send("Added role to target")
    else:
        await ctx.channel.send("You do not have permission to change others roles!")


# deletes role from server
@client.command(brief='Admin Only.')
async def dRole(ctx, *, arg):
    if ctx.author.guild_permissions.administrator:
        roleToDelete = discord.utils.get(ctx.guild.roles, name=arg)
        await roleToDelete.delete()
        await ctx.channel.send("Deleted role")
    else:
        ctx.channel.send("You do not have permission to delete roles!")


# removes the furry role from all users
@client.command(brief='Admin only')
async def reform(ctx):
    if ctx.author.guild_permissions.administrator:
        role = discord.utils.get(ctx.guild.roles, name="I've Been A Naughty Furry :(")
        for guild in client.guilds:
            for member in guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
        await ctx.channel.send("The channel has been reformed!")
    else:
        await ctx.channel.send("You do not have permission to repent for your sins!")


"""
Various fun commands with no real purpose
"""


# sends a random fun fact!
@client.command(brief='Prints out a League Fact')
async def ff(ctx):
    author = ctx.author
    ff = open("FF.txt", "r")
    line = next(ff)
    for num, aline in enumerate(ff, 2):
        if random.randrange(num): continue
        line = aline
    await ctx.send(line)


# sends a random dog or cat fun fact!
@client.command(brief='Woof Woof Meow.')
async def ffd(ctx):
    author = ctx.author
    ffd = open("FFD.txt", "r")
    line = next(ffd)
    for num, aline in enumerate(ffd, 2):
        if random.randrange(num): continue
        line = aline
    await ctx.send(line)


# Rolls entered dice amount
@client.command(brief='Rolls dice. Format: xDy')
async def roll(ctx, x):
    Dnum = int(x.split('d')[0])
    max = int(x.split('d')[1])
    await ctx.send('rolling'+str(Dnum)+' d'+str(max))
    if max == 10:
        for i in range(Dnum):
            await ctx.send(random.randint(0, 9))
    else:
        for i in range(Dnum):
            await ctx.send(random.randint(1, max))


# Creates a DND Character
@client.command(brief='Rolls a DND statline and bst')
async def char(ctx):
    await ctx.send("Your stats are: ")
    statList = []
    bst = 0
    for x in range(6):
        numList = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]
        numList.remove(min(numList))
        stat = numList[0] + numList[1] + numList[2]
        statList.append(stat)
    for i in statList:
        bst = bst + i
    await ctx.send(str(statList[0]) + '\n' + str(statList[1]) + '\n' + str(statList[2]) + '\n' +
                   str(statList[3]) + '\n' + str(statList[4]) + '\n' + str(statList[5]) + "\n BST = " + str(bst))


# flips a coin
@client.command(brief='Flips a coin.')
async def flip(ctx):
    result = random.randint(1,2)
    if result == 1:
        fResult = "Heads!"
    else:
        fResult = "Tails!"
    await ctx.send(fResult)


# flips a coin but puts it backwards for some reason
@client.command(brief='Flips a coin backwards?')
async def flop(ctx):
    result = random.randint(1,2)
    if result == 1:
        fResult = "Sdaeh!"
    else:
        fResult = "Sliat!"
    await ctx.send(fResult)


# Generates a random color
@client.command(brief='Generates a random color!')
async def color(ctx):
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    img = Image.new('RGB', (128,128), (r, g, b))
    img.save("Colortemp.png", "PNG")
    file = discord.File("Colortemp.png")
    await ctx.send("LET THERE BE A COLOR! Red Value: "+str(r)+"Green Value: "+str(g)+"Blue Value: "+str(b), file=file)


# Plays rock paper scissors
@client.command(brief='Rock Paper Scissors!')
async def rps(ctx, UserChoice):
    author = ctx.author
    UserChoice = UserChoice.lower().strip()
    Choice = random.randint(1, 3)
    if Choice == 1:
        MyChoice = "Paper"
    elif Choice == 2:
        MyChoice = "Rock"
    else:
        MyChoice = "Scissors"

    if author == "IAmNotThomas#7208":
        await ctx.send("Thomas is already Winston.")

    if UserChoice == "paper":
        if MyChoice == "Paper":
            await ctx.send("I'm already Paper. It's a tie.")
        elif MyChoice == "Rock":
            await ctx.send("I've chosen Rock. You win!")
        else:
            await ctx.send("I've chosen Scissors. Git gud.")

    elif UserChoice == "rock":
        if MyChoice == "Paper":
            await ctx.send("I've chosen Paper. Git Gud.")
        elif MyChoice == "Rock":
            await ctx.send("I'm already Rock. It's a tie.")
        else:
            await ctx.send("I've chosen Scissors. You win!")

    elif UserChoice == "scissors":
        if MyChoice == "Paper":
            await ctx.send("I've chosen Paper. You win!")
        elif MyChoice == "Rock":
            await ctx.send("I've chosen rock. Git Gud")
        else:
            await ctx.send("I'm already Winston. I mean scissors. It's a tie.")

    else:
        await ctx.send("That's not how this works. Rock, Paper, or Scissors?")

client.run(TOKEN)


