import tweepy, json, re

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
user_id = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



### when favorites are existed
# tweets = json.load(open('tweets.json','r',encoding='utf8'))
# oldest = tweets[-1]['id'] - 1
# tweetsapi = api.user_timeline(user_id=user_id,count='200',max_id=oldest)

### when no favorites is existed
tweets = []
tweetsapi = api.user_timeline(user_id=user_id,count='200')


for t in tweetsapi:
# for t in tweets:
    t_json = t._json
    tweets.append(t_json)
    tweets.append(t)
file=open('tweets.json','w',encoding='utf8')
file.write(json.dumps(tweets))
file.close()



usernames = []
users = []
followings = json.load(open('followings.json','r',encoding='utf8'))
for following in followings:
    users.append(following)
    usernames.append(following['screen_name'].lower())
followers = json.load(open('followers.json','r',encoding='utf8'))
for follower in followers:
    users.append(follower)
    usernames.append(follower['screen_name'].lower())


followingsapi = api.get_friends(user_id=user_id)
followersapi = api.get_followers(user_id=user_id)

following_list=[]
for f in followingsapi:
    f_json = f._json
    if f_json in users:
        pass
    else:
        following_list.append(f_json)
file=open('followings.json','w',encoding='utf8')
file.write(json.dumps(following_list))
file.close()

followers_list=[]
for f in followersapi:
    f_json = f._json
    if f_json in users:
        pass
    else:
        followers_list.append(f_json)
file=open('followers.json','w',encoding='utf8')
file.write(json.dumps(followers_list))
file.close



### when favorites are existed
# favorites = json.load(open('favorites.json','r',encoding='utf8'))
# oldest = favorites[-1]['id'] - 1
# favoritesapi = api.get_favorites(user_id=user_id,max_id=oldest)

### when no favorite is existed
favoritesapi = api.get_favorites(user_id=user_id)
favorites = []


for f in favoritesapi:
    f_json = f._json
    favorites.append(f_json)
file=open('favorites.json','w',encoding='utf8')
file.write(json.dumps(favorites))
file.close()


favorites = json.load(open('favorites.json','r',encoding='utf8'))

for favorite in favorites:
    try:
        api.destroy_favorite(favorite['id'])
    except:
        pass



for tweet in tweets:
    tweettext = str( tweet['text'].lower())

    if tweet['favorite_count'] <= 2:
        try:
            username = re.findall(r'@(\w+)', tweettext)[0].lower()
            if username in usernames:
                pass
            else:
                try:
                    api.destroy_status(tweet['id'])
                except:
                    pass
        except:
            try:
                api.destroy_status(tweet['id'])
            except:
                pass

    elif tweettext.startswith("@") == True:
        username = re.findall(r'@(\w+)', tweettext)[0].lower()
        if username in usernames:
            pass
        else:
            try:
                api.destroy_status(tweet['id'])
            except:
                pass

    elif tweettext.startswith("rt @") == True:
        try:
            api.unretweet(tweet['id'])
        except:
            pass

