import vk_api
import time
import random
import datetime
import requests
import urllib3
import os

def loginAndGetApi(login, password) :
	vk_session = vk_api.VkApi(login, password)
	vk_session.auth()
	return vk_session.get_api()
	
FRIENDS_WILL_BE_CONST = 'friendsWillBeAddedstr'
FRIENDS_WERE_ADDED_CONST ='friendsWereAddedstr'
def createLogFiles() :
	logsPath = os.path.join(os.getcwd(), 'logs')
	if not os.path.exists(logsPath):
		os.makedirs(logsPath)
		
	needPath = os.path.join(logsPath, 'FriendsThatWillBeAdded')
	if not os.path.exists(needPath):
		os.makedirs(needPath)
		
	addedPath = os.path.join(logsPath, 'FriendsThatWereAdded')
	if not os.path.exists(addedPath):
		os.makedirs(addedPath)
	
	datetimestr = datetime.datetime.now().strftime('_%H-%M-%m__%d-%m-%y')
	
	friendsWillBeAddedstr = os.path.join(needPath, 'friendsWillBeAdded' + datetimestr + '.log')
	friendsWereAddedstr = os.path.join(addedPath, 'friendsWereAdded' + datetimestr + '.log')
	
	with open(friendsWillBeAddedstr, 'w+', encoding='utf-8') as file:
		print('friendsWillBeAdded log file created.')
	
	with open(friendsWereAddedstr, 'w+', encoding='utf-8') as file:
		print('friendsWereAdded log file created.')	
		
	return {FRIENDS_WILL_BE_CONST:friendsWillBeAddedstr, FRIENDS_WERE_ADDED_CONST: friendsWereAddedstr}

def filterFriends(friends, vk, sex) :
	friendsTemp = friends.copy()
	for key in list(friendsTemp) :
		addFriend = vk.users.get(user_id=key,fields='sex')
		if addFriend[0].get('sex') != sex :  # gender. 1 = female, 2 = male
			del friendsTemp[key]
	return friendsTemp
	
def addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt) :
	MUTUAL_FRIENDS_LIMIT = mutualFriendsCnt

	dictMutualFriends = {}
	mutualFriendsForAdding = {}

	friends = vk.friends.get().get('items')
	me = vk.users.get()[0].get('id')
	outgoingRequests = vk.friends.getRequests(out=1).get('items')

	print('start processing...')
	for friend in friends :
		try :
			mutualFriends = vk.friends.get(user_id=friend).get('items')
		except vk_api.exceptions.ApiError :
			print('\texception. Maybe deleted user with id: ' + str(friend))
			continue
		#print('My Friend is: ' + str(vk.users.get(user_id=friend)) + '\n')
		for mFriend in mutualFriends : 
			if (mFriend not in friends) and (mFriend not in outgoingRequests) and (mFriend != me) :
				if dictMutualFriends.get(mFriend) :
					dictMutualFriends[mFriend] += 1
					if dictMutualFriends[mFriend] >= MUTUAL_FRIENDS_LIMIT : 
						mutualFriendsForAdding[mFriend] = dictMutualFriends[mFriend]
				else :
					dictMutualFriends[mFriend] = 1

	print('end processing')
	
	mutualFriendsForAddingTemp = filterFriends(mutualFriendsForAdding, vk, 1)
	if len(mutualFriendsForAddingTemp) == 0 :
		mutualFriendsForAddingTemp = mutualFriendsForAdding
		print('switch to ANY GENDER!')
	mutualFriendsForAdding = mutualFriendsForAddingTemp
	
	print('friends amount: ' + str(len(mutualFriendsForAdding)))
	
	logFilesPaths = createLogFiles()
	
	print('start writing to file FriendsThatWillBeAdded...')
	with open(logFilesPaths.get(FRIENDS_WILL_BE_CONST), 'a', encoding='utf-8') as file:
		file.write('friends amount: ' + str(len(mutualFriendsForAdding)) + '. mutual friends limit = ' + str(MUTUAL_FRIENDS_LIMIT) + '\n')
		for key in mutualFriendsForAdding :
			addFriend = vk.users.get(user_id=key)
			file.write('FRIEND. cnt = ' + str(mutualFriendsForAdding[key]) + '. Info: ' + str(addFriend) + '\n')
	print('end writing to file FriendsThatWillBeAdded')

	print('start writing to file FriendsThatWereAdded...')
	with open(logFilesPaths.get(FRIENDS_WERE_ADDED_CONST), 'a', encoding='utf-8') as file:
		file.write('friends amount: ' + str(len(mutualFriendsForAdding)) + '. mutual friends limit = ' + str(MUTUAL_FRIENDS_LIMIT) + '\n')
		
	friendsCnt = random.randint(3, 5)
	i = 0
	
	for key in mutualFriendsForAdding : 
		addFriend = vk.users.get(user_id=key)
		try :
			vk.friends.add(user_id=key)
		except (vk_api.exceptions.ApiError, requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as exp :	
			print('exception or connection refused. User with id: ' + str(key))
			vk = loginAndGetApi(login, password)
			continue
		print('\trequest sent. at time: ' + str(datetime.datetime.now()) + '. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend))
		with open(logFilesPaths.get(FRIENDS_WERE_ADDED_CONST), 'a', encoding='utf-8') as file:	
			#file.write('request sent. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
			file.write('request sent. at time: ' + str(datetime.datetime.now()) + '. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
		time.sleep(random.randint(33, 59))
		i += 1
		if i >= friendsCnt :
			friendsCnt = random.randint(3, 5)
			i = 0
			randd = random.randint(33, 88)
			print('wait ' + str(randd) + ' minutes...')
			time.sleep(60 * randd)

			
	print('end writing to file FriendsThatWereAdded')	
	return len(mutualFriendsForAdding)

login = input('Enter login: ')
password = input('Enter password: ')
mutualFriendsCnt = int(input('Enter mutual friends amount: '))
vk = loginAndGetApi(login, password)

resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt)

while resultedCnt > 0 :
	randd = random.randint(4, 8)
	print('wait for ' + str(randd) + ' hours!...')
	time.sleep(60 * 60 * randd)
	try : 
		resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt)
	except (vk_api.exceptions.ApiError, requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError, urllib3.exceptions.NewConnectionError) as exp :
		print('there is exception or connection refused! rerun adding with mutualFriendsCnt: ' + str(mutualFriendsCnt))
		vk = loginAndGetApi(login, password)
		resultedCnt = addPossibleFriendsWithCommonFriends(vk, login, password, mutualFriendsCnt)
	print('mutual friends limit = ' + str(mutualFriendsCnt + 1))
	mutualFriendsCnt += 1
		
input('Please enter to exit...')