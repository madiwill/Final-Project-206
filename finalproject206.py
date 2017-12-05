# Name: Madison Willihnganz
# uniqname: madiwill
# Section Day/Time: Thursday/3-4pm

import json
import random
import requests
import facebook
import sqlite3
import pprint
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from datetime import datetime 

#FacebookAPI

def __init__(self):
        self.fb_url = 'https://developers.facebook.com/tools/debug/og/object'

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

class Post():
    def __init__(self, post_dict={}):
    	if 'message' in post_dict:
    		self.message = post_dict['message']
    	else:
    		self.message = ""
    	if 'comments' in post_dict:
    		self.comments = post_dict['comments']['data']
    	else:
    		self.comments = []
    	if 'likes' in post_dict:
    		self.likes = post_dict['likes']['data']
    	else:
    		self.likes = []

fb_access_token = "EAACEdEose0cBAPPZAKLlSVR8li69IHGF6iY6dIIYhIGqItaOKZAFBNZAktagjf3GPaIG2zqbkKJexLIo5ZCsSoLH9Tn8LOJmovlji2XBV3o1ozElW36FrIgWlaOGOqiD2vwUmJPEd3UBQGfoRWdjJgaJbpVx8ZBzInuxZCvznqs1ZAEnj4zVBn0NiZCQ5IhCztwZD"
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
    fbparams={"access_token":fb_access_token, "limit": 100}
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
fb = json.loads(facebook_post)

print ('----------------------------------------3')

#create facebook data table
conn= sqlite3.connect('Facebook_206_Final_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Facebook_Data')
cur.execute('CREATE TABLE Facebook_Data (post VARCHAR, time DATETIME)')

fb_data = fb['data']
for post in fb_data:
    if 'message' in post:
        remove_timezone1 = post['created_time'][:-5]
        time = datetime.strptime(remove_timezone1, '%Y-%m-%dT%H:%M:%S')
        tup = post['message'], time
        cur.execute('INSERT OR IGNORE INTO Facebook_Data (post, time) VALUES (?, ?)', tup)
    if 'story' in post:
        remove_timezone = post['created_time'][:-5]
        time = datetime.strptime(remove_timezone, '%Y-%m-%dT%H:%M:%S')
        tup = post['story'], time
        cur.execute('INSERT OR IGNORE INTO Facebook_Data (post, time) VALUES (?, ?)', tup)

conn.commit()

print ('----------------------------------------3')

#InstagramAPI

insta_access_token = "213962356.1677ed0.4c721dc52c6946458137aeb2bec48b57"

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
insta = json.loads(str(insta_post))


#create instagram data table

conn= sqlite3.connect('Insta_206_Final_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Instagram_Data')
cur.execute('CREATE TABLE Instagram_Data (post VARCHAR, time DATETIME)')
import datetime

insta_data = insta['data']
for post in insta_data:
    if 'user' in post:
        date = (datetime.datetime.fromtimestamp(int(post['created_time'])).strftime('%Y-%m-%d %H:%M:%S'))
        tup = post['user']['full_name'], date
        cur.execute('INSERT OR IGNORE INTO Instagram_Data (post, time) VALUES (?, ?)', tup)

conn.commit()

#create plotly graph
plotly.tools.set_credentials_file(username='madiwill', api_key='BL58oUvyXtX2LWrL7Rv5')
plotly.tools.set_config_file(world_readable=True)
trace0 = Bar(x=[1, 2, 3, 4], y=[10, 15, 13, 17])
trace1 = Scatter(x=[1, 2, 3, 4], y=[16, 5, 11, 9])
data = Data([trace0, trace1])

py.plot(data, filename = 'basic-line')

print ('----------------------------------------5')