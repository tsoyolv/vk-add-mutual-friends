import vk_api
import time
import random
import datetime

login = input('Enter login: ')
password = input('Enter password: ')

vk_session = vk_api.VkApi(login, password)
vk_session.auth()

vk = vk_session.get_api()

friends = vk.friends.get().get('items')

dictMutualFriends = {}
mutualFriendsForAdding = {}

me = vk.users.get()[0].get('id')

MUTUAL_FRIENDS_LIMIT = int(input('Enter mutual friends amount: '))

outgoingRequests = vk.friends.getRequests(out=1).get('items')

print('start processing...')
for friend in friends :
	try :
		mutualFriends = vk.friends.get(user_id=friend).get('items')
	except vk_api.exceptions.ApiError :
		print('exception. Maybe deleted user with id: ' + str(friend))
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

with open('friendsW.txt', 'w+', encoding='utf-8') as file:
	print('file created')

print('start writing to file...')

print('friends amount: ' + str(len(mutualFriendsForAdding)))
with open('friendsW.txt', 'a', encoding='utf-8') as file:
	file.write('friends amount: ' + str(len(mutualFriendsForAdding)) + '\n')
	for key in mutualFriendsForAdding :
		#randd = random.randint(3, 88)
		#print('random digit: ' + str(randd))
		#time.sleep(60 * randd)
		#time.sleep(random.randint(1, 15))
		##dangertry :
			##dangervk.friends.add(user_id=key)
		##dangerexcept vk_api.exceptions.ApiError :	
			##dangerprint('exception. User with id: ' + str(key))
			##dangercontinue
		addFriend = vk.users.get(user_id=key)
		#print('\t request sent. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
		file.write('request sent. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
		#file.write('request sent. at time: ' + str(datetime.datetime.now()) + '. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
print('end writing to file')	
		
input('Please enter to exit...')