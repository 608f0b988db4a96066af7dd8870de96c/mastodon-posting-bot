#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import os.path
import time
import json
import requests
from mastodon import Mastodon

SOURCE = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&tags=loli+-animated&json=1'
CLIENT_ID = 'client_id.secret'
ACCESS_TOKEN = 'token.secret'
API_BASE_URL = 'https://baraag.net'
LAST_POSTED = 'src'

def json_parse(source, image_number):
    data = []
    response = requests.get(source)
    image_source = response.json()[image_number]['file_url']
    original_source = response.json()[image_number]['source']
    data.append(image_source)
    data.append(original_source)
    return data

def login():
    mastodon = Mastodon(
        client_id = CLIENT_ID,
        access_token = ACCESS_TOKEN,
        api_base_url = API_BASE_URL
    )
    return mastodon

def post_image(image_source, original_source, mastodon):
    with open('temp.jpg', 'wb') as f:
        f.write(requests.get(image_source).content)
    mastodon.status_post(status='%s' %original_source, media_ids = [mastodon.media_post(media) for media in ['temp.jpg']])

def main():
    mastodon = login()

    if not os.path.isfile(LAST_POSTED):
        post_image(json_parse(SOURCE, 0)[0], json_parse(SOURCE, 0)[1], mastodon)
        with open(LAST_POSTED, 'w') as f:
            f.write(json_parse(SOURCE, 0)[0])

    while True:
        last_image_source = json_parse(SOURCE, 0)[0]
        with open(LAST_POSTED, 'r') as f:
            last_posted_image = f.read()

        if last_image_source != last_posted_image:
            for i in range(0, 99):
                if last_posted_image == json_parse(SOURCE, i)[0]:
                    current_number = i
                    break

            if current_number == None:
                current_number = 1

            for i in range(current_number - 1, -1, -1):
                post_image(json_parse(SOURCE, i)[0], json_parse(SOURCE, i)[1], mastodon)
            with open(LAST_POSTED, 'w') as f:
                f.write(last_image_source)
        else:
            print('Zzz... %s' %time.strftime('%X %x'))
            time.sleep(3600)

if __name__ == '__main__':
    main()
