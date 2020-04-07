from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import routes, bigtwo, hand_checker
import json
import time


@socketio.on('joined', namespace='/game')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('left', namespace='/game')
def left(message):
	room = session.get('room')
	leave_room(room)
	emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
	routes.room_data[room]['room_count'] -= 1
	routes.room_data[room]['room_members'].remove(session.get('name'))


@socketio.on('startgame', namespace='/game')
def startgame():
	#TODO: make sure four people are in the room before 
	room = session.get('room')
	emit('start_game', {'msg': " "}, room=room)
	hands = bigtwo.deal(bigtwo.create_deck())
	json_dictionary = {}

	# determine who should go first, based on who has the three of diamonds
	routes.room_data[room]['turn'] = three_of_diamonds_index(hands)
	turnNumber = routes.room_data[room]['turn']
	whoseTurn = routes.room_data[room]['room_members'][turnNumber] #TODO: make this be whoever has the 3 of spades... can do this in this file by checking hands
	for i in range(4):
		json_dictionary[routes.room_data[room]['room_members'][i]] = hands[i]

	# update the dictionary with whose turn it is
	json_dictionary.update( {'whose_turn': whoseTurn})

	# update the dictionary with names and gambling amounts
	json_dictionary.update({'names': routes.room_data[room]['room_members']})
	json_dictionary.update({'gambling_amounts': routes.room_data[room]['gambling']})

	print(json_dictionary)
	json_object = json.dumps(json_dictionary)
	emit('deal', json_object, room=room)

@socketio.on('attemptedplay', namespace='/game')
def changeupcard(json):
	# If this move is valid, update the upcards and whose turn it is
	room = session.get('room')
	if (hand_checker.valid_move(routes.room_data[room]['upcards'], json['upcards'])):
		# update upcards and turn
		routes.room_data[room]['upcards'] = json['upcards']	
		routes.room_data[room]['turn'] = routes.room_data[room]['turn'] + 1 
		routes.room_data[room]['turn'] = routes.room_data[room]['turn'] % 4
		currentTurn = routes.room_data[room]['turn'] # temp variable cuz this code is getting hella index-y
		whoseTurn = routes.room_data[room]['room_members'][currentTurn]
		json.update({'whose_turn':whoseTurn})

		# update consecutive passes
		routes.room_data[room]['consecutive_passes'] = 0

		emit('delete_last_move', json)
		emit('change_upcard', json, room=room)
	else:
		emit('invalid_move', json)

@socketio.on('passturn', namespace='/game')
def passturn():
	room = session.get('room')

	# update current turn and consecutive passes
	routes.room_data[room]['turn'] = routes.room_data[room]['turn'] + 1 
	routes.room_data[room]['turn'] = routes.room_data[room]['turn'] % 4
	routes.room_data[room]['consecutive_passes'] += 1

	# check if three consecutive passes (round over)
	if routes.room_data[room]['consecutive_passes'] == 3:
		routes.room_data[room]['consecutive_passes'] = 0
		routes.room_data[room]['upcards'] = []
		emit('wipe_upcards', room=room)

	# update turn data and append to json object
	whoseTurn = routes.room_data[room]['room_members'][routes.room_data[room]['turn']]
	json = {}
	json.update({'whose_turn':whoseTurn})
	emit('pass_turn', json, room=room)

@socketio.on('endgame', namespace='/game')
def endgame(json):
	room = session.get('room')
	if (hand_checker.valid_move(routes.room_data[room]['upcards'], json['upcards'])):
		# tell everyone who won
		name = session.get('name')
		champ = {'name': name}
		emit('display_winner', champ, room=room)

		# update who won
		index_of_winner = routes.room_data[room]['room_members'].index(name)
		routes.room_data[room]['num_wins'][index_of_winner] += 1
		routes.room_data[room]['cards_left'][index_of_winner] = 0

		# update gambling info? will this work? TODO: Better way to do this?
		emit('determine_rankings', champ, room=room)
		time.sleep(5) # giving time for the rankings to be determined... needed for concurrency, i set arbitrary time tho lol
		print(routes.room_data[room]['cards_left'])
		determine_gambling_standings(room)
		print(routes.room_data[room]['gambling'])

		# fix consecutive passes
		routes.room_data[room]['consecutive_passes'] = 0

		#clear out previous cards
		emit('clear_board', room=room)
		startgame()
	else:
		emit('invalid_move', json)

@socketio.on('seedrankingarray', namespace='/game')
def seedrankingarray(json):
	room = session.get('room')
	name = session.get('name')
	index_of_winner = routes.room_data[room]['room_members'].index(name)
	routes.room_data[room]['cards_left'][index_of_winner] = json['num_left']

def three_of_diamonds_index(hands):
	for i in range(4):
		hand = hands[i]
		for card in hand:
			if card[0] == 3 and card[1] == 1:
				return i

def determine_gambling_standings(room):
	# Gotta do a lotta funky indexing n such lol
	cards_left = routes.room_data[room]['cards_left'].copy()
	cards_left.sort()
	print(cards_left)
	print(routes.room_data[room]['cards_left'])
	stakes = routes.room_data[room]['stakes']

	# UPDATE WINNER
	winner = routes.room_data[room]['cards_left'].index(0)
	routes.room_data[room]['gambling'][winner] += routes.room_data[room]['stakes']

	if cards_left[1] == cards_left[2] and cards_left[1] == cards_left[3]: # CASE WHERE 2-4 ARE TIED
		for i in range(4):
			if i != winner:
				routes.room_data[room]['gambling'][i] -= (stakes / 3)
	elif cards_left[1] == cards_left[2]: # CASE WHERE 2-3 ARE TIED
		last_place = routes.room_data[room]['cards_left'].index(cards_left[3])
		routes.room_data[room]['gambling'][last_place] -= (1.5 * stakes)
		for i in range(4):
			if i != winner and i != last_place:
				routes.room_data[room]['gambling'][i] += (stakes / 4)
	elif cards_left[2] == cards_left[3]: # CASE WHERE 3-4 ARE TIED
		second_place = routes.room_data[room]['cards_left'].index(cards_left[1])
		routes.room_data[room]['gambling'][second_place] += (0.5 * stakes)
		for i in range(4):
			if i != winner and i != second_place:
				routes.room_data[room]['gambling'][i] -= (stakes * 0.75)
	else: # ALL THINGS DIFFERENT
		last_place = routes.room_data[room]['cards_left'].index(cards_left[3])
		routes.room_data[room]['gambling'][last_place] -= (1.5 * stakes)
		second_place = routes.room_data[room]['cards_left'].index(cards_left[1])
		routes.room_data[room]['gambling'][second_place] += (0.5 * stakes)

#TODO: keep track of wins/losses (for gambling purposes)?
