# Name: Madison Willihnganz
# uniqname: madiwill
# Section Day/Time: Thursday/3-4pm

import json
import random
import requests
import facebook
import sqlite3
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
from datetime import datetime 

#InstagramAPI

insta_access_token = "213962356.1677ed0.4c721dc52c6946458137aeb2bec48b57"

#took from project 3 and adapted to instagram
CACHE_FNAME = "insta.json" 
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)

except:
    CACHE_DICTION = {}

#defining function get_user_instaposts which is similar to the twitter function in project 3
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

#invocating a function
insta_post = get_user_instaposts("madiwilly10")
insta = json.loads(str(insta_post))


#create instagram data table
conn= sqlite3.connect('Insta_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Instagram')
cur.execute('CREATE TABLE Instagram (post VARCHAR, time DATETIME)')

#had to reimport as I was getting an error
import datetime

dates = []
insta_data = insta['data']
for post in insta_data:
    if 'user' in post:
        # used StackOverflow to help with converting Unix timestamp to Python https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python/14048587
        date = (datetime.datetime.fromtimestamp(int(post['created_time'])).strftime('%Y-%m-%d %H:%M:%S'))
        #sorting through json file
        tup = post['user']['full_name'], date
        dates.append(date)
        #putting the time values into the database
        cur.execute('INSERT OR IGNORE INTO Instagram (post, time) VALUES (?, ?)', tup)

conn.commit()

#had to reimport as I was getting an error
from datetime import datetime

#create plotly graph for instagram
#create empty lists for the days of the week
sunday =[]
monday = []
tuesday = []
wednesday = []
thursday = []
friday = []
saturday = []

for date in dates:
    #spliting the date by the year, month, and day based on the timestamp
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    weekday = datetime(year, month, day).weekday()

    #weekday gives numbers 0-6 to the days of the week in Python
    if weekday == 0:
        monday.append(weekday)
    if weekday == 1:
        tuesday.append(weekday)
    if weekday == 2:
        wednesday.append(weekday)
    if weekday == 3:
        thursday.append(weekday)
    if weekday == 4:
        friday.append(weekday)
    if weekday == 5:
        saturday.append(weekday)
    if weekday == 6:
        sunday.append(weekday)

#FacebookAPI

fb_access_token = "EAACEdEose0cBAO7MF5GSFxJBDLiZBkLPyqaE6JFi1yXAPDOZBKD74QXnFET5MrvqlqD7ZCEqkqlFVNIsdgXFeXeOM8d2NZCPaz6Y48VQZCDXHxfxKTZCglh0fKO7X1NrtvA7XZAkJt4HKjy7e4kTaWDeoSjT8ZCtJN8rn3IYSWjaePbz2YgN3omU8GhOacIi9BcZD"
if fb_access_token == None:
    fb_access_token = raw_input("\nCopy and paste token from https://developers.facebook.com/tools/explorer\n>  ")
graph = facebook.GraphAPI(fb_access_token)
profile = graph.get_object('me', fields = 'name,location')

#took from project 3 and adapted to facebook
CACHE_FNAME = "facebook.json" 
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)

except:
    CACHE_DICTION = {}

#defining function get_user_fbposts which is similar to the twitter function in project 3
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

#invocating a function 
facebook_post = get_user_fbposts("Madi Willihnganz")
fb = json.loads(facebook_post)
# print(fb)
#create facebook data table
conn= sqlite3.connect('Facebook_Project.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (post VARCHAR, time DATETIME)')

fb_dates = []
fb_data = fb['data']


for post in fb_data:
    if 'message' in post:
        #professor Van Lent showed me and Mallory Robbins this method to eliminate the timezone
        new_time1 = post['created_time'][:-5]
        #Converting date to datetime  https://stackoverflow.com/questions/30140320/python-convert-date-string-to-datetime
        fb_time = str(datetime.strptime(new_time1, '%Y-%m-%dT%H:%M:%S'))
        #sorting through json file
        tup = post['message'], fb_time
        fb_dates.append(fb_time)
        #putting the time values into the database
        cur.execute('INSERT OR IGNORE INTO Facebook (post, time) VALUES (?, ?)', tup)
    if 'story' in post:
        #professor Van Lent showed me and Mallory Robbins this method to eliminate the timezone
        new_time2 = post['created_time'][:-5]
        fb_time = str(datetime.strptime(new_time2, '%Y-%m-%dT%H:%M:%S'))
        #sorting through json file
        tup = post['story'], fb_time
        fb_dates.append(fb_time)
        #putting the time values into the database
        cur.execute('INSERT OR IGNORE INTO Facebook (post, time) VALUES (?, ?)', tup)

conn.commit()

#had to reimport as I was getting an error
from datetime import datetime

#create plotly graph for facebook
#create empty lists for the days of the week
fb_sunday =[]
fb_monday = []
fb_tuesday = []
fb_wednesday = []
fb_thursday = []
fb_friday = []
fb_saturday = []

for fb_time in fb_dates:
    #spliting the date by the year, month, and day based on the timestamp
    year = int(fb_time[0:4])
    month = int(fb_time[5:7])
    day = int(fb_time[8:10])
    weekday = datetime(year, month, day).weekday()

    #weekday gives numbers 0-6 to the days of the week in Python
    if weekday == 0:
        fb_monday.append(weekday)
    if weekday == 1:
        fb_tuesday.append(weekday)
    if weekday == 2:
        fb_wednesday.append(weekday)
    if weekday == 3:
        fb_thursday.append(weekday)
    if weekday == 4:
        fb_friday.append(weekday)
    if weekday == 5:
        fb_saturday.append(weekday)
    if weekday == 6:
        fb_sunday.append(weekday)

#Plotly authentication https://plot.ly/python/getting-started/
plotly.tools.set_credentials_file(username='madiwill', api_key='BL58oUvyXtX2LWrL7Rv5')
plotly.tools.set_config_file(world_readable=True)

#plotly data for days of the week for Facebook and Instagram
facebook_dates = Bar(x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], y=[len(fb_monday), len(fb_tuesday), len(fb_wednesday), len(fb_thursday), len(fb_friday), len(fb_saturday), len(fb_sunday)])
insta_dates = Bar(x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], y=[len(monday), len(tuesday), len(wednesday), len(thursday), len(friday), len(saturday), len(sunday)])
data = Data([facebook_dates, insta_dates])
#naming the file
py.plot(data, filename = 'Days of the Week')



print ('----------------------------------------5')