import discord 
import tweepy
import asyncio


#'Tweepy' Twitter API authentication data
consumer_key = 'otXd4O6dMglxjVBcYYNXuf1Hn'
consumer_secret = 'p6TFg2g9fqZZSvdWTmisuEknB9DlZTdv8A4QLCQ1mJPN9yU3bM'
access_key = '947878329708941313-kvHprQA9TsHGGTgMeKUDQdfIC2WYf5e'
access_secret = 'b53m9a8gx58k3RSziF8SShHZu0lx7bFNRThjAoRNya7wa'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


def frcTweets(screen_name, count):
    '''
    Requires: screen_name is a valid twitter handle, count is an int > 0, < 200
    Modifies: Nothing
    Effects: fetches urls of last 'count' tweets from input user
    '''

    alltweets = []	
    alltweets = api.user_timeline(screen_name = screen_name,count = count)
    outtweets = [tweet.id_str for tweet in alltweets]
    urls = str()
    for i in range(count):
        urls += '\n' + 'https://twitter.com/' + screen_name + '/status/' + outtweets[i]
    print(urls)
    return urls

client = discord.Client()

@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
#Messages channel when given certain commands
async def on_message(message):
    if message.content.startswith('!frc'):
        count = int(input('Count?'))
        await client.send_message(message.channel, frcTweets('FIRSTweets', count))
#Discord Bot Authentication data
client.run('Mzk3Mjc1Njg3OTY4NTcxMzkz.DSwZ9g.-wb7f3c_MK38dH5kR60hGiFpfhU')
