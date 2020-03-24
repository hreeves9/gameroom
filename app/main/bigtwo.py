import random
from . import routes

cardsValues = {3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K", 14:"A", 15:"2"};

suitValues = {1:"d", 2:"c", 3:"h", 4:"s"};

def create_deck():
	#double for loop with card values and suits to populate a list
	#also shuffle the deck here
	#return a list
	returnList = []

	for key in cardsValues:
		for key2 in suitValues:
			returnList.append([key, key2])

	for i in range(1000):
		location1 = random.randint(0,51)
		location2 = random.randint(0,51)
		temp = returnList[location1];

		returnList[location1] = returnList[location2]
		returnList[location2] = temp


	return returnList

def card_greater(card1, card2):
	if card1[0] > card2[0]:
		return True
	elif card1[0] == card2[0]:
		if card1[1] > card2[1]:
			return True
	return False

def sort_hand(hand):
	swapbool = True
	n = len(hand) - 1
	x = hand
	while swapbool:
		swapbool = False
		for i in range(0,n):
			if card_greater(x[i], x[i+1]):
				temp = x[i]
				x[i] = x[i+1]
				x[i+1] = temp
				swapbool = True
		n -= 1
	return x

def deal(deck):
	temp = [deck[0:13], deck[13:26], deck[26:39], deck[39:52]] #fixed dealing keys
	returnList = []
	for item in temp:
		returnList.append(sort_hand(item))

	return returnList
