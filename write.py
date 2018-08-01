import vk_api
import time
import random

vk_session = vk_api.VkApi('+71111111111', 'password')
vk_session.auth()

vk = vk_session.get_api()

friends = vk.friends.get().get('items')

dictMutualFriends = {}
mutualFriendsForAdding = {}

me = vk.users.get()[0].get('id')

for friend in friends :
	try :
		mutualFriends = vk.friends.get(user_id=friend).get('items')
	except vk_api.exceptions.ApiError :
		print('exception. Maybe deleted user')
		continue
	print('My Friend is: ' + str(vk.users.get(user_id=friend)) + '\n')
	for mFriend in mutualFriends : 
		if mFriend not in friends and mFriend != me:
			if dictMutualFriends.get(mFriend) :
				dictMutualFriends[mFriend] += 1
			else :
				dictMutualFriends[mFriend] = 1
			if dictMutualFriends[mFriend] >= 5 : 
				mutualFriendsForAdding[mFriend] = dictMutualFriends[mFriend]
			print('\t POSSIBLE FRIEND count=' + str(dictMutualFriends[mFriend]) + '\n')
	
with open('friendsW.txt', 'w+') as file:
	print('file created')

with open('friendsW.txt', 'a') as file:
	for key in mutualFriendsForAdding :
		#time.sleep(60 * random.randint(33, 92))
		#vk.friends.add(user_id=key)
		addFriend = vk.users.get(user_id=key)
		print('\t request sent. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
		file.write('request sent. cnt = ' + str(mutualFriendsForAdding[key]) + ' friend: ' + str(addFriend) + '\n')
		
		
input('Please enter to exit.')