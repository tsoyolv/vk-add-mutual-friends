import vk_api
import time
import random

vk_session = vk_api.VkApi('+79111111111', 'password')
vk_session.auth()

vk = vk_session.get_api()

friendsFile = open('friends.log', 'w+')

friends = vk.friends.get().get('items')

dictMutualFriends = {}
mutualFriendsForAdding = {}

for friend in friends :
	mutualFriends = vk.friends.get(user_id=friend).get('items')
	print('My Friend is: ' + str(vk.users.get(user_id=friend)) + '\n')
	friendsFile.write('My Friend is: ' + str(vk.users.get(user_id=friend)) + '\n')
	for mFriend in mutualFriends : 
		print('\t mutual friends is: ')
		friendsFile.write('\t mutual friends is: ')
		if mFriend not in friends and mFriend != vk.users.get()[0].get('id'):
			if dictMutualFriends.get(mFriend) :
				dictMutualFriends[mFriend] += 1
			else :
				dictMutualFriends[mFriend] = 1
			if dictMutualFriends[mFriend] >= 5 : 
				mutualFriendsForAdding[mFriend] = dictMutualFriends[mFriend]
			print('\t POSSIBLE FRIEND count=' + str(dictMutualFriends[mFriend]) + ' friend = ' + str(vk.users.get(user_id=mFriend)) + '\n')
			friendsFile.write('\t POSSIBLE FRIEND count=' + str(dictMutualFriends[mFriend]) + ' friend = ' + str(vk.users.get(user_id=mFriend)) + '\n')
		else : 
			print('\t ALREADY FRIEND' + str(vk.users.get(user_id=mFriend)) + '\n')
			friendsFile.write('\t ALREADY FRIEND' + str(vk.users.get(user_id=mFriend)) + '\n')
	
for key in mutualFriendsForAdding :
	time.sleep(60 * random.randint(33, 92))
	vk.friends.add(user_id=key)
	print('\t request sent. cnt = ' + str(mutualFriendsForAdding[key]) + 'friend: ' + str(vk.users.get(user_id=key)) + '\n')
	friendsFile.write('\t request sent. cnt = ' + str(mutualFriendsForAdding[key]) + 'friend: ' + str(vk.users.get(user_id=key)) + '\n')
	
friendsFile.close()
input('Please enter to exit.')