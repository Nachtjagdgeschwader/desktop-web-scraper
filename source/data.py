#!/usr/bin/python3
# -*- coding: utf-8 -*-
import vk
from datetime import datetime
def vksearch(query,end_time,start_time):
    session = vk.Session(access_token='Your access token')
    # Get your token through 
    # https://oauth.vk.com/authorize?client_id=4797459&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos ,audio,video,docs,notes,pages,status,wall,groups,notifications,offline&response_type=token
    vkapi = vk.API(session)
    full_data = []
    for x in range(0,1000,200):
        results=vkapi.newsfeed.search(q=query, count=200, start_time=start_time,
                                      end_time=end_time, offset=x)
        res1= results[1:]
        full_data.extend(res1)
    return full_data

def create_dataframe(data):
    date = []
    text = []
    comments = []
    likes = []
    reposts = []
    url1 = []
    for item in data:
        date.append(datetime.fromtimestamp(item['date']))
        text.append(item['text'])
        comments.append(item['comments']['count'])
        likes.append(item['likes']['count'])
        reposts.append(item['reposts']['count'])
        if item['post_type']=="post":
            url='https://vk.com/wall'+str(item['owner_id'])+'_'+str(item['id'])
        elif item['post_type']=="reply":
            url = 'https://vk.com/wall' + str(item['owner_id']) + '_' \
                  + str(item['post_id'])+'?reply='+str(item['id'])
        else:
            url='other URL'
        url1.append(url)
    return url1, text, date, comments, likes, reposts