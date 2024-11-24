from ..app import app, socketio, games, players, Game
import pytest 

@pytest.fixture
def app_client():
    return app.test_client()

@pytest.fixture
def socket_client(app_client):
    return socketio.test_client(app,flask_test_client=app_client)

def test_home(app_client):
    assert app_client.get("/").status_code == 200

def test_new_game(app_client):
    len_before = len(games)
    response = app_client.post("/games/new", data={
        'name': 'test',
        'size': 3
    }, follow_redirects=True)
    assert len(games) - len_before == 1
    assert len(response.history) == 1
    
@pytest.fixture
def game():
    return Game("test1", 4)

def test_connect(socket_client):
    n_players = len(players)
    socket_client.connect()
    assert len(players) - n_players == 1
