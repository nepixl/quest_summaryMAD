import json
import requests
import time
import locale
import configparser
import pymysql

config = configparser.ConfigParser()
config.read('config.ini')

dbip = config.get('CONFIG', 'DBIP')
dbuser = config.get('CONFIG', 'DBUSER')
dbpw = config.get('CONFIG', 'DBPW')
dbname = config.get('CONFIG', 'DBNAME')
token = config.get('CONFIG', 'TOKEN')
chat_id = config.get('CONFIG', 'CHATID')
mapmode = config.get('CONFIG', 'MAPMODE')
mapurl = config.get('CONFIG', 'MAPURL')
madminurl = config.get('CONFIG', 'MADMINURL')
localeSetting = config.get('CONFIG', 'LOCALE')
madlanguage = config.get('CONFIG', 'MADLANGUAGE')
pokemonIds = config.get('CONFIG', 'POKEMON')
rarecandy = config.get('CONFIG', 'RARECANDY')
silverpinap = config.get('CONFIG', 'silverpinap')
stardust = config.get('CONFIG', 'STARDUST')
user = config.get('CONFIG', 'USER')
passw = config.get('CONFIG', 'PASS')

pokemonIds = pokemonIds.split(',')
stardust = stardust.split(',')
rarecandy = rarecandy.split(',')
silverpinap = silverpinap.split(',')

text_file = open('text.txt', 'r', encoding='utf-8')
text = text_file.read()

candyList = []
silverpinapList = []
starList = []
pokeList = []


for k in rarecandy:
    candyList.append([])
	
for k in silverpinap:
    silverpinapList.append([])
	
for k in stardust:
    starList.append([])
	
for k in pokemonIds:
    pokeList.append(False)

if user != "":
    json_input = requests.get(madminurl + '/get_quests', auth=(user, passw))
else:
    json_input = requests.get(madminurl + '/get_quests')

data = json_input.json()

if madlanguage == "":
	print('Missing madlanguage in config.ini\n', end='', flush=True)
	exit()
	
if mapmode == "":
	print('Missing mapmode in config.ini\n', end='', flush=True)
	exit()
	
if dbuser == "":
	print('Missing some databasesettings in config.ini\n', end='', flush=True)
	exit()
	
# Open database connection
db = pymysql.connect(dbip,dbuser,dbpw,dbname)

# prepare a cursor object
cursor = db.cursor()

# count pokestop in DB.
cursor.execute("SELECT COUNT(*) FROM pokestop")

# Fetch a single row, call it amountpokestops.
amountpokestops = cursor.fetchone()

# Count questpokemon in db
cursor.execute("select COUNT(*) from trs_quest where not quest_pokemon_id = 0")
countpkm = cursor.fetchone()

# Done. disconnect
db.close()
	
if madlanguage == "DE":
    if mapmode == "CUSTOM":
        link = ''
        for d in data:
            if d['quest_reward_type'] == "Item":
                if d['item_type'] == "Sonderbonbon":
                    if str(d['item_amount']) in rarecandy:
                        link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                        d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n'
                        candyList[rarecandy.index(d['item_amount'])].append(link)
					
                if d['item_type'] == "Silberne Sananabeere":
                    if str(d['item_amount']) in silverpinap:
                        link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                        d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n'
                        silverpinapList[silverpinap.index(d['item_amount'])].append(link)
		
            elif d['quest_reward_type'] == 'Sternenstaub':
                if str(d['item_amount']) in stardust:
                    link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                     d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n'
                    starList[stardust.index(d['item_amount'])].append(link)
       
            elif d['quest_reward_type'] == 'Pokemon':
                if str(d['pokemon_id']) in pokemonIds:
                    link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                    d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n' + '$' + d['pokemon_id'] + '$'
                    text = text.replace('$' + d['pokemon_id'] + '$', link)
                    pokeList[pokemonIds.index(d['pokemon_id'])] = True

    elif mapmode == "GMAPS":
        link = ''
        for d in data:
            if d['quest_reward_type'] == "Item":
                if d['item_type'] == "Sonderbonbon":
                    if str(d['item_amount']) in rarecandy:
                        link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(
                        d['longitude']) + '%22>' + d['name'] + '</a>\n'
                        candyList[rarecandy.index(d['item_amount'])].append(link)		
					
                elif d['item_type'] == "Silberne Sananabeere":
                    if str(d['item_amount']) in silverpinap:
                        link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(
                        d['longitude']) + '%22>' + d['name'] + '</a>\n'
                        silverpinapList[silverpinap.index(d['item_amount'])].append(link)
				
            elif d['quest_reward_type'] == 'Sternenstaub':
                    if str(d['item_amount']) in stardust:
                        link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(
                        d['longitude']) + '%22>' + d['name'] + '</a>\n'
                        starList[stardust.index(d['item_amount'])].append(link)
						
            elif d['quest_reward_type'] == 'Pokemon':
                if str(d['pokemon_id']) in pokemonIds:
                    link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(d['longitude']) + '%22>' + d['name'] + '</a>\n' + '$' + d['pokemon_id'] + '$'
                    text = text.replace('$' + d['pokemon_id'] + '$', link)
                    pokeList[pokemonIds.index(d['pokemon_id'])] = True
				
if madlanguage == "EN":
    if mapmode == "CUSTOM":
        link = ''
        for d in data:
            if d['quest_reward_type'] == "Item":
                if d['item_type'] == "Rare Candy":
                    if str(d['item_amount']) in rarecandy:
                        link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                        d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n'
                        candyList[rarecandy.index(d['item_amount'])].append(link)
					
                elif d['item_type'] == "Silver Pinap":
                    if str(d['item_amount']) in silverpinap:
                        link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                        d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n'
                        silverpinapList[silverpinap.index(d['item_amount'])].append(link)
		
                elif d['quest_reward_type'] == 'Stardust':
                    if str(d['item_amount']) in stardust:
                        link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                        d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n'
                        starList[stardust.index(d['item_amount'])].append(link)
       
            elif d['quest_reward_type'] == 'Pokemon':
                if str(d['pokemon_id']) in pokemonIds:
                    link = '<a href=%22' + mapurl + '/?lat=' + str(d['latitude']) + str('%26lon=') + str(
                    d['longitude']) + '%26zoom=16%22>' + d['name'] + '</a>\n' + '$' + d['pokemon_id'] + '$'
                    text = text.replace('$' + d['pokemon_id'] + '$', link)
                    pokeList[pokemonIds.index(d['pokemon_id'])] = True

    if mapmode == "GMAPS":
        link = ''
        for d in data:
            if d['quest_reward_type'] == "Item":
                if d['item_type'] == "Rare Candy":
                    if str(d['item_amount']) in rarecandy:
                            link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(
                            d['longitude']) + '%22>' + d['name'] + '</a>\n'
                            candyList[rarecandy.index(d['item_amount'])].append(link)		
					
                elif d['item_type'] == "Silver Pinap":
                    if str(d['item_amount']) in silverpinap:
                            link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(
                            d['longitude']) + '%22>' + d['name'] + '</a>\n'
                            silverpinapList[silverpinap.index(d['item_amount'])].append(link)
				
                elif d['quest_reward_type'] == 'Stardust':
                    if str(d['item_amount']) in stardust:
                            link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(
                            d['longitude']) + '%22>' + d['name'] + '</a>\n'
                            starList[stardust.index(d['item_amount'])].append(link)
            elif d['quest_reward_type'] == 'Pokemon':
                if str(d['pokemon_id']) in pokemonIds:
                    link = '<a href=%22http://www.google.com/maps/place/' + str(d['latitude']) + str(',') + str(d['longitude']) + '%22>' + d['name'] + '</a>\n' + '$' + d['pokemon_id'] + '$'
                    text = text.replace('$' + d['pokemon_id'] + '$', link)
                    pokeList[pokemonIds.index(d['pokemon_id'])] = True

starstring = ''
candystring = ''
silverpinapstring = ''

if madlanguage == "DE":
    for i in range(0, len(stardust)):
        if len(starList[i]) == 0:
            continue
        starstring += '\n🌟¬ ' + stardust[i] + ' <b>Sternenstaub:</b>\n'
        for k in starList[i]:
            starstring += k
		
    for i in range(0, len(rarecandy)):
        if len(candyList[i]) == 0:
            continue
        candystring += '\n🍬¬ ' + rarecandy[i] + ' <b>Sonderbonbons:</b>\n'
        for k in candyList[i]:
            candystring += k
		
    for i in range(0, len(silverpinap)):
        if len(silverpinapList[i]) == 0:
            continue
        silverpinapstring += '\n🍈¬ ' + silverpinap[i] + ' <b>Silberne Sananabeere:</b>\n'
        for k in silverpinapList[i]:
            silverpinapstring += k
		
    for i in range(0, len(pokemonIds)):
        if pokeList[i]:
            text = text.replace('$' + pokemonIds[i] + '$', '')
            continue
        text = text.replace('$' + pokemonIds[i] + '$', '<i>Heute nicht gefunden</i>\n')
	
elif madlanguage == "EN":
    for i in range(0, len(stardust)):
        if len(starList[i]) == 0:
            continue
        starstring += '\n🌟¬ ' + stardust[i] + ' <b>Stardust:</b>\n'
        for k in starList[i]:
            starstring += k
		
    for i in range(0, len(rarecandy)):
        if len(candyList[i]) == 0:
            continue
        candystring += '\n🍬¬ ' + rarecandy[i] + ' <b>Rare Candie(s):</b>\n'
        for k in candyList[i]:
            candystring += k
		
    for i in range(0, len(silverpinap)):
        if len(silverpinapList[i]) == 0:
            continue
        silverpinapstring += '\n🍈¬ ' + silverpinap[i] + ' <b>Silver Pinapberrie(s):</b>\n'
        for k in silverpinapList[i]:
            silverpinapstring += k
		
    for i in range(0, len(pokemonIds)):
        if pokeList[i]:
            text = text.replace('$' + pokemonIds[i] + '$', '')
            continue
        text = text.replace('$' + pokemonIds[i] + '$', '<i>Nothing found today</i>\n')
	
text = text.replace('$rarecandy$', candystring)
text = text.replace('$stardust$', starstring)
text = text.replace('$silverpinap$', silverpinapstring)
text = text.replace('$amount$', str(len(data)))
text = text.replace('$amountquests$', str(len(data)))
text = text.replace('$amountpokestops$', "%s" % amountpokestops)
locale.setlocale(locale.LC_TIME, localeSetting)
text = text.replace('$date', time.strftime("%A, %e.%m.%Y"))
text = text.replace('&', '%26amp;')

def bot_sendtext(bot_message):
    ### Send text message
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=html&text=' + bot_message
    requests.get(send_text)

bot_sendtext(text)
