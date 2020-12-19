import twapi as tw
import pandas as pd
import stateanalyzer as st

def test_tw_authenticate():
	api = tw.TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_key, tw.access_secret)
	r = api.request('search/tweets', {'q':'hello'})
	responses = []
	for item in r.get_iterator():
		if 'text' in item:
			responses += item['text']
	# if authentication failed then assertion would return assertion failed
	assert len(responses) != 0

def test_list_of_govs():
	govs_username = pd.read_csv("data_folder/governors.csv")
	# checks if governor list exists for the 50 states + Puerto Rico
	assert len(govs_username) == 51

def test_common_word_search():
	api = tw.TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_key, tw.access_secret)
	r = api.request('search/tweets', {'q':'hello'})
	responses = []
	for item in r.get_iterator():
		if 'text' in item:
			responses += [item['text']]
	sentiment = tw.np.text_type_analysis(responses[0])
	assert sentiment[0] > -1.0 and sentiment[0] < 1.0

def test_sentiment():
	sentiment = tw.np.text_type_analysis("hate")
	#will give a negative sentiment since word is negative
	assert sentiment[1] == "Negative"

def test_unexistent_word_search(word):
	api = tw.TwitterAPI(tw.consumer_key, tw.consumer_secret, tw.access_key, tw.access_secret)
	r = api.request('search/tweets', {'q':"ejwbfiuerfb"})
	responses = []
	for item in r.get_iterator():
		if 'text' in item:
			responses += [item['text']]
	try:
		sentiment = tw.np.text_type_analysis(responses[0])
		assert sentiment[0] > -1.0 and sentiment[0] < 1.0
	except:
		#raises assertion error since word does not exist
		assert len(responses) > 1
