import discord 
import tweepy
import asyncio
import time
import datetime
import requests
import calendar
import nltk

with open('discordToken.txt', 'r+') as myfile:
        token = str(myfile.read())
with open('TBAkey.txt', 'r+') as myfile:
        TBAkey = str(myfile.read())

base_url = 'https://www.thebluealliance.com/api/v3'
header = {'X-TBA-Auth-Key': TBAkey}
teams = str()


def messageTokenizor(message):
    '''
    Requires: message is a string
    Modifies: Nothing
    Effects: uses nltk to 'tokenize' then return the input message
    '''
    #tokenizes the given string
    tokens = nltk.word_tokenize(message)
    #returns tokenized message
    return tokens

def timeTillEvents(team_key):
    '''
    Requires: team_key is a valid TBA FRC team_key
    Modifies: Nothing
    Effects: Returns a string with countdowns until all of a teams event's this year
    '''
    #sets the current time using the datetime lib
    now = datetime.datetime.now()
    #creates a list of FRC events for the given team using TBA api and the python requests lib
    team_events = requests.get(base_url + '/team/' + team_key + '/events', header).json()
    #list of countdowns that will be populated later
    count_down = []
    #loops through the given team's events
    for year in range(len(team_events)):
        #checks it's a district event
        if team_events[year]['district'] != None:
            #checks that the given event is taking place this year
            if int(team_events[year]['district']['year']) == int(now.year):
                #sets the date of the event
                event_date = team_events[year]['start_date']
                current_month = now.month
                current_day = now.day
                #isolates the event month from the event_date string
                event_month = event_date[5:-3]
                #isolates the event day of the month from the event_date string
                event_day = event_date[8:]
                #gets the number of days in the current month
                current_month_days = calendar.monthrange(int(now.year), int(now.month))[1]
                
                if int(current_day) > int(event_day):
                    days_till = ((int(current_month_days) - int(current_day)) + (int(event_day) - 1)) - 2
                    months_till = int(event_month) - int(current_month) - 1
                else:
                    days_till = (int(event_day) - int(current_day))
                    months_till = int(event_month) - int(current_month)
                count = '\n' + str(months_till) + ' months ' + str(days_till) + ' days until ' + str(team_events[year]['name'])
                count_down.append(count)
    #reorders the list of countdown till events in chronological order
    count_down.reverse()
    newMessage = str()
    for i in range(len(count_down)):
        newMessage += str(count_down[i])
    return newMessage

def timeTillEvent(event_key):
    '''
    Requires: 
    Effects: 
    '''
    #Sets the current time
    now = datetime.datetime.now()
    count_down = []
    #Gets the event object from TBA
    event = requests.get(base_url + '/event/' + event_key, header).json()
    #Gets the date the event takes place on
    event_date = event['start_date']
    #Gets the current month 
    current_month = now.month
    #Gets the current day of the month
    current_day = now.day
    #Gets the event month
    event_month = event_date[5:-3]
    #Gets the day of the month of the event
    event_day = event_date[8:]
    #Gets the total number of days in the current month
    current_month_days = calendar.monthrange(int(now.year), int(now.month))[1]
    
    if int(current_day) > int(event_day):
        days_till = ((int(current_month_days) - int(current_day)) + (int(event_day) - 1)) - 2
        months_till = int(event_month) - int(current_month) - 1
    else:
        days_till = (int(event_day) - int(current_day))
        months_till = int(event_month) - int(current_month)
    message = '\n' + str(months_till) + ' months ' + str(days_till) + ' days'
    return message

def userTweets(screen_name):
    '''
    Requires: screen_name is a valid twitter handle, count is an int > 0, < 200
    Effects: fetches urls of last 'count' tweets from input user
    '''
    #Create empty list to store user tweets
    alltweets = []
    #fills list with given user tweets
    alltweets = api.user_timeline(screen_name = screen_name,count = 5)
    #populates new list with the ID of each tweet in alltweets
    outtweets = [tweet.id_str for tweet in alltweets]
    urls = str()
    #Opens a file that stores list of tweets that have already been sent
    with open('storedTweets.txt', 'r+') as myfile:
        #Reads the contents of the text file into a python object
        openedTweets = str(myfile.read())
        #Iterates through the list of tweet IDs
        for i in range(len(outtweets)):
            #Sets a temporary variable to the current ID being referenced by the iterator
            tempVar = str(outtweets[i])
            #Checks that that ID is not in the text file log
            if tempVar not in openedTweets:
                #Writes the current ID to the end of the text file
                myfile.seek(0, 2)
                myfile.write(str(outtweets[i]) + ' ')
                #Uses the ID  to add to a string of URLs
                urls += '\n' + 'https://twitter.com/' + str(screen_name) + '/status/' + str(outtweets[i])
    return urls

def getMatchTime(match):
    '''
    Requires: match is a match object, valid frc team number
    Effects: Returns string match time
    '''
    #Gets the date and time of a given match, in UNIX time, and converts to human readable time
    full_date = datetime.datetime.fromtimestamp(match['predicted_time']).strftime('%H:%M:%S %Y-%m-%d')
    #Parse full_date, breaking it up into date and time
    date = full_date[8:]
    time = full_date[:-10]
    message = time + ' on ' + date
    return message

def teamInfo(team_key):
    '''
    Requires: 
    Effects: 
    '''



    
    #Gets the next event for the given team
    event = getNextEvent(team_key)
    #Contsructs a message about the given team's stats
    message = ('Team ' + team[3:] + ', ' + teamName(team_key) + ', '
               + ' has been a member of FIRST Robotics for ' + numYears(team_key)
               + '. They are currently ranked ' + str(getDistrictRank(team_key)) + ' in their district, '
               + getTeamDistrict(team_key) + ' and ' + str(getEventRank(team_key))
               + ' at their most recent event, with a WTL record of ' + winTieLoss(team_key))
    return message

def teamName(team_key):
    '''
    Requires: 
    Effects: 
    '''
    #Gets the team nickname, like "Roborangers", "NC Gears", or "Robohawks"
    nickname = requests.get(base_url + '/team/' + team_key, header).json()
    return nickname['nickname']

def numYears(team_key):
    '''
    Requires: 
    Effects: 
    '''
    #Gets the number of years the team has been a member of FIRST
    years = requests.get(base_url + '/team/' + team_key + '/years_participated', header).json()
    return str(len(years)) + ' year(s)'

def winTieLoss(team_key):
    '''
    Requires: 
    Effects: 
    '''
    #Gets event key of latest event 
    #event_key = getNextEvent(team_key)
    event_key = '2017miwmi'
    #Get team stats at event
    events = requests.get(base_url + '/team/' + team_key + '/event/' + event_key + '/status', header).json()
    #Gets team WTL at event
    wtl = events['qual']['ranking']['record']
    wins = wtl['wins']
    losses = wtl['losses']
    ties = wtl['ties']
    winTieLoss = (str(wins) + '-' + str(ties) + '-' + str(losses))
    return winTieLoss

def nextMatchInfo(match):
    '''
    Requires: 
    Effects: 
    '''
    event = getNextEvent(team)

    embed=discord.Embed(title='**' + team[3:] + ' next match, number ' + str(match['match_number']) + '**', color=0xea0006)
    embed.add_field(name='__Time Till Match:__', value=getTimeTillMatch(match), inline=False)
    embed.add_field(name='__Match Start Time:__', value=str(getMatchTime(match)), inline=True)
    #embed.add_field(name='Match Start Date', value=xxxx-xx-xx, inline=True)
    embed.add_field(name='__Alliance Color:__', value=getAllianceColor(match)[0].upper() + getAllianceColor(match)[1:], inline=False)
    embed.add_field(name='__Red Alliance Members:__', value=getAllianceMembers(match), inline=True)
    embed.add_field(name='__Blue Alliance Members:__', value=oppositeAlliance(match), inline=True)
    embed.add_field(name='__Match Prediction:__', value=predictionMessage(matchPrediction(match)), inline=False)

    return embed

def matchInfo(match, event_key):
    embed=discord.Embed(title="EVENT_NAME, match number: MATCH_NUMBER", description="Match number MATCH_NUMBER, at EVENT_NAME event.", color=0x45fc07)
    embed.set_thumbnail(url="https://raw.githubusercontent.com/Team5173/Mallard-Discord/master/frc-game.png")
    embed.add_field(name='Competition Level', value=match['comp_level'], inline=False)
    embed.add_field(name='Winner', value=match['winning_alliance'], inline=True)
    embed.add_field(name='Score', value='Red ' + str(match['alliances']['red']['score']) + '-' + 'Blue ' + str(match['alliances']['blue']['score']), inline=True)
    embed.add_field(name='Red Alliance: ', value=getAllianceMembersEmbed(match, 'red', event_key), inline=True)
    embed.add_field(name='Blue Alliance: ', value=getAllianceMembersEmbed(match, 'blue', event_key), inline=True)
    if type(match['videos']) is list:
        embed.add_field(name='Video: ', value='No videos available', inline=True)
    else:
        embed.add_field(name='Video: ', value='www.youtube.com/watch?v=' + str(match['videos']['key']), inline=True)
    return embed


def getMatch(match_key):
    match = requests.get(base_url + '/match/' + match_key, header).json()
    return match
    
def nextEventInfo():
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    event = getNextEvent(team)
    message = 'Team ' + team[3:] + '\'s next event, ' + event['name'] + ' at ' + event['location_name'] + ' in ' + timeTillEvent(event['key'])
    return message

def predictionMessage(match_prediction):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    if match_prediction == 'none':
        message = 'There is currently no match perdiction available.'
        return message
    winner = match_prediction['winning_alliance']
    message = (winner +  ' alliance predicted to win with a score of '
               + str(int(match_prediction[winner]['score'])) + '-'
               + str(int(match_prediction[oppositeColor(winner)]['score'])))
    
    return message

def matchPrediction(match):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    event = getNextEvent(team)
    event_key = event['key']
    #event_key = '2017miwmi'
    match_key = match['key']
    predictions = requests.get(base_url + '/event/' + event_key + '/predictions', header).json()
    print(predictions)
    if predictions is None:
        return 'none'
    
    match_prediction = []
    for key in predictions['match_predictions']['playoff'].keys():
        if key == match_key:
            match_prediction = predictions['match_predictions']['playoff'][key] 
    for key in predictions['match_predictions']['qual'].keys():
        if key == match_key:
            match_prediction = predictions['match_predictions']['qual'][key]
    return match_prediction
    

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
    message = (str(int(weeks)) + ' weeks ' + str(int(days)) + ' days '
    + str(int(hours)) + ' hours ' + str(int(minutes)) + ' minutes ')
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
            alli += (' Team ' + match['alliances']['blue']['team_keys'][i][3:] + ', '
                     + teamName(match['alliances']['blue']['team_keys'][i])  + ', '
                     + getEventRank(match['alliances']['blue']['team_keys'][i]))            
    else:
        for i in range(len(match['alliances']['red']['team_keys'])):
            alli += (' Team ' + match['alliances']['red']['team_keys'][i][3:] + ', '
                     + teamName(match['alliances']['red']['team_keys'][i])  + ', '
                     + getEventRank(match['alliances']['red']['team_keys'][i]))
    return alli

def getAllianceMembersEmbed(match, color, event_key):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    alli = str()
    if color == 'blue':
        for i in range(len(match['alliances']['blue']['team_keys'])):
            alli += (' Team ' + match['alliances']['blue']['team_keys'][i][3:] + ', '
                     + teamName(match['alliances']['blue']['team_keys'][i])  + ', '
                     + str(getEventRankEmbed(match['alliances']['blue']['team_keys'][i], event_key)))            
    else:
        for i in range(len(match['alliances']['red']['team_keys'])):
            alli += (' Team ' + match['alliances']['red']['team_keys'][i][3:] + ', '
                     + teamName(match['alliances']['red']['team_keys'][i])  + ', '
                     + str(getEventRankEmbed(match['alliances']['red']['team_keys'][i], event_key)))
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
            opp += (' Team ' + match['alliances']['red']['team_keys'][i][3:] +', '
                    + teamName(match['alliances']['red']['team_keys'][i])  + ', '
                    + getEventRank(match['alliances']['red']['team_keys'][i]))
    else:
        for i in range(len(match['alliances']['blue']['team_keys'])):
            opp += (' Team ' + match['alliances']['blue']['team_keys'][i][3:] + ', '
                    + teamName(match['alliances']['blue']['team_keys'][i])  + ', '
                    + getEventRank(match['alliances']['blue']['team_keys'][i]))
    return opp

def getNextMatch(team_key):
    '''
    Requires: team_key is an integer, valid frc team number
    Modifies: Nothing
    Effects: returns string with given team's next match at their current or closest event
    '''

    event = getNextEvent(team_key)
    match_times = []
    now = datetime.datetime.now()
    stamp = int(now.timestamp())
    times = {}
    key = event['key']
    #key = '2017miwmi'
    team_matches = requests.get(base_url + '/team/' + team + '/event/' + key + '/matches', header).json()
    for i in range(len(team_matches)):
        match_times.append(team_matches[i]['predicted_time'])
    for time in range(len(match_times)):
        times[match_times[time] - stamp] = team_matches[time]
    smallest = stamp    
    for key in times.keys():
        if (key < smallest) and (key > 0):
            smallest = key
    return times[smallest]

def oppositeColor(color):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    if color == 'red':
        return 'blue'
    else:
        return 'red'

def getMatchResult(match_key):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    members = str()
    enemy = str()
    match = requests.get(base_url + '/match/' + match_key, header).json()
    print(match)
    match_num = match['match_number']
    winningAlliance = match['winning_alliance']
    for i in range(len(match['alliances'][winningAlliance]['team_keys'])):
        members += (' ' + match['alliances'][winningAlliance]['team_keys'][i][3:] + ', '
                    + ' rank ' + getEventRank(match['alliances'][winningAlliance]['team_keys'][i]))
    for i in range(len(match['alliances'][oppositeColor(winningAlliance)]['team_keys'])):
        enemy += (' ' + match['alliances'][oppositeColor(winningAlliance)]['team_keys'][i][3:] + ', '
                    + ' rank ' + getEventRank(match['alliances'][oppositeColor(winningAlliance)]['team_keys'][i]))

    if winningAlliance == 'blue':
        score = str(match['alliances'][winningAlliance]['score']) + '-' + str(match['alliances']['red']['score'])
    else:
        score = str(match['alliances'][winningAlliance]['score']) + '-' + str(match['alliances']['blue']['score'])
               
    message = ('Match number ' + str(match_num) + ' concluded with a ' + str(winningAlliance)
               + ' win, with alliance members' + str(members) + 'victorious over '
               + oppositeColor(winningAlliance) + ' alliance, with members ' + str(enemy))
    return message

def getEventRankEmbed(team_key, event_key):
    event = requests.get(base_url + '/team/' + team_key + '/event/' + event_key + '/status', header).json()
    return event['qual']['ranking']['rank']
               
def getEventRank(team_key):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    event = getNextEvent(team_key)
    eventKey = event['key']
    #eventKey = '2017miwmi'
    rankings = requests.get(base_url + '/event/' + eventKey + '/rankings', header).json()
    for i in range(len(rankings['rankings'])):
        if rankings['rankings'][i]['team_key'] == team_key:
            return ' currently rank ' + str(rankings['rankings'][i]['rank']) + ', '

def getTeamDistrict(team_key):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    now = datetime.datetime.now()
    districts = requests.get(base_url + '/team/' + team_key + '/districts', header).json()
    for i in range(len(districts)):
        if districts[i]['year'] == now.year:
            return districts[i]['key']

def getTeamDistrictName(team_key):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    now = datetime.datetime.now()
    districts = requests.get(base_url + '/team/' + team_key + '/districts', header).json()
    for i in range(len(districts)):
        if districts[i]['year'] == now.year:
            return districts[i]['display_name']

def getDistrictRank(team_key):
    '''
    Requires: 
    Modifies: Nothing
    Effects: 
    '''
    #Gets team's district
    district_key = getTeamDistrict(team_key)
    #district_key = '2017fim'
    #Gets ranks in district
    rankings = requests.get(base_url + '/district/' + district_key + '/rankings', header).json()
    #return team's rank in district
    for i in range(len(rankings)):
        if rankings[i]['team_key'] == team_key:
            return rankings[i]['rank']
    
def getNextEvent(team_key):
    '''
    Requires: team_key is an integer, valid frc team number
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
                if (cD < eD) or (cD == eD) or (cD == eD -1):
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
    global team
    
    if message.content.startswith('!frc-tweets'):
        count = int(input('Screen name??'))
        await client.send_message(message.channel, userTweets(screen_name))
    if message.content.startswith('mal! rank'):
        await client.send_message(message.channel, getEventRank(team))
    if message.content.startswith('mal! district'):
        await client.send_message(message.channel, getDistrictRank(team))
    if message.content.startswith('mal! team stats'):
        await client.send_message(message.channel, teamInfo(team))
    if message.content.startswith('mal! match result'):
        text = messageTokenizor(message.content)
        match_key = text[4]
        event_key = text[4].split('_')[0]
        await client.send_message(message.channel, embed=matchInfo(getMatch(match_key), event_key))
    if message.content.startswith('mal! countdown'):
        await client.send_message(message.channel, timeTillEvents(team))
    if message.content.startswith('mal! set team'):
        text = messageTokenizor(message.content)
        team = text[4]
        team = 'frc' + team
        embed=discord.Embed(description= 'Team was set to ' + text[4], color=0xea0006)
        embed.set_author(name=teamName(team))
        await client.send_message(message.channel, embed=embed)
    if message.content.startswith('mal! next event'):
        await client.send_message(message.channel, nextEventInfo())
    if message.content.startswith('mal! next match'):
        await client.send_message(message.channel, embed=nextMatchInfo(getNextMatch(team)))
    if message.content.startswith('!LastCommit'):
        await client.send_message(message.channel, lastCommit())
#Discord Bot Authentication data
client.run(token)
