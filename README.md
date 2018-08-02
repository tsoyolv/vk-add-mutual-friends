# vk-add-mutual-friends - Console App that adds all mutual friends in VK who have common friends amount >= n

That console app adds mutual friends who have common friends amount >= n with random time delay and after it adds all mutual friends, it is continue to add 
mutual friends with more common friends amount (incremented by 1). It continues till the moment when there is no mutual friends.

Requirements:
-
1. VK account
2. Python 3 and higher

Start
-
To start application locally you need to:
1. install vk_api pip install vk_api (https://github.com/python273/vk_api)
2. Start addAllMutualFriends.py
3. Enter your login/password and mutual friends amount

To start application that removes all outgoing requests for friends you need to:
1. install vk_api pip install vk_api (https://github.com/python273/vk_api)
2. Start removeAllOutgoingRequests.py
3. Enter your login/password