import simpleaudio as sa
from threading import Timer
from colorama import init
init()
from colorama import Fore, Back, Style
def getIntel():
	maxResults = 1
	
	with open(r'C:\Users\David\Documents\EVE\logs\Chatlogs\GotG Home Intel_20180220_181819.txt','r', encoding='utf-16') as file:
		linelist = list(file)
	lines = len(linelist)
	global previous
	if(previous == 0):
		previous = lines - 10
	prev = previous
	previous = lines
	if(prev != lines):
		newLines = lines - prev
		if(newLines > 20):
			newLines = 20
		for i in range(newLines):
			reqIndex = lines - newLines + i
			parseLine(linelist[reqIndex], prev, lines)
			print(Fore.GREEN + str(reqIndex))
			print(Style.RESET_ALL)
	
	if(stop == False):
		t = Timer(5, getIntel)
		t.start()

def parseLine(line, prev, lines):
	messageParts = line.split(' > ')
	header = messageParts[0].split(' ] ')
	character = header[1]
	addIntelChar(character)
	terms = messageParts[1].replace('\n', '').split('  ')
	printSummary(lines, prev, line)
	printIntel(character, terms)

def addIntelChar(character):
	global intelChars
	for intelChar in intelChars:
		if(intelChar == character):
			return
	intelChars.append(character)

def addInfoChar(character, json):
	global infoChars
	for infoChar in infoChars:
		if(infoChar == character):
			return
	infoChars.append([character, json])

def printSummary(lines, prev, line):
	print(lines)
	print(prev)
	print(Fore.RED + line)
	print(Style.RESET_ALL)

def printIntel(character, terms):
	print('Character:')
	print(character)
	for alertChar in alertChars:
		if(alertChar == character):
			ping()
	print('Terms:')
	for term in terms:
		print(term)
		parseUnknown(term)
		# print(termSearch(term))

def ping():
	wave_obj = sa.WaveObject.from_wave_file(r'C:\Temp\sms-alert-3-daniel_simon.wav')
	play_obj = wave_obj.play()
	play_obj.wait_done()

import requests
def ESI_search(term):
	r = requests.get('https://esi.tech.ccp.is/latest/search/?categories=character,solar_system&datasource=tranquility&language=en-us&search=' + term + '&strict=true')
	return r.json()

def ESI_char(character_id):
	return ESI_get('characters', character_id)

def ESI_corp(corporation_id):
	return ESI_get('corporations', corporation_id)

def ESI_alliance(alliance_id):
	return ESI_get('alliances', alliance_id)

def ESI_get(endpoint, id):
	r = requests.get('https://esi.tech.ccp.is/latest/' + endpoint + '/' + id + '/?datasource=tranquility')
	return r.json()

def getChar(character_id):
	char_json = ESI_char(str(character_id))
	corporation_id = getCorp(char_json)
	corp_json = ESI_corp(str(corporation_id))
	if('alliance_id' in corp_json):
		alliance_id = getAlliance(corp_json)
		alliance_json = ESI_alliance(str(alliance_id))
		return [corporation_id, corp_json['name'],alliance_id, alliance_json['name']]
	else:
		return [corporation_id, corp_json['name']]

def printJSON(json):
	for i in json:
		print(i +':'+str(json[i]) )

def getCorp(json):
	return json['corporation_id']

def getAlliance(json):
	return json['alliance_id']

def getSearchType(json):
	found = 'n'
	foundID = 0
	for id in json:
		if(id == 'solar_system'):
			found = 's'
			foundID = json[id][0]
		if(id == 'character'):
			found = 'c'
			foundID = json[id][0]
	return [found, foundID]

def termSearch(term):
	result = getSearchType(ESI_search(term))
	if(result[0] == 'c'):
		output = ['character', term, getChar(result[1])]
	if(result[0] == 's'):
		output = ['solar_system', term, result[1]]
	if(result[0] == 'n'):
		output = ['none']
	return output

def tryTerms(splitTerm):
	returnValue = 1
	size = len(splitTerm)
	for i in range(size):
		j = size-i
		subTerm = ''
		for k in range(j):
			if(k>0):
				subTerm += ' '
			subTerm += splitTerm[k]
		result = termSearch(subTerm)
		if(result[0]!='none'):
			returnValue = j
			#print(subTerm)
			print(result)
			if(result[0] == 'character'):
				addInfoChar(result[1], result)
			return returnValue
	return returnValue

def parseUnknown(term):
	splitTerm = term.strip().split(' ')
	while(len(splitTerm)>0):
		foundLen = tryTerms(splitTerm)
		for m in range(foundLen):
			splitTerm.pop(0)

alertChars = ['SmallFatCat','Moot Scudrunner','Arcee Ebonheart']
intelChars = []
infoChars = []
previous = 0
stop = False
getIntel()


stop = True



import clipboard

def clip():
	# clipboard.copy("abc")
	text = clipboard.paste()
	list = text.split('\n')
	r = 0
	f = 0
	for i in list:
		r += 1
		row = i.split('\t')
		f = len(row)
		print(row)
	return [len(text), r, f]






