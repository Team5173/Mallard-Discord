import discord 
import tweepy
import asyncio
import time
import threading

#'Tweepy' Twitter API authentication data
consumer_key = 'otXd4O6dMglxjVBcYYNXuf1Hn'
consumer_secret = 'p6TFg2g9fqZZSvdWTmisuEknB9DlZTdv8A4QLCQ1mJPN9yU3bM'
access_key = '947878329708941313-kvHprQA9TsHGGTgMeKUDQdfIC2WYf5e'
access_secret = 'b53m9a8gx58k3RSziF8SShHZu0lx7bFNRThjAoRNya7wa'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def userTweets(screen_name):
    '''
    Requires: screen_name is a valid twitter handle, count is an int > 0, < 200
    Modifies: Nothing
    Effects: fetches urls of last 'count' tweets from input user
    '''

    alltweets = []	
    alltweets = api.user_timeline(screen_name = screen_name,count = 2)
    outtweets = [tweet.id_str for tweet in alltweets]
    urls = str()
    with open('storedTweets.txt', 'r+') as myfile:
        openedTweets = str(myfile.read())
        for i in range(len(outtweets)):
            tempVar = str(outtweets[i])
            print(tempVar)
            if tempVar not in openedTweets:
                myfile.seek(0, 2)
                myfile.write(str(outtweets[i]) + ' ')
                urls += '\n' + 'https://twitter.com/' + screen_name + '/status/' + outtweets[i]
    print(urls)
    return urls

client = discord.Client()

def getChannel(channelName):
    for server in client.servers:
        for channel in server.channels:
            if channel.name == channelName:
                return channel

@client.event
async def autoTweet(destination, screen_name):
    message = userTweets(screen_name)
    if message != '':
        await client.send_message(destination, content = message )

@client.event
async def autoSetup():
    screen_name = input('User?')
    channelID = getChannel(input('Channel?'))
    while(True):
        await autoTweet(channelID, screen_name)
        time.sleep(2)

@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await autoSetup()
    
@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('!frc'):
        count = int(input('Count?'))
        await client.send_message(message.channel, userTweets('FIRSTweets', count))
    if message.content.startswith('!getC'):
        await client.send_message(message.channel, getChannelID('frc-tweets'))
#Discord Bot Authentication data
client.run('Mzk3Mjc1Njg3OTY4NTcxMzkz.DSwZ9g.-wb7f3c_MK38dH5kR60hGiFpfhU')


