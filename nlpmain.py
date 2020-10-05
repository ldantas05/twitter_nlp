# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import tkinter as tk


client = client = language.LanguageServiceClient.from_service_account_json(r"key.json")

def wr(text, sentiment_read, entity_counter):
	with open("output.txt", 'w', encoding="utf-8") as file:
		file.write("Overall Sentiment Analysis\n\n")
		file.write(text)
		file.write(sentiment_read)
		file.write("Types of entities:\n")
		for x in entity_counter:
			file.write(x[0] + ' ')
			file.write(str(x[1]) + '\n')

def text_type_analysis(text):
	document = types.Document(
    	content=text,
    	type=enums.Document.Type.PLAIN_TEXT)
	encoding_type = enums.EncodingType.UTF8
	sentiment = client.analyze_sentiment(document=document).document_sentiment
	response = client.analyze_entities(document, encoding_type=encoding_type)
	overall_sentiment = "Neutral"
	if sentiment.score <=-0.25:
		overall_sentiment = "Negative"
	elif sentiment.score >= 0.25:
		overall_sentiment = "Positive"
	entity_list_unique = []
	list_entity = []
	for entity in response.entities:
		list_entity += [enums.Entity.Type(entity.type).name]
		if enums.Entity.Type(entity.type).name not in entity_list_unique:
			entity_list_unique+=[enums.Entity.Type(entity.type).name]
	counter = []
	for entity in entity_list_unique:
		counter += [[entity+":", list_entity.count(entity)]]
	entity_counter = counter
	sentiment_read = 'Overall Sentiment: {}, {}'.format(sentiment.score, overall_sentiment)

	return [sentiment.score, overall_sentiment]

if __name__ == "main":
	root = tk.Tk()
	root.geometry("800x800")
	def text_analyze():
		text_type_analysis(ent_text.get("1.0", 'end-1c'))
	def quit():
		root.destroy()
	lbl_text =  tk.Label(root, text="Input text").grid(row=0, column=0)
	ent_text = tk.Text(root, bd=3)
	ent_text.grid(row = 0, column = 2)
	btn_text = tk.Button(root, text="Analyze text", command = text_analyze).grid(row=2, column=0, columnspan=5)
	btn_quit = tk.Button(root, text="Quit", command = quit).grid(row=2, column=6)

	root.mainloop()