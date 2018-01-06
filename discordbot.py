import discord 
import tweepy
import asyncio
import time
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
header = {'X-TBA-Auth-Key': '15BE7yn8Vl4sRULbIgyRlMwMJRR3d5NRRygVxBOoICx0tQjhr7KhWKPwsPOdYJwP'}

team = str()


def messageTokenizor(message):


    tokens = nltk.word_tokenize(message)
    return tokens

def timeTillEvents(team_number):
    now = datetime.datetime.now()
    team_events = requests.get(base_url + '/team/' + team + '/events', header).json()
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

def getMatchTime(match):
    '''
    Requires: match is a match object, valid frc team number
    Modifies: Nothing
    Effects: Returns string match time
    '''
    full_date = datetime.datetime.fromtimestamp(match['predicted_time']).strftime('%H:%M:%S %Y-%m-%d')
    date = full_date[8:]
    time = full_date[:-10]
    message = time + ' on ' + date
    return message
def getRank(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns string with given team's current rank at their most recent event
    '''
    event = getNextEvent(team_number)
    eventKey = event['key']
    rankings = requests.get(base_url + '/event/' + eventKey + '/rankings', header).json()
    for i in range(len(rankings['rankings'])):
        if rankings['rankings'][i]['team_key'] == team_number:
            return 'Team ' + team + ' is currently rank ' + rankings['rankings'][i]['rank'] + ' at the ' + event['name'] + ' event.'

def teamInfo(team_number):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    
    event = getNextEvent(team)
    message = ('Team ' + team + ' has been a member of FIRST Robotics for' + numYears(team_number)
    + '. They are currently ranked ' + getDistrictRank(team) + ' in their district, ' + getTeamDistrict(team))



def nextMatchInfo(match):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    event = getNextEvent(team)
    message = ('Team ' + team[3:] + '\'s next match, number ' + str(match['match_number']) + ' at '
    + event['name'] + ', begins in ' + getTimeTillMatch(match) + ' at ' + str(getMatchTime(match))
    + ' on the ' + getAllianceColor(match) + ' alliance with alliance members ' + getAllianceMembers(match)
    + ' against' + oppositeAlliance(match) + matchPrediction(match))
    return message

def getTimeTillMatch(match):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    now = datetime.datetime.now()
    stamp = int(now.timestamp())
    timeTill = match['predicted_time'] - stamp
    weeks = timeTill / 60 / 60 / 24 / 7
    days = (weeks % 1) * 7
    hours = (days % 1) * 24
    minutes = (hours % 1) * 60
    message = str(int(weeks)) + ' weeks ' + str(int(days)) + ' days ' + str(int(hours)) + ' hours ' + str(int(minutes)) + ' minutes '
    return message
def getAllianceColor(match):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    color = str()
    for i in range(len(match['alliances']['blue']['team_keys'])):
        if match['alliances']['blue']['team_keys'][i] == team:
            color = 'blue'
    if color != 'blue':
        color = 'red'
    return color

def getAllianceMembers(match):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    alli = str()
    color = getAllianceColor(match)
    if color == 'blue':
        for i in range(len(match['alliances']['blue']['team_keys'])):
            alli += ' ' + match['alliances']['blue']['team_keys'][i][3:] + ', '
    else:
        for i in range(len(match['alliances']['red']['team_keys'])):
            alli += ' ' + match['alliances']['red']['team_keys'][i][3:] + ', '
    return alli
        
def oppositeAlliance(match):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    opp = str()
    color = getAllianceColor(match)
    if color == 'blue':
        for i in range(len(match['alliances']['red']['team_keys'])):
            opp += ' ' + match['alliances']['red']['team_keys'][i][3:] +', '
    else:
        for i in range(len(match['alliances']['blue']['team_keys'])):
            opp += ' ' + match['alliances']['blue']['team_keys'][i][3:] + ', '

    return opp

def getNextMatch(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns string with given team's next match at their current or closest event
    '''

    event = getNextEvent(team_number)
    match_times = []
    now = datetime.datetime.now()
    stamp = int(now.timestamp())
    times = {}
    #key = event['key']
    key = '2017miwmi'
    team_matches = requests.get(base_url + '/team/' + team + '/event/' + key + '/matches', header).json()
    for i in range(len(team_matches)):
        match_times.append(team_matches[i]['predicted_time'])
    for time in range(len(match_times)):
        times[match_times[time] - stamp] = team_matches[i]
    smallest = stamp
    for key in times.keys():
        if (key < smallest):
            smallest = key
    return times[smallest]
    
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
    
def getNextEvent(team_number):
    '''
    Requires: team_number is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns event object for given team's next event
    '''
    now = datetime.datetime.now()
    team_events = requests.get(base_url + '/team/' + team + '/events', header).json()
    dates = {}
    dt = []
    for year in range(len(team_events)):
        if team_events[year]['district'] != None:
            if int(team_events[year]['district']['year']) == int(now.year):
                event_date = team_events[year]['start_date']
                event_month = event_date[5:-3]
                event_day = event_date[8:]
                current_day = now.day
                current_month = now.month
                cD = str(current_month) + str(event_day)
                cD = int(cD)
                eD = str(event_month) + str(event_day)
                eD = int(eD)
                if cD < eD:
                    dates[eD] = team_events[year]
                    dt.append(eD)
    smallest = 1231
    for i in range(len(dt)):
        if (dt[i] < smallest):
            smallest = dt[i]
            
    return dates[smallest]

    
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
        await client.send_message(message.channel, getRank(team))
    if message.content.startswith('!NextMatchTime'):
        await client.send_message(message.channel, getMatchTime(team))
    if message.content.startswith('!NextMatchPrediction'):
        await client.send_message(message.channel, getMatchPrediction(team))
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
    if message.content.startswith('!NextEvent'):
        await client.send_message(message.channel, getNextEvent(team))
    if message.content.startswith('!NextMatch'):
        await client.send_message(message.channel, nextMatchInfo(getNextMatch(team)))
#Discord Bot Authentication data
client.run('Mzk3Mjc1Njg3OTY4NTcxMzkz.DSwZ9g.-wb7f3c_MK38dH5kR60hGiFpfhU')


