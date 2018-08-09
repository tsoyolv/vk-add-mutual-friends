import vk_api
import getpass
import logging

logging.basicConfig(filename='removedOutgoingRequests.log',level=logging.INFO)

login = input('Enter login: ')
password = getpass.getpass('Enter password: ')

vk_session = vk_api.VkApi(login, password)
vk_session.auth()

vk = vk_session.get_api()

outRequests = vk.friends.getRequests(out=1).get('items')

for outRequest in outRequests :
    outFriendFriends = vk.friends.get(user_id=outRequest).get('items')
    try :
        logging.info('delete request for user: ' + str(vk.users.get(user_id=outRequest)) + '. User friends cnt: ' + str(len(outFriendFriends)))
        if len(outFriendFriends) >= 1000 :
            logging.info('More than 1000')
            #vk.friends.delete(user_id=outRequest)
    except vk_api.exceptions.ApiError :	
        logging.info('exception or connection refused. User with id: ' + str(outRequest))
        continue
	


input('Please enter to exit.')