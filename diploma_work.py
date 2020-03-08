import requests
import time
import json
# from pprint import pprint

token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

params = {
    'access_token': token,
    'v': '5.103'
}


class User():

    params = {
        'access_token': token,
        'v': '5.103'
    }
    
    def __init__(self, user_id):
        self.user_id = user_id


    def get_user_friends(self):
        params = self.params
        try:
            response = requests.get(f'https://api.vk.com/method/friends.get?user_id={self.user_id}', params)
            self.friends_list = response.json()['response']['items']
        except requests.exceptions.ConnectionError:
            print('Connection failed. Try again later.')
            return False
        else:
            return True
                
    
    def get_user_groups(self):
        params = self.params
        print('executing request...')
        try:
            response = requests.get(f'https://api.vk.com/method/groups.get?user_id={self.user_id}&extended=1&fields=members_count', params)
        except requests.exceptions.ConnectionError:
            return False
        else:
            try:
                self.groups_info_list = response.json()['response']['items']
            except KeyError:
                self.groups_info_list = []
        print('...')
        try:
            response = requests.get(f'https://api.vk.com/method/groups.get?user_id={self.user_id}', params)
        except requests.exceptions.ConnectionError:
            return False
        else:
            try:
                self.groups_id_set = set(response.json()['response']['items'])
            except KeyError:
                self.groups_id_set = {}
        return True




def check_common_groups(user):
    for friend_id in user.friends_list:
        friend = User(friend_id)
        if friend.get_user_groups() == True:
            time.sleep(0.34)
            common_set = user.groups_id_set.intersection(friend.groups_id_set)
            user.groups_id_set.difference_update(common_set)
        else:
            print('Connection failed.')

    final_list = []
    for group in user.groups_info_list:
        if group.get('id') in user.groups_id_set:
            final_list.append({'name':group.get('name'), 'gid':group.get('id'), 'members_count':group.get('members_count')})
    
    file_writing(final_list)


def file_writing(final_list):
    with open('groups.json', 'w', encoding='utf-8') as file:
        json.dump(final_list, file, ensure_ascii=False, indent=4)
    print('File "groups.json" created.')




if __name__ == "__main__":
    eshmargunov = User(171691064)
    if eshmargunov.get_user_friends() == True:
        eshmargunov.get_user_groups()
        check_common_groups(eshmargunov)
    print('Program finished.')