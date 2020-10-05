#author Nelson Lenonardo Gonzalez Dantas Copyright 2020
import twapi as tw
import nlpmain as gg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import chart_studio as py 
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, plot
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from datetime import datetime
from datetime import date
from tkinter import messagebox



#Getting governors names and tweets and sentiment


def plot_in_map(metrics):
	avgs_total_time = metrics.groupby(['State Abb'], as_index=False).mean()
	data_map = dict(type='choropleth',
	locations = avgs_total_time['State Abb'],
	locationmode = 'USA-states',
	colorscale = 'Reds',
	text = avgs_total_time['State Abb'],
	z = avgs_total_time['Sentiment Score'],
	colorbar = {'title':"Sentiment Analysis"})
	layout = dict(title = 'Average Sentiment',
		geo = dict(scope='usa'))
	choromap = go.Figure(data = [data_map],layout = layout)
	plot(choromap)

def plot_scatter(metrics):
	avgs_tweeted_date = metrics[["Date Tweeted", "State Abb", "Sentiment Score"]]
	#avgs_tweeted_date = pd.DataFrame(columns = ["Date", "State", "Sentiment"], data=[pd.to_datetime(metrics["Date Tweeted"]).dt.strftime('%Y %b %d'), metrics["State Abb"], metrics["Sentiment Score"]])
	avgs_tweeted_date=avgs_tweeted_date.groupby(["Date Tweeted", "State Abb"])["Sentiment Score"].mean().reset_index()
	df = pd.pivot_table(avgs_tweeted_date, values='Sentiment Score', index=['Date Tweeted'],columns='State Abb')
	fig = go.Figure()
	for col in df.columns:
		fig.add_trace(go.Scatter(x=df.index, y=df[col].values, name = col,mode = 'markers+lines', line=dict(shape='linear'), connectgaps=True))
	fig.show()

def get_tweets(govs, datein, dateout):
	to_df = []
	for x in range(len(govs)):
		to_df += tw.get_tweets(govs.iloc[x]["Handle"], govs.iloc[x]["Name"], datein, dateout, govs.iloc[x]["Abb"])
	metrics = pd.DataFrame(to_df, columns = ["Name", "State Abb", "Tweet", "Date Tweeted", "Sentiment Score", "Overall Sentiment"])
	#plot_in_map(metrics)
	plot_scatter(metrics)

def get_govs(datein, dateout, state = ""):
	govs_username = pd.read_csv("data_folder/governors.csv")
	get_tweets(govs_username, datein, dateout)


#plt.show()



#creating basic GUI
def start():
	root = tk.Tk()

	#initial calendar
	def start_date():
		strt = tk.Tk()
		def ret():
			ent_initial_date.delete(0, "end")
			new_val = cal.selection_get()
			new_val = new_val.strftime("%Y%m%d")
			ent_initial_date.insert(0, new_val)
			strt.destroy()
		cal = Calendar(strt, selectmode='day')
		cal.pack(fill="both", expand=True)
		tk.Button(strt, text="Select", command=ret).pack()
		strt.mainloop()
	#end initial calendar

	#end date
	def final_date():
		end_date = tk.Tk()
		def ret():
			ent_final_date.delete(0, "end")
			new_val = cal.selection_get()
			new_val = new_val.strftime("%Y%m%d")
			ent_final_date.insert(0, new_val)
			end_date.destroy()
		cal = Calendar(end_date, selectmode='day')
		cal.pack(fill="both", expand=True)
		tk.Button(end_date, text="Select", command=ret).pack()
		end_date.mainloop()
	#end end date

	#Start State Search
	def strt_search():
		if ((ent_initial_date.get() < ent_final_date.get()) or (ent_final_date.get() > date.today().strftime('%y%m%d'))):
			messagebox.showerror("Date error", "The selected date is invalid please type or select another date")
		elif ((ent_initial_date.get() =="") or (ent_final_date.get() =="")):
			messagebox.showerror("Date error", "The selected date is invalid please type or select another date")
		get_govs(ent_initial_date.get(), ent_final_date.get())
	lbl_initial = tk.Label(root, text="Enter initial date").grid(row=0, column = 0)
	ent_initial_date = tk.Entry(root, validate = "focusin", validatecommand = start_date)
	ent_initial_date.grid(column = 1, row = 0)
	bt_initial_date = tk.Button(root, text="Select Start Date", command=start_date)
	bt_initial_date.grid(column =2, row=0)
	lbl_final = tk.Label(root, text="Enter final date").grid(row=1, column = 0)
	ent_final_date = tk.Entry(root, validate = "focusin", validatecommand = final_date)
	ent_final_date.grid(column = 1, row = 1)
	bt_final_date = tk.Button(root, text="Select End Date", command=final_date)
	bt_final_date.grid(column =2, row=1)
	btn_strt_src = tk.Button(root, text="Search", command=strt_search)
	btn_strt_src.grid(column =0, row=2, columnspan=3, sticky = tk.W+tk.E)
	s = ttk.Style(root)
	s.theme_use('clam')
	root.mainloop()



start()