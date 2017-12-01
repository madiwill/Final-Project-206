# Name: Madison Willihnganz
# uniqname: madiwill
# Section Day/Time: Thursday/3-4pm

import json
import random
import requests
import facebook
import sqlite3

#FacebookAPI

# def __init__(self):
#         self.fb_url = 'https://developers.facebook.com/tools/debug/og/object'

# def pretty(obj):
#     return json.dumps(obj, sort_keys=True, indent=2)

# class Post():
#     def __init__(self, post_dict={}):
#     	if 'message' in post_dict:
#     		self.message = post_dict['message']
#     	else:
#     		self.message = ""
#     	if 'comments' in post_dict:
#     		self.comments = post_dict['comments']['data']
#     	else:
#     		self.comments = []
#     	if 'likes' in post_dict:
#     		self.likes = post_dict['likes']['data']
#     	else:
#     		self.likes = []

fb_access_token = "xxxxx"
if fb_access_token == None:
    fb_access_token = raw_input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")

baseurl = "https://graph.facebook.com/v2.3/me/feed"
url_params = {}
url_params["access_token"] = fb_access_token
# Write code to fill in other url_parameters dictionary here.
url_params['limit'] = 100
url_params['fields'] = 'message,comments,likes'
url_params['include_hidden'] = True
print ('----------------------------------------1')
feed = requests.get(baseurl,params=url_params)
d = json.loads(feed.text)
for post in d['data']:
    if 'message' in post:
        print(post['message'])

graph = facebook.GraphAPI(fb_access_token)
profile = graph.get_object('me', fields = 'name,location') #fields is an optional key word argument
# profile = graph.get_object('me', fields = 'name,location{location}') #fields is an optional key word argument
# print(json.dumps(profile, indent = 4))



CACHE_FNAME = "facebook.json" 
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)

except:
    CACHE_DICTION = {}

print ('----------------------------------------2')

def get_user_fbposts(username):
    fbparams={"access_token":fb_access_token}
    baseurl= "https://graph.facebook.com/v2.3/me/feed"
    if username in CACHE_DICTION:
        print ('using cached data')
        fb_results= CACHE_DICTION[username]
    else:
        print ('getting data from the internet')
        fb_results=requests.get(baseurl,params=fbparams)
        CACHE_DICTION[username]=fb_results.text
        f=open(CACHE_FNAME,"w")
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return fb_results
facebook_post = get_user_fbposts("Madi Willihnganz")

print ('----------------------------------------3')

#InstagramAPI

insta_access_token = "xxxxxx"

CACHE_FNAME = "insta.json" 
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)

except:
    CACHE_DICTION = {}

print ('----------------------------------------4')

def get_user_instaposts(username):
    instaparams={"access_token":insta_access_token}
    baseurl="https://api.instagram.com/v1/users/self/media/recent/"
    if username in CACHE_DICTION:
        print ('using cached data')
        insta_results= CACHE_DICTION[username]
    else:
        print ('getting data from the internet')
        insta_results=requests.get(baseurl,params=instaparams)
        CACHE_DICTION[username]=insta_results.text
        f=open(CACHE_FNAME,"w")
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return insta_results

insta_post = get_user_instaposts("madiwilly10")


print ('----------------------------------------5')