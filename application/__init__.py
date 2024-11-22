from flask import Flask, make_response, redirect, render_template, request, url_for, session
from http import HTTPStatus
from flask_socketio import SocketIO, send
from random import randint
from .game import Game

app = Flask(__name__)
socketio = SocketIO(app)

# this isn't an actual secret because we're not storing 
# any actual data, just tracking users
app.secret_key = b"bingus pingus" 

players = set()
games = {}

@app.route("/")
def home():
    # todo: keep players from racing to the same id
    session["player_id"] = randint(0,10000)
    return render_template("index.html")


@app.route("/games/new", methods=['POST', 'GET'])
def new_game():
    if  request.method == 'GET':
        return render_template('new_game.html')
    elif request.method == 'POST':
        
        game = Game(request.form['name'], request.form['size'])
        games[game.id] = game
        return redirect(url_for("show_game", game_id=game.id))
    else:
        return 'invalid method', HTTPStatus.METHOD_NOT_ALLOWED
    
@app.route("/games/<int:id>", methods=['GET'])
def show_game(game_id:int):
    if game_id not in games:
        return '', HTTPStatus.NOT_FOUND
    return render_template('game.html',game=games[game_id])


@socketio.on('join')
def join_game(game_id):
    if game_id not in games:
        socketio.emit('join',{
            'ok': False,
            'error': {
            'missing game': game_id
        }}, namespace=f"/games/{game_id}",
        )
    game = games[game_id]
    player_id = session['player_id']
    if len(game.players) >= 2:
        socketio.emit('join',{
            'ok': False,
            'error': 'game full'
        }, namespace=f"/games/{game_id}")
    if player_id in game.players:
        socketio.emit('join',{'error': {
            'already_joined': player_id
        }}, namespace=f"/games/{game_id}")

    game.players.add(player_id)
    if len(game.players) == 2:
        socketio.emit('start', namespace=f"/games/{game_id}")
    else:
        socketio.emit('join', {'ok'})

@socketio.on('mark_square')
def mark_square(game_id,row,col):
    player_id = session['player_id']
    games[game_id].squares[row][col].player = player_id
    socketio.emit("mark", {
        "row": row,
        "col": col,
        "player": player_id
    }, namespace=f"/games/{game_id}", include_self=False)


@socketio.on('unmark_square')
def unmark_square(game_id, row, col):
    player_id = session['player_id']
    games[game_id].squares[row][col].player = None

    socketio.emit("mark",{
        "row": row,
        "col": col,
        "player": None
    }, namespace=f"/games/{game_id}", include_self=False)


if __name__ == "__main__":
    socketio.run(app)