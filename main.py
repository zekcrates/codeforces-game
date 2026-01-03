from flask import Flask, render_template, request, session, redirect, url_for
import uuid
from cf import check_solution, user_exists
from problems import get_problem
from flask_socketio import SocketIO, send, emit, join_room


app = Flask(__name__)
app.secret_key = "dev-secret-key"
socketio = SocketIO(app)
waiting_queue = []
active_games = {}


@socketio.on('message')
def handle_message(data):
    print("message received: ", data)


@app.route('/')
def index():
    return render_template("random.html")


@socketio.on('join_game')
def handle_join(data):
    handle = data.get("handle")
    if not handle or not user_exists(handle):
        emit('error_msg', {'msg': 'Invalid CF handle'})
        return 
    player_data = {'handle': handle, 'sid': request.sid}
    if waiting_queue:
        opponent = waiting_queue.pop(0)
        game_id = str(uuid.uuid4())
        problem = get_problem()

        active_games[game_id] = {
            'player1': player_data,
            'player2': opponent,
            'problem': problem,
            'winner': None
        }


        join_room(game_id)
        join_room(game_id, sid=opponent['sid'])
        emit('match_found', {
            'game_id': game_id,
            'opponent': opponent['handle'], 
            'problem': problem 

        }, room=game_id)
        emit('match_found', {
            'game_id': game_id,
            'opponent': handle,
            'problem': problem
        }, room=opponent['sid'])
    
    else:
        waiting_queue.append(player_data)
        emit('waiting', {'msg': 'Searching for opponent...'})


@socketio.on('check_solution')
def handle_check(data):
    game_id = data.get('game_id')
    handle = data.get('handle')
    game= active_games.get(game_id)
    if not game or game['winner']:
        return 
    
    emit('game_over', {'winner': handle}, room=game_id)

@socketio.on('leave_queue')
def handle_leave():
    global waiting_queue
    waiting_queue = [p for p in waiting_queue if p['sid'] != request.sid]

if __name__ == '__main__':
    socketio.run(app, debug=True)