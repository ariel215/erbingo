from flask import Flask, make_response, redirect, render_template, request, url_for
from http import HTTPStatus
from flask_socketio import SocketIO, send
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
games = {}

@app.route("/")
def home():
    # todo: keep players from racing to the same id
    return render_template("index.html",games=games)


@app.route("/games/new", methods=['POST', 'GET'])
def new_game():
    if  request.method == 'GET':
        return render_template('new_game.html')
    elif request.method == 'POST':
        game = Game(int(request.form['size']))
        games[game.id] = game
        return redirect(url_for("show_game", game_id=game.id))
    else:
        return 'invalid method', HTTPStatus.METHOD_NOT_ALLOWED
    
@app.route("/games/<int:game_id>", methods=['GET'])
def show_game(game_id:int):
    if game_id not in games:
        return '', HTTPStatus.NOT_FOUND
    return render_template('game.html',game=games[game_id])

def make_player_id():
    player_id = randint(0, 10_000)
    while player_id in players:
        player_id = randint(0,10_000)
    players.add(player_id)
    return player_id


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