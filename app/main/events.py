from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import routes, bigtwo
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
    routes.room_count[room] -= 1
    print(routes.room_count[room])
    routes.room_members[room].remove(session.get('name'))


@socketio.on('startgame', namespace='/game')
def startgame():
	#TODO: make sure four people are in the room before 
	room = session.get('room')
	emit('start_game', {'msg': " "}, room=room)
	hands = bigtwo.deal(bigtwo.create_deck())
	json_dictionary = {}
	whoseTurn = routes.room_members[room][0] #TODO: make this be whoever has the 3 of spades... can do this in this file by checking hands
	for i in range(4):
		json_dictionary[routes.room_members[room][i]] = hands[i]
	json_dictionary.update( {'whose_turn': whoseTurn})
	print(json_dictionary)
	json_object = json.dumps(json_dictionary)
	emit('deal', json_object, room=room)

@socketio.on('attemptedplay', namespace='/game')
def changeupcard(json):
	# If this move is valid, update the upcards and whose turn it is
	if (bigtwo.valid_move(routes.upcards, json['upcards'])):
		routes.upcards = json['upcards']	
		room = session.get('room')
		routes.turn = routes.turn + 1 
		routes.turn = routes.turn % 4
		whoseTurn = routes.room_members[room][routes.turn]
		json.update({'whose_turn':whoseTurn})
		emit('delete_last_move', json)
		emit('change_upcard', json, room=room)
	else:
		emit('invalid_move', json)

@socketio.on('passturn', namespace='/game')
def passturn():
	room = session.get('room')
	routes.turn = routes.turn + 1 
	routes.turn = routes.turn % 4
	whoseTurn = routes.room_members[room][routes.turn]
	json = {}
	json.update({'whose_turn':whoseTurn})
	emit('pass_turn', json, room=room)
	

#TODO: Add end of round logic (ie who wins, and starting another round afterwards), keep track of wins/losses (for gambling purposes)?
