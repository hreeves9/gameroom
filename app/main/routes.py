from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm

room_count = {}

@main.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        if form.room.data not in room_count:
            room_count[form.room.data] = 1
            return redirect(url_for('.game'))
        else:
            if room_count[form.room.data] < 4:
                room_count[form.room.data] += 1
                print("HELLO")
                return redirect(url_for('.game'))
            else:
                print("uh oh spaghetti os. the room is full.")

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
