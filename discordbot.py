import discord 
import tweepy
import asyncio
import time
import tbapy
import datetime
import requests
import calendar
import nltk

#'Tweepy' Twitter API authentication data
consumer_key = 'otXd4O6dMglxjVBcYYNXuf1Hn'
consumer_secret = 'p6TFg2g9fqZZSvdWTmisuEknB9DlZTdv8A4QLCQ1mJPN9yU3bM'
access_key = '947878329708941313-kvHprQA9TsHGGTgMeKUDQdfIC2WYf5e'
access_secret = 'b53m9a8gx58k3RSziF8SShHZu0lx7bFNRThjAoRNya7wa'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

base_url = 'https://www.thebluealliance.com/api/v3'


team = str()


def messageTokenizor(message):

    #Tokenizes string, creates list of strings, one for each word, as well as punctuation
    tokens = nltk.word_tokenize(message)
    return tokens

def timeTillEvents(team_number):
    now = datetime.datetime.now()
    team_events = requests.get(base_url + '/team/' + team + '/events', headers = {'X-TBA-Auth-Key': '15BE7yn8Vl4sRULbIgyRlMwMJRR3d5NRRygVxBOoICx0tQjhr7KhWKPwsPOdYJwP'}).json()
    count_down = []
    for year in range(len(team_events)):
        if team_events[year]['district'] != None:
            if int(team_events[year]['district']['year']) == int(now.year):
                event_date = team_events[year]['start_date']
                current_month = now.month
                current_day = now.day
                event_month = event_date[5:-3]
                event_day = event_date[8:]
                current_month_days = calendar.monthrange(int(now.year), int(now.month))[1]
                if int(current_day) > int(event_day):
                    print('current bigger')
                    print(str(team_events[year]['name']))
                    print(event_date)
                    days_till = ((int(current_month_days) - int(current_day)) + (int(event_day) - 1)) - 2
                    months_till = int(event_month) - int(current_month) - 1
                else:
                    print('current smaller')
                    print(str(team_events[year]['name']))
                    print(event_date)
                    days_till = (int(event_day) - int(current_day))
                    months_till = int(event_month) - int(current_month)
                count = '\n' + str(months_till) + ' months ' + str(days_till) + ' days until ' + str(team_events[year]['name'])
                count_down.append(count)
    count_down.reverse()
    newMessage = str()
    for i in range(len(count_down)):
        newMessage += str(count_down[i])
    return newMessage

def userTweets(screen_name):
    '''
    Requires: screen_name is a valid twitter handle, count is an int > 0, < 200
    Modifies: Nothing
    Effects: fetches urls of last 'count' tweets from input user
    '''

    alltweets = []	
    alltweets = api.user_timeline(screen_name = screen_name,count = 5)
    outtweets = [tweet.id_str for tweet in alltweets]
    urls = str()
    with open('storedTweets.txt', 'r+') as myfile:
        openedTweets = str(myfile.read())
        for i in range(len(outtweets)):
            tempVar = str(outtweets[i])
            if tempVar not in openedTweets:
                myfile.seek(0, 2)
                myfile.write(str(outtweets[i]) + ' ')
                urls += '\n' + 'https://twitter.com/' + screen_name + '/status/' + outtweets[i]
    print(urls)
    return urls

def getMatchTime(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: Returns string with time until a team's next match
    '''
    '''
    event = getNextEvent(team_number)
    match = getNextMatch(team_number)

    currentDate = sys.date()
    matchDate = event.match.date()
    matchTime = event.match.time()
    currentTime = sys.time()

    if matchDate == currentDate:
        if currentTime < matchTime:
            timeTill = matchTime - currentTime 

    return str(timeTill)
    '''

def getRank(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns string with given team's current rank at their most recent event
    '''
    '''
    event = getNextEvent(team_number)
    rank = tba.event_rankings(event)

    return str(rank)
    '''
def getNextMatch(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns string with given team's next match at their current or closest event
    '''
    '''
    event = getNextEvent(team_number)
    matches = tba.event_matches(event, [simple/keys])
    
    for i in range(len(team.event.matches())):
        if team.event.match()
    '''
def getMatchPrediction(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns string with given team's 
    '''
def getMatchResult(match_number):
    '''
    Requires: match_number is an integer, valid match
    Modifies: Nothing
    Effects: returns string with result of given match
    '''
def setEvent(event_name):
    '''
    Requires: event_name is a string, valid name of frc event, assumes current year
    Modifies: Nothing
    Effects: returns string with result of given match
    '''

def getNextEvent(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns event object for given team's next event
    '''
    
client = discord.Client()

def getChannel(channelName):
    '''
    Requires: channelName is the name of a channel the bot is a member of
    Modifies: Nothing
    Effects: Returns a channel object with the given name

    '''
    for server in client.servers:
        for channel in server.channels:
            if channel.name == channelName:
                return channel
'''
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
'''
@client.event
#Console Feedback
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await autoSetup()
    
@client.event
#Messages channel when given certain commands
async def on_message(message):
    global team
    if message.content.startswith('!frc-tweets'):
        count = int(input('Count?'))
        await client.send_message(message.channel, userTweets('FIRSTweets', count))
    if message.content.startswith('!getChannel'):
        await client.send_message(message.channel, getChannel('frc-tweets'))
    if message.content.startswith('!TeamRank'):
        await client.send_message(message.channel, getRank(team, event))
    if message.content.startswith('!NextMatchTime'):
        await client.send_message(message.channel, getMatchTime(team_number))
    if message.content.startswith('!NextMatchPrediction'):
        await client.send_message(message.channel, getMatchPrediction(team_number))
    if message.content.startswith('!MatchResult'):
        await client.send_message(message.channel, getMatchResult(match_number))
    if message.content.startswith('!Countdown'):
        print(team)
        await client.send_message(message.channel, timeTillEvents(team))
    if message.content.startswith('!setTeam'):
        text = messageTokenizor(message.content)
        team = text[2]
        team = 'frc' + team
        await client.send_message(message.channel, 'Team was set to ' + text[2])
#Discord Bot Authentication data
client.run('Mzk3Mjc1Njg3OTY4NTcxMzkz.DSwZ9g.-wb7f3c_MK38dH5kR60hGiFpfhU')


