import vk_api

login = input('Enter login: ')
password = input('Enter password: ')

vk_session = vk_api.VkApi(login, password)
vk_session.auth()

vk = vk_session.get_api()

outRequests = vk.friends.getRequests(out=1).get('items')

for outRequest in outRequests :
	try :
		vk.friends.delete(user_id=outRequest)
	except vk_api.exceptions.ApiError :	
		print('exception or connection refused. User with id: ' + str(outRequest))
		continue
	print('delete request for user: ' + str(vk.users.get(user_id=outRequest)))


input('Please enter to exit.')