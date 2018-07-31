import vk_api

def log(file, str) :
	print(str + '\n')
	file.write(str + '\n')
	return

vk_session = vk_api.VkApi('+791111111111', 'password')
vk_session.auth()

vk = vk_session.get_api()


friends = vk.friends.get().get('items')

print('start loop')
friendsFile = open('friends.txt', 'w+')
for friend in friends :
	mutualFriends = vk.friends.get(user_id=friend).get('items')
	for mFriend in mutualFriends : 
		if mFriend not in friends and mFriend != vk.users.get()[0].get('id'):
			print(str({mFriend:1}) + '\n')
			friendsFile.write(str({mFriend:1}) + '\n')

friendsFile.close()			
print('END!!!!!!!')				
input('Please enter to exit.')