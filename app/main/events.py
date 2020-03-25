from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import routes, bigtwo, hand_checker
import json


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
		print("NUMBER OF WINS:")
		print(routes.room_data[room]['num_wins'][index_of_winner])

		# fix consecutive passes
		routes.room_data[room]['consecutive_passes'] = 0

		#clear out previous cards
		emit('clear_board', room=room)
		startgame()
	else:
		emit('invalid_move', json)

def three_of_diamonds_index(hands):
	for i in range(4):
		hand = hands[i]
		for card in hand:
			if card[0] == 3 and card[1] == 1:
				return i
#TODO: Add end of round logic (ie who wins, and starting another round afterwards), keep track of wins/losses (for gambling purposes)?
