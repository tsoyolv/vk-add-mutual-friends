import vk_api

def log(file, str) :
	print(str + '\n')
	file.write(str + '\n')
	return

login = input('Enter login: ')
password = input('Enter password: ')

vk_session = vk_api.VkApi(login, password)
vk_session.auth()

vk = vk_session.get_api()

writeLimit = 1000

friends = vk.friends.get().get('items')

me = vk.users.get()[0].get('id')

print('start loop')

writeCnt = 0

with open('friends.txt', 'w+') as file:
	print('file created')

allMFriendsCount = 0
for friend in friends :
	friendObj = vk.users.get(user_id=friend)
	try :
		mutualFriends = vk.friends.get(user_id=friend).get('items')
	except vk_api.exceptions.ApiError :
		print('exception. Maybe deleted user')
		continue
	j = 0;
	print('friend: ' + str(friendObj))
	while j < len(mutualFriends) :
		with open('friends.txt', 'a') as file:  #with open('friends.txt', 'w') as file:
			while writeCnt < writeLimit and j < len(mutualFriends) :
				mFriend = mutualFriends[j]
				if mFriend not in friends and mFriend != me:
					#print('\t' + str({mFriend:1}) + '\n')
					file.write(str({mFriend:1}) + '\n')
					writeCnt += 1
				j += 1
				allMFriendsCount += 1
			if writeCnt == writeLimit :
				writeCnt = 0
				print('writeCnt')
	
		
print('All possible friends count: ' + str(allMFriendsCount))
print('END!!!!!!!')				
input('Please enter to exit.')