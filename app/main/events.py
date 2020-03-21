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
    routes.room_members[room].remove(session.get('name'))


@socketio.on('startgame', namespace='/game')
def startgame():
	#TO DO:
	#make sure four people are in the room before 
	room = session.get('room')
	emit('start_game', {'msg': " "}, room=room)
	hands = bigtwo.deal(bigtwo.create_deck())
	json_dictionary = {}
	for i in range(4):
		json_dictionary[routes.room_members[room][i]] = hands[i]
	json_object = json.dumps(json_dictionary)
	emit('deal', json_object, room=room)
