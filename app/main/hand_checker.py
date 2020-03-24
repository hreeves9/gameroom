def valid_move(trump_hand, current_hand):
	if len(trump_hand) == 0:
		return True

	if len(trump_hand) != len(current_hand):
		return False

	ctrump_hand = []
	ccurrent_hand = []

	for item in trump_hand:
		ctrump_hand.append({"value" : convert_to_value(item), "suit": convert_to_suit(item)})

	for item in current_hand:
		ccurrent_hand.append({"value" : convert_to_value(item), "suit": convert_to_suit(item)})

	ctrump_hand = sort_hand(ctrump_hand)
	ccurrent_hand = sort_hand(ccurrent_hand)

	if len(ctrump_hand) == 1:
		return check_one_hand(ctrump_hand, ccurrent_hand)

	if len(ctrump_hand) == 2:
		if valid_two(ccurrent_hand):
			return check_two_hand(ctrump_hand, ccurrent_hand)
		return False

	if len(ctrump_hand) == 3:
		if valid_three(ccurrent_hand):
			return check_three_hand(ctrump_hand, ccurrent_hand)
		return False

	if len(ctrump_hand) == 5:
		if valid_five(ccurrent_hand):
			return check_five_hand(ctrump_hand, ccurrent_hand)
		return False

def convert_to_value(item):
	temp = item[:-1]
	dicti = {"3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14, "2":15}
	return dicti[temp]

def convert_to_suit(item):
	temp = item[-1]
	dicti = {"D":1, "C":2, "H":3, "S":4}
	return dicti[temp]

def card_greater(card1, card2):
	if card1["value"] > card2["value"]:
		return True
	elif card1["value"] == card2["value"]:
		if card1["suit"] > card2["suit"]:
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

def check_one_hand(trump_hand, current_hand):
	if current_hand[0]["value"] == trump_hand[0]["value"]:
		return current_hand[0]["suit"] > trump_hand[0]["suit"]
	return current_hand[0]["value"] > trump_hand[0]["value"]


def valid_two(current_hand):
	return (current_hand[0]["value"] == current_hand[1]["value"])

def check_two_hand(trump_hand, current_hand):
	if current_hand[0]["value"] < trump_hand[0]["value"]:
		return False
	if current_hand[0]["value"] == trump_hand[0]["value"]:
		return ((current_hand[0]["suit"] == 4) or (current_hand[1]["suit"] == 4))
	return True

def valid_three(current_hand):
	return ((current_hand[0]["value"] == current_hand[1]["value"]) and (current_hand[0]["value"] == current_hand[2]["value"]))

def check_three_hand(trump_hand, current_hand):
	return current_hand[0]["value"] > trump_hand[0]["value"]

def valid_five(current_hand):
	if is_straight(current_hand):
		return True
	if is_flush(current_hand):
		return True
	if is_four_of_a_kind(current_hand):
		return True
	if is_full_house(current_hand):
		return True
	return False

def get_hand_index(hand):
	hand_index = 0

	if is_straight(hand):
		hand_index = 1
	if is_flush(hand):
		hand_index = 2
	if is_full_house(hand):
		hand_index = 3
	if is_four_of_a_kind(hand):
		hand_index = 4
	if is_straight(hand) and is_flush(hand):
		hand_index = 5
		if hand[0]["value"] == 11:
			hand_index = 6
	return hand_index

def check_five_hand(trump_hand, current_hand):
	#["straight", "flush", "full_house", "four_of_a_kind", "straight_flush", "royal_flush"]
 	#[ 1, 2, 3, 4, 5, 6]
 	trump_hand_index = get_hand_index(trump_hand)
 	current_hand_index = get_hand_index(current_hand)

 	if current_hand_index > trump_hand_index:
 		return True
 	if current_hand_index < trump_hand_index:
 		return False

 	if current_hand_index == 1:
 		return check_straight(trump_hand, current_hand)

 	if current_hand_index == 2:
 		return check_flush(trump_hand, current_hand)

 	if current_hand_index == 3:
 		return check_full_house(trump_hand, current_hand)

 	if current_hand_index == 4:
 		return check_full_house(trump_hand, current_hand)

 	if current_hand_index == 5:
 		return check_flush(trump_hand, current_hand)
 	
 	if current_hand_index == 6:
 		return check_royal_flush(trump_hand, current_hand)

def check_straight(trump_hand, current_hand):
	if current_hand[4]["value"] == trump_hand[4]["value"]:
		return current_hand[4]["suit"] > trump_hand[4]["suit"]
	return current_hand[4]["value"] > trump_hand[4]["value"]

def check_flush(trump_hand, current_hand):
	#i guarantee on my mother there is a better way to do this
	if current_hand[4]["value"] == trump_hand[4]["value"]:
		if current_hand[3]["value"] == trump_hand[3]["value"]:
			if current_hand[2]["value"] == trump_hand[2]["value"]:
				if current_hand[1]["value"] == trump_hand[1]["value"]:
					if current_hand[0]["value"] == trump_hand[0]["value"]:
						return current_hand[0]["suit"] > trump_hand[0]["suit"]
					return current_hand[0]["value"] > trump_hand[0]["value"]
				return current_hand[1]["value"] > trump_hand[1]["value"]
			return current_hand[2]["value"] > trump_hand[2]["value"]
		return current_hand[3]["value"] > trump_hand[3]["value"]
	return current_hand[4]["value"] > trump_hand[4]["value"]

def check_full_house(trump_hand, current_hand):
	return current_hand[2]["value"] > trump_hand[2]["value"]

def check_royal_flush(trump_hand, current_hand):
	return current_hand[0]["suit"] > trump_hand[0]["suit"]

def is_straight(current_hand):
	i = 1
	while i < 5:
		if (current_hand[i]["value"] - 1) != current_hand[i-1]["value"]:
			return False
		i += 1
	return True

def is_flush(current_hand):
	suit = current_hand[0]["suit"]
	for item in current_hand:
		if item["suit"] != suit:
			return False
	return True

def is_four_of_a_kind(current_hand):
	#when cards are in order, either first four or last four will be equal
	#therefore, compare both sets against themselves. if one of them is true, return true

	first_four = True
	last_four = True

	first_four_value = current_hand[0]["value"]
	i = 0
	while i < 4:
		if current_hand[i]["value"] != first_four_value:
			first_four = False
		i += 1

	last_four_value = current_hand[4]["value"]
	i = 1
	while i < 5:
		if current_hand[i]["value"] != last_four_value:
			last_four = False
		i += 1

	return (first_four or last_four)

def is_full_house(current_hand):
	# two scenarios : [X,X,X,Y,Y] or [X,X,Y,Y,Y]
	#check both, either one appears, return true
	threes_first = ((current_hand[0]["value"] == current_hand[1]["value"]) and (current_hand[0]["value"] == current_hand[2]["value"]))
	pair_second = (current_hand[3]["value"] == current_hand[4]["value"])
	scenario1 = threes_first and pair_second

	threes_second = ((current_hand[2]["value"] == current_hand[3]["value"]) and (current_hand[2]["value"] == current_hand[4]["value"]))
	pair_first = (current_hand[0]["value"] == current_hand[1]["value"])
	scenario2 = pair_first and threes_second

	return (scenario1 or scenario2)
