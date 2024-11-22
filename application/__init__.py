from flask import Flask, make_response, redirect, render_template, request, url_for
from http import HTTPStatus
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

games = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/games/new", methods=['POST', 'GET'])
def new_game():
    if  request.method == 'GET':
        return render_template('new_game.html')
    elif request.method == 'POST':
        id = add_game(request.form)
        return {
            "id": id
        }
    else:
        return 'invalid method', HTTPStatus.METHOD_NOT_ALLOWED
    
@socketio.on('join')
def join_game(game_id, player_id):
    if game_id not in games:
        send({'error': {
            'missing game': game_id
        }})
    game = games[game_id]
    if len(game.players) >= 2:
        send({
            'error': 'game full'
        })
    if player_id in game.players:
        send({'error': {
            'already_joined': player_id
        }})

    game.players.add(player_id)
    send('ok')


@app.route("/games/<int:id>", methods=['GET'])
def join_game(game_id, player_id):
    if game_id not in games:
        return '', HTTPStatus.NOT_FOUND
    
    return render_template('game.html',game=games[game_id],player=players[player_id])
    
@socketio.on('mark_square')
def mark_square(game_id,player_id,row,col):
    raise NotImplemented
    




if __name__ == "__main__":
    socketio.run(app)