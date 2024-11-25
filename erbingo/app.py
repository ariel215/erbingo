from flask import Flask, redirect, render_template, request, url_for
from http import HTTPStatus
from flask_socketio import SocketIO
from random import randint
from .game import Game, Board
from pathlib import Path

_HERE = Path(__file__).parent
app = Flask(__name__)
socketio = SocketIO(app)
Board.load_squares(_HERE / "data" / "goals.txt")

# this isn't an actual secret because we're not storing 
# any actual data, just tracking users
app.secret_key = b"bingus pingus" 
players = set()
app.game = None

@app.route("/")
def home():
    if not app.game: 
        return redirect(url_for('new_game'))
    else:
        return redirect(url_for('play',game_id=app.game.id))


@app.route("/new_game", methods=['POST', 'GET'])
def new_game():
    if  request.method == 'GET':
        return render_template('new_game.html')
    elif request.method == 'POST':
        app.game = Game(int(request.form['size']))
        return redirect(url_for("play"))
    else:
        return 'invalid method', HTTPStatus.METHOD_NOT_ALLOWED
    
@app.route("/play", methods=['GET'])
def play():
    if not app.game:
        return redirect(url_for('new_game'))
    return render_template('game.html',game=app.game)


@socketio.on('mark_square')
def mark_square(json):
    row = json['row']
    col = json['col']
    socketio.emit("mark_square", data={
        "row": row,
        "col": col,
    }, include_self=False)


@socketio.on('unmark_square')
def unmark_square(json):
    row = json['row']
    col = json['col']
    socketio.emit("unmark_square",data={
        "row": row,
        "col": col,
    }, include_self=False)


if __name__ == "__main__":
    socketio.run(app)