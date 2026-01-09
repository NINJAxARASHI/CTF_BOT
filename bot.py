import discord
from discord.ext import commands, tasks
import os, socket
from dotenv import load_dotenv
import threading, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
load_dotenv()




global challenges
# Dictionnaire des challenges: {'nom_du_challenge': port}
# Exemple: challenges = {'Challenge 1': 30001, 'Challenge 2': 30002}
challenges = {}

global ch
# Dictionnaire des challenges pour first blood: {id: {'name': 'nom', 'solved': False}}
# Exemple: ch = {1: {'name': 'Challenge 1', 'solved': False}}
ch = {}



global connectionData
connectionData = {}


client = commands.Bot(command_prefix='.')

client.remove_command('help')

@client.event
async def on_ready():
    checkChallenges.start()
    firstBlood.start()
    await client.change_presence(status =  discord.Status.online, activity=discord.Game('Type .list to list all commands'))
    print('Bot is ready')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')






@tasks.loop(seconds=180)
async def firstBlood():
    # Si aucun challenge n'est configuré, on ne fait rien
    if not ch or len(ch) == 0:
        return

    allSolved = True
    keys = dict.keys(ch)
    for i in keys:
        if not(ch[i]['solved']):
            allSolved = False

    if(allSolved):
        return
    
    # Vérifier si le channel est configuré
    first_blood_channel = os.getenv('FIRST_BLOOD_CHANNEL')
    if not first_blood_channel:
        return
    
    channel = client.get_channel(int(first_blood_channel))
    if not channel:
        return

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    usernameStr = os.getenv('USER')
    passwordStr = os.getenv('PASSWORD')

    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options )

    print('loading')
    browser.get(('https://ctf.csivit.com/login'))
    print('loaded')

    username = browser.find_element_by_id('name-input')
    username.send_keys(usernameStr)
    password = browser.find_element_by_id('password-input')
    password.send_keys(passwordStr)

    submitBtn = browser.find_element_by_class_name('btn-outlined')
    submitBtn.click()


    for i in keys:
        
        if(ch[i]['solved']):
            continue

        browser.get(f'https://ctf.csivit.com/api/v1/challenges/{i}/solves')
        html = browser.page_source
        time.sleep(2)
        html = html[html.index('{'):html.rindex('}')+1]
        y = json.loads(html)
            
        try: y['data']
        except:
            print('key error')
            continue

        if(y['data']==[]):
            continue

        if(y['data']==[]):
            print(f'no data for {ch[i]}')
            continue

        ch[i]['solved'] = True
        # print(f'`First blood for challenge: {ch[i]["name"]} goes to {y["data"][0]["name"]}`')
        print("sending")
        await channel.send(f'```css\n🩸 First blood for .{ch[i]["name"]} goes to [{y["data"][0]["name"]}]```')
    browser.close()
    print('Completed!')


@tasks.loop(seconds = 120)
async def checkChallenges():
    # Si aucun challenge n'est configuré, on ne fait rien
    if not challenges or len(challenges) == 0:
        return
    
    print("send")
    global connectionData
    connectionData={}
    
    # Vérifier si le channel est configuré
    challenge_status_channel = os.getenv('CHALLENGE_STATUS_CHANNEL')
    if not challenge_status_channel:
        return
    
    server = socket.gethostbyname('chall.csivit.com')
    channel = client.get_channel(int(challenge_status_channel))
    if not channel:
        return
    
    embed = discord.Embed(title="Challenge Status")
    for i in challenges:
        ADDR = (server, int(challenges[i]))
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            t1 = time.time()
            socket_client.connect(ADDR)
            t2 = time.time()
            t = str(t2-t1)
            t = t[0:t.index('.')+4]
            data = f'```css\nTime: {t}s```'
            embed.add_field(name=i,value=data)
            connectionData[i]=data
        except:
            data = f"```diff\n-Unable to connect.```"
            embed.add_field(name=i, value=data)
            connectionData[i]=data

    await channel.send(embed=embed)
    print('sent')

@client.command(aliases=['Challenges', 'challenges', 'challenge'])
@commands.has_permissions(kick_members=True)
async def challengeStats(ctx):
    if not challenges or len(challenges) == 0:
        await ctx.send('Aucun challenge configuré pour le moment.')
        return
    
    if(not(len(connectionData) == len(challenges))):
        await ctx.send('Data is being collected, please wait for a few seconds!')
        return
    
    embed = discord.Embed(title='Challenge Status')
    for i in connectionData:
        embed.add_field(name=i, value=connectionData[i])
    
    await ctx.send(embed=embed)


@client.command(aliases=['Flag'])
async def flag(ctx):
    if ctx.channel.type is discord.ChannelType.private:
        await ctx.send(os.getenv('FLAG'))
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send('Sssssshhh, not here. DM me maybe ;)')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('All required arguments not passed.')
        return
    
    if isinstance(error, commands.BadArgument):
        await ctx.send('Arguments sent not correct.')
        return
    
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist.')
        return

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send('Bot does not have permissions to perform the task. Please grant permissions')
    
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Bot does not have permissions to perform the task. Please give permission')


    


client.run(os.getenv('TOKEN'))

#https://discord.com/oauth2/authorize?client_id=723828224307757178&scope=bot
