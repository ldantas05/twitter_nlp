from TwitterAPI import TwitterAPI
import credentials as twt
import requests
from requests.structures import CaseInsensitiveDict
import json
import pandas as pd
import nlpmain as np

#make request
consumer_key = twt.consumer_key
consumer_secret = twt.consumer_secret
access_key = twt.access_key
access_secret = twt.access_secret
bearer_token = twt.bearer_token

#keywords for search
keywords = "(pandemic OR covid OR corona OR virus OR disease)"

#write to file

def write(tweet_list, state):
	print(state)
	with open("data_folder/"+state+".txt", 'w', encoding="utf-8") as file:
		for x in tweet_list:
			file.write(x)

def get_tweets(handle, name, datein, dateout, state):
	all_tweets = []
	url = "https://api.twitter.com/1.1/tweets/search/{}/{}.json".format(twt.type_of_search, twt.dev)
	headers = CaseInsensitiveDict()
	headers["authorization"] = 'Bearer {}'.format(bearer_token)
	headers['content-type'] = 'application/json'
	data ={"query":"from:{} lang:en {}".format(handle, keywords), "fromDate":"{}0000".format(datein),  "toDate":"{}2359".format(dateout)}
	data = json.dumps(data)
	newest_tweets = requests.post(url, data=data, headers=headers)
	data = newest_tweets.json()
	try: 
		data = data['results']
	except:
		data = ["No results"]
	to_print = []
	for status in data:
		try:
			tweet = status['text']
		except:
			pass
		try:
			tweet = status['extended_tweet']['full_text']
		except:
			pass
		try:
			tweet = status['full_text']
		except:
			pass
		sentiments = np.text_type_analysis(tweet)
		date_of_creation = pd.to_datetime(status["created_at"]).date()
		to_print += [[name, state, tweet, date_of_creation, sentiments[0], sentiments[1]]]
	return to_print

def authenticate():
	api = TwitterAPI(consumer_key, consumer_secret, access_key, access_secret)



