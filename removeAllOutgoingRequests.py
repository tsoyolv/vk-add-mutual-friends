import vk_api

vk_session = vk_api.VkApi('+71111111111', 'password')
vk_session.auth()

vk = vk_session.get_api()

outRequests = vk.friends.getRequests(out=1).get('items')

for outRequest in outRequests :
	#vk.friends.delete(user_id=outRequest)
	print('delete request for user: ' + str(vk.users.get(user_id=outRequest)) + '\n')


input('Please enter to exit.')