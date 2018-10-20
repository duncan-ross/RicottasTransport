import random
import json

chat_history = {}

def main():
	with open('data.json') as f:
		chat_history = json.load(f)

def end():
	with open('data.json', 'w') as f:
		json.dump(chat_history, f)
		

def response(text):
	if text in chat_history:
		nodes = chat_history[text]
		total_responses = sum([i[1] for i in nodes])
		ran = random.random()
		current = 0.0
		for i in nodes:
			prob = i[1]/total_responses
			if ran > current and ran < prob+current:
				return i[0]
			current += prob
	else:
		chat_history[text] = []


def learn(text, response):
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

