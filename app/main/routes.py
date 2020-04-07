from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm

room_data = {}
# room_count = {}
# room_members = {}
turn = 0
consecutive_passes = 0
upcards = []

@main.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        if form.room.data not in room_data: #room_count:            
            room_data[form.room.data] = {'upcards': [], 'room_members': [], 'turn': 0, 
                                         'consecutive_passes': 0, 'room_count': 1, 'num_wins': [0, 0, 0, 0], 
                                         'stakes': int(form.stakes.data), 'gambling': [0, 0, 0, 0],
                                         'cards_left': [0, 0, 0, 0]}
            room_data[form.room.data]['room_members'].append(form.name.data)
            print(room_data)
            return redirect(url_for('.game'))
        else:
            if room_data[form.room.data]['room_count'] < 4:
                room_data[form.room.data]['room_members'].append(form.name.data)
                room_data[form.room.data]['room_count'] = room_data[form.room.data]['room_count'] + 1
                print(room_data)
                return redirect(url_for('.game'))
            else:
                print("room is full")

    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@main.route('/game')
def game():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('game.html', name=name, room=room)
