from pprint import pprint
import vk
from urllib.parse import urlencode, urlparse
import requests
import json
import time


def get_params():
    AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    VERSION = '5.63'
    APP_ID = 5947968  # Your app_id here
    access_token = ""  # Your token
    params = {'access_token': access_token,
              'v': VERSION,
              }
    return params


def get_friend_name_and_frinds(user_id=None):
    if user_id:
        params = get_params()
        params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/users.get', params)
    name = response.json()

    ff = dict()
    for i in name['response']:
        if len(i) == 4:
            continue
        else:
            response = requests.get('https://api.vk.com/method/friends.get', params)
            m = response.json()
            try:
                ff.update({id: m['response']['items']})
            except:
                print('EXCEPT')
    return ff


def open_file():
    with open("freinds.json", encoding='utf-8') as f:
        list_friends = json.load(f)
        i = 0
        for id in list_friends['response']['items']:
            ff = get_friend_name_and_frinds(id)
            i += 1
            if i == 5:
                time.sleep(4)
                i = 0
            time.sleep(0.25)

        response = requests.get('https://api.vk.com/method/friends.get', get_params())
        k = response.json()
        set_friends = set(k['response']['items'])
        pprint(set_friends)
        if ff:
            for i in ff.values():
                new_set_friends = set_friends & set(i)
                print("ПЕРЕСЕЧЕНИЕ!!!!!!!!!!!!!!", new_set_friends)

open_file()
