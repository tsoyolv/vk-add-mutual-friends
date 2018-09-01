import logging
import os
from datetime import datetime
from datetime import timedelta
import vk_api
import time
import random
import requests
import urllib3
import getpass

def LOG_PATH():
	return 'logs'
def FRINEDS_BE_ADDED_LOG_PATH() :
	return os.path.join(LOG_PATH(), 'FriendsThatWillBeAdded')
def FRIENDS_WERE_ADDED_LOG_PATH() :
	return os.path.join(LOG_PATH(), 'FriendsThatWereAdded')

def createLogFiles() :
	if not os.path.exists(LOG_PATH()):
		os.makedirs(LOG_PATH())		
	if not os.path.exists(FRINEDS_BE_ADDED_LOG_PATH()):
		os.makedirs(FRINEDS_BE_ADDED_LOG_PATH())	
	if not os.path.exists(FRIENDS_WERE_ADDED_LOG_PATH()):
		os.makedirs(FRIENDS_WERE_ADDED_LOG_PATH())
	return

def createLogger(name, path, level, consoleLogAdded) : 
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	ch = logging.FileHandler(os.path.join(path, name + '_{:%I-%M-%S__%d-%m-%Y}.log'.format(datetime.now())), mode='a', encoding='utf-8', delay=False)
	ch.setLevel(level)
	formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y %I:%M:%S')
	ch.setFormatter(formatter)
	logger.addHandler(ch)	
	if consoleLogAdded :
		ch = logging.StreamHandler()
		ch.setLevel(level)
		formatter = logging.Formatter(fmt='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %I:%M:%S')
		ch.setFormatter(formatter)
		logger.addHandler(ch)
	return logger
	
def loginAndGetApi(login, password) :
	vk_session = vk_api.VkApi(login, password)
	vk_session.auth()
	return vk_session.get_api()	

def filterFriends(friends, vk, sex, ignoreThousand) :
	filtered = {}
	for key in list(friends) :
		addFriend = vk.users.get(user_id=key,fields='sex')
		if addFriend[0].get('deactivated') :
			continue
		if ignoreThousand and vk.users.getFollowers(user_id=key).get('count') >= 1000 :
			continue
		if sex == -1 :
			filtered[key] = (addFriend, friends[key])
		elif addFriend[0].get('sex') == sex :  # gender. 1 = female, 2 = male
			filtered[key] = (addFriend, friends[key])
	return filtered
	
def addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt, firstTimeLimit) :
	# new logger in every bunch
	logWillbeAdded = createLogger('friendsWillBeAdded' + str(mutualFriendsCnt), FRINEDS_BE_ADDED_LOG_PATH(), logging.DEBUG, False)
	logWereAdded = createLogger('friendsWereAdded'+ str(mutualFriendsCnt), FRIENDS_WERE_ADDED_LOG_PATH(), logging.INFO, True)
	
	MUTUAL_FRIENDS_LIMIT = mutualFriendsCnt

	dictMutualFriends = {}
	mutualFriendsForAdding = {}

	friends = vk.friends.get().get('items')
	me = vk.users.get()[0].get('id')
	outgoingRequests = vk.friends.getRequests(out=1, count=1000).get('items')
	
	logger.debug('start processing...')
	
	for friend in friends :
		try :
			mutualFriends = vk.friends.get(user_id=friend).get('items')
		except vk_api.exceptions.ApiError as exp :
			logger.exception('User was deleted or banned user with id: %s', str(friend))
			continue
		for mFriend in mutualFriends : 
			if (mFriend not in friends) and (mFriend not in outgoingRequests) and (mFriend != me) :
				if dictMutualFriends.get(mFriend) :
					dictMutualFriends[mFriend] += 1
					if dictMutualFriends[mFriend] >= MUTUAL_FRIENDS_LIMIT : 
						mutualFriendsForAdding[mFriend] = dictMutualFriends[mFriend]
				else :
					dictMutualFriends[mFriend] = 1

	logger.debug('end processing...')
	
	mutualFriendsForAdding = filterFriends(mutualFriendsForAdding, vk, 1, True)
	
	logger.debug('start writing to file FriendsThatWillBeAdded...')
	logWillbeAdded.debug('friends amount: %s. mutual friends limit = %s', str(len(mutualFriendsForAdding)), str(MUTUAL_FRIENDS_LIMIT))
	for key in mutualFriendsForAdding :	
		try :
			friend = mutualFriendsForAdding[key]
			logWillbeAdded.debug('FRIEND. cnt = %s. Info: %s', str(friend[1]), str(friend[0]))
		except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as exp :	
			waitReconnect = random.randint(3, 5)
			logger.exception('Connection refused! User: %s. wait %s minutes', str(friend[0]), str(waitReconnect))
			time.sleep(60 * waitReconnect)
			vk = loginAndGetApi(login, password)
			continue
	logger.debug('end writing to file FriendsThatWillBeAdded')
	
	global outgoingRequestsCnt 
	global currentDay
	global nextDay
	global OUTGOING_REQUESTS_DAY_LIMIT 
	
	logger.debug('start writing to file FriendsThatWereAdded...')
	logWereAdded.info('friends amount: %s. mutual friends limit: %s. outgoing requests limit: %s', str(len(mutualFriendsForAdding)), str(MUTUAL_FRIENDS_LIMIT), str(OUTGOING_REQUESTS_DAY_LIMIT))
	vk.messages.send(user_id=me, message='Bunch started!!! mutual friends cnt: ' + str(MUTUAL_FRIENDS_LIMIT) + ' .friends amount: ' + str(len(mutualFriendsForAdding)))
	
	friendsBunchLimit = random.randint(3, 5)
	i = 0

	for key in mutualFriendsForAdding : 
		try :
			friend = mutualFriendsForAdding[key]
			vk.friends.add(user_id=key)
			outgoingRequestsCnt += 1
			if outgoingRequestsCnt == 1 :
				nextDay = datetime.today() + timedelta(days=1)
				logger.debug('Limit: %s for day till: %s', str(OUTGOING_REQUESTS_DAY_LIMIT), str(nextDay))
			if outgoingRequestsCnt >= OUTGOING_REQUESTS_DAY_LIMIT :
				currentDay = datetime.today()
				if currentDay < nextDay : 
					waitOutLimit = (nextDay - currentDay).seconds
					logger.info('Outgoing requests limit! wait for %s minutes. Till %s', str((waitOutLimit + 100) / 60), str(nextDay))
					vk.messages.send(user_id=me, message='Outgoing requests limit! wait ' + str((waitOutLimit + 100) / 60) + ' minutes!')
					time.sleep(waitOutLimit + 100)
				outgoingRequestsCnt = 0
			logWereAdded.info('Request sent. cnt = %s. friend: %s', str(friend[1]), str(friend[0]))
			
			if firstTimeLimit == 0 :
				logger.debug('Firsttime limit exceed! limit: ' + str(firstTimeLimit))	
				break
			elif firstTimeLimit > 0 :
				firstTimeLimit -= 1
			
		except vk_api.exceptions.ApiError as expA :
			logger.exception('exception with user. User: %s. Exception: %s', str(friend[0]), expA)
			continue
		except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as exp :	
			waitReconnect = random.randint(3, 5)
			logger.exception('Connection refused! User: %s. wait %s minutes', str(friend[0]), str(waitReconnect))
			time.sleep(60 * waitReconnect)
			vk = loginAndGetApi(login, password)
			continue		
		time.sleep(random.randint(33, 59))
		i += 1
		if i >= friendsBunchLimit :
			friendsBunchLimit = random.randint(3, 5)
			i = 0
			randd = random.randint(33, 88)
			logger.info('wait %s minutes...', str(randd))
			time.sleep(60 * randd)

			
	logger.debug('end writing to file FriendsThatWereAdded')	
	return len(mutualFriendsForAdding)

def main() : 
	login = input('Enter login: ')
	password = getpass.getpass('Enter password: ')
	mutualFriendsCnt = int(input('Enter mutual friends amount: '))
	vk = loginAndGetApi(login, password)
	
	try : 
		resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt, -1)
	except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as exp :
		logger.exception("Connection refused! rerun adding with mutualFriendsCnt: %s Exception: %s", str(mutualFriendsCnt), exp)
		vk = loginAndGetApi(login, password)
		resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt, -1)
		
	while resultedCnt > 0 :
		if resultedCnt <= 8 :
			randd = random.randint(13, 16) * 60
		elif resultedCnt < 20 :
			randd = random.randint(9, 12) * 60
		else :
			randd = random.randint(4, 8) * 60
		logger.debug('Bunch done! wait for %s minutes!...', str(randd))
		time.sleep(60 * randd)
		mutualFriendsCnt += 1
		logger.debug('mutual friends limit = %s', str(mutualFriendsCnt))
		try : 
			resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt, -1)
		except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as exp :
			logger.exception('Connection refused! rerun adding with mutualFriendsCnt: %s', str(mutualFriendsCnt))
			vk = loginAndGetApi(login, password)
			resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt, -1)
			
	return

# log files and main logger
createLogFiles()
logger = createLogger('main', LOG_PATH(), logging.DEBUG, True)	

# global variables
OUTGOING_REQUESTS_DAY_LIMIT = 40  
outgoingRequestsCnt = 0
currentDay = datetime.today()
nextDay = currentDay + timedelta(days=1)

try:
    main()
except Exception as e:
    logger.exception("%s", e)
