import vk_api

vk_session = vk_api.VkApi('+79111111111', 'password')
vk_session.auth()

vk = vk_session.get_api()

friendsFile = open('friends.txt', 'w+')

friends = vk.friends.get().get('items')

dictMutualFriends = {}

for friend in friends :
	mutualFriends = vk.friends.get(user_id=friend).get('items')
	print(str(vk.users.get(user_id=friend)) + '\n')
	friendsFile.write('My Friend is: ' + str(vk.users.get(user_id=friend)) + '\n')
	for mFriend in mutualFriends : 
		print('\t mutual friends is: ')
		if mFriend not in friends and mFriend != vk.users.get()[0].get('id'):
			if dictMutualFriends.get(mFriend) :
				dictMutualFriends[mFriend] += 1
			else :
				dictMutualFriends[mFriend] = 1
			print('\t POSSIBLE FRIEND count=' + str(dictMutualFriends[mFriend]) + ' friend = ' + str(vk.users.get(user_id=mFriend)) + '\n')
		else : 
			print('\t ALREADY FRIEND' + str(vk.users.get(user_id=mFriend)) + '\n')
	
for key in dictMutualFriends :
	if dictMutualFriends[key] >= 5 :
			friendsFile.write('\t MUTUAL FRIEND cnt = ' + str(dictMutualFriends[key]) + 'friend: ' + str(vk.users.get(user_id=mFriend)) + '\n')
	
friendsFile.close()
input('Please enter to exit.')