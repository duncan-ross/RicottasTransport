import random
import json
import sys
import csv
import spacy
import os
import glob
import string
import re

table = str.maketrans({key: None for key in string.punctuation})
data_file_name = 'data.json'

def start(text):
	chat_history = {}
	with open(data_file_name, 'r') as f:
		chat_history = json.load(f)
		talk = response(chat_history, text.strip().lower())
		print("Ricottas:", talk)
		os.system("say " + talk)
		# shouldLearn = input("Learn or Chat: ")
		# if ( shouldLearn == "learn"):
		# 	learnChatterbot(chat_history)
		# 	learnMovies(chat_history, "movie_lines.tsv")
		# 	learnMovies(chat_history, "movie_lines 2.tsv")
		# else:
			# runChat(chat_history)
		
		#learnChatterbot(chat_history)
		# learnQuestionAnswer(chat_history)
		# learnJeopardy(chat_history)
		# closeFile(chat_history)

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def learnQuestionAnswer(chat_history):
	path = '/Users/duncanross/Downloads/stanford-question-answering-dataset/'
	for filename in glob.glob(os.path.join(path, '*.json')):
		with open(filename, 'r') as f:
			data = json.load(f)
			for element in data["data"]:
				for paragraph in element["paragraphs"]:
					for qa in paragraph["qas"]:
						for answer in qa["answers"]:
							learn(chat_history, qa["question"].strip().lower(), answer["text"].strip().lower())

def learnJeopardy(chat_history):
	path = '/Users/duncanross/Downloads/Jeopardy'
	for filename in glob.glob(os.path.join(path, '*.json')):
		with open(filename, 'r') as f:
			data = json.load(f)
			for element in data:
				clean = cleanhtml(element["question"])
				learn(chat_history, clean.strip().lower(), element["answer"].strip().lower())
	
def learnChatterbot(chat_history):
	path = '/Users/OsmarCoronel/Desktop/UIUC/Junior/Fall/HackGT' 
	for filename in glob.glob(os.path.join(path, '*.data')):
		with open(filename, 'r') as f:
			spamreader = csv.reader(f, delimiter=':')
			previous = None
			for row in spamreader:
				if previous is None:
					previous = row[1]
				else:
					learn(chat_history, previous, row[1])
					previous = row[1]
	
def learnMovies(chat_history, movie_name):
	with open(movie_name, 'r') as f:
		tsvin = csv.reader(f, delimiter='\t')
		convoNum = None
		previous = None
		for row in tsvin:
			if 2 >= len(row):
				continue
			if convoNum is None:
				convoNum = row[2]
			if row[2] == convoNum and previous is not None:
				learn(chat_history, previous.strip().lower(), row[4].strip().lower())
				previous = row[4]
			else:
				previous = row[4]
				convoNum = row[2]
def runChat(chat_history):
	line = input("User: ")
	while line != "quit":
		talk = response(chat_history, line.strip().lower())
		print("Ricottas:", talk)
		os.system("say " + talk)
		line = input("User: ")

def learnChat(chat_history):
	for line in sys.stdin:
		text, response = line.split("|")
		text = text.strip().lower()
		response = response.strip().lower()
		learn(chat_history, text, response)

def closeFile(chat_history):
	with open(data_file_name, 'w') as f:	
		json.dump(chat_history, f)

def response(chat_history, text):
	text = text.translate(table)
	nlp = spacy.load('en')
	if text in chat_history:
		return selectRandom(chat_history, text)
	else:
		doc2 = nlp(text)
		for i in chat_history.keys():
			doc1 = nlp(i)
			if doc2.similarity(doc1) > .8:
				return selectRandom(chat_history, i)
		print ("Sorry I do not know that! :(")
		# response = input("How should I respond: ")
		# chat_history[text] = [(response, 1)]
		return ""#response

def selectRandom(chat_history, text):
	nodes = chat_history[text]
	total_responses = sum([i[1] for i in nodes])
	ran = random.random()
	current = 0.0
	for i in nodes:
		prob = i[1]/total_responses
		if ran > current and ran < prob+current:
			return i[0]
		current += prob
	return ""

def learn(chat_history, text, response):
	text = text.translate(table)
	response = response.translate(table)
	if text in chat_history:
		nodes = chat_history[text]
		for i in range(len(nodes)):
			if response == nodes[i][0]:
				t,c = nodes[i]
				nodes[i] = (t, c+1)
				break
		else:
			nodes.append((response, 1.0))
	else:
		chat_history[text] = [(response, 1.0)]
