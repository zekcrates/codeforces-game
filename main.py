from flask import Flask, render_template, request,redirect, jsonify
import uuid

from problems import get_problem

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("random.html")

waiting_queue = []  # list of player IDs
active_games = {} 
@app.route('/random', methods=['POST'])
def random_join():
    player_id = str(uuid.uuid4())
    if waiting_queue:
        opponent_id = waiting_queue.pop(0)
        problem = get_problem()  # This is a dict with full problem info
        game_id = f"{player_id}_{opponent_id}"
        active_games[game_id] = {
            'player1': player_id,
            'player2': opponent_id,
            'problem': problem,  # store full problem
            'winner': None
        }
        return jsonify({
            'status': 'matched',
            'player_id': player_id,
            'game_id': game_id,
            'problem': problem,       
            'opponent_id': opponent_id
        })
    else:
        waiting_queue.append(player_id)
        return jsonify({
            'status': 'waiting',
            'player_id': player_id
        })


if __name__ == '__main__':
    app.run(debug=False)