#!/usr/bin/env python
# encoding: utf-8
#Author - Nelson Leonardo

import tweepy
import tkinter as tk
import credentials as twt
import sys


#credentials
consumer_key = twt.consumer_key
consumer_secret = twt.consumer_secret
access_key = twt.access_key
access_secret = twt.access_secret


#authenticate
def authenticate():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	return api

def write(tweet_list, type_of_write):
	with open("output.txt", 'w', encoding="utf-8") as file:
		file.write(type_of_write)
		for x in tweet_list:
			file.write(x)


#grab user tweets
def user_tweets(name, tweet_num=0):
	all_tweets = []
	api = authenticate()
	try:
		newest_tweets = api.user_timeline(screen_name=name, count = tweet_num)
	except:
		print("No user found")
		return
	all_tweets.extend(newest_tweets)
	i = 1
	to_print = ["Tweets from: @" + name + "\n"]
	for status in all_tweets:
		to_print += [str(i)+ ". "+ status.text +"\n"]
		i+=1
	write(to_print, "User Tweets \n")

#grab tweets by keyword
def key_word_search(word, tweet_num=0):
	to_print = []
	all_tweets = []
	api = authenticate()
	try:
		newest_tweets = api.search(q=word, count=tweet_num)
	except:
		print("No keyword found")
		return
	all_tweets.extend(newest_tweets)
	i = 1
	for status in all_tweets:
		to_print += [str(i)+ ". "+ status.user.screen_name + ":" + status.text +"\n"]
		i+=1
	write(to_print, "Keyword Search:" + word+"\n")



#GUI
def start():
	root = tk.Tk()
	def quit():
		root.destroy()
	def retrieve():
		user_tweets('@'+ent_user.get(), int(ent_count.get()))
	def keyword():
		key_word_search(ent_hashtag.get(), ent_count.get())

	root.title("Twitter Sentiment Reader")
	lbl_user = tk.Label(root, text="Twitter User without @").grid(row = 0, column =0)
	ent_user = tk.Entry(root, bd=5)
	ent_user.grid(row=0, column = 2)
	lbl_hashtag = tk.Label(root, text="Enter the keyword").grid(row=1, column=0)
	ent_hashtag = tk.Entry(root, bd=5)
	ent_hashtag.grid(row=1, column=2)
	lbl_count = tk.Label(text="How many tweets to display?").grid(row=2, column=0)
	ent_count = tk.Entry(root, bd= 5)
	ent_count.grid(row=2, column=2)
	btn_user = tk.Button(root, text="Search by User", command=retrieve).grid(row=3, column=0)
	btn_hashtag = tk.Button(root, text="Search by Keyword", command=keyword).grid(row=3, column=1)
	btn_quit = tk.Button(root, text="quit", command=quit).grid(row=3, column=2)
	root.mainloop()





if __name__ == "__main__":
	start()
