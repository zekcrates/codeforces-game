from flask import Flask, render_template, request, session
import uuid
from cf import user_exists
from problems import get_problem

app = Flask(__name__)
app.secret_key = "dev-secret-key"  

waiting_queue = []
active_games = {}  


@app.route('/')
def index():
    return render_template("random.html")


@app.route('/random', methods=['GET', 'POST'])
def random_join():

    if request.method == 'POST':
        cf_handle = request.form.get("handle")

        if not cf_handle:
            return "CF handle required", 400

        if not user_exists(cf_handle):
            return "CF handle not present", 400

        player_id = str(uuid.uuid4())

        session["cf_handle"] = cf_handle
        session["player_id"] = player_id

        player_data = {
            "player_id": player_id,
            "handle": cf_handle
        }

        if waiting_queue:
            opponent = waiting_queue.pop(0)
            problem = get_problem()
            game_id = f"{player_id}_{opponent['player_id']}"

            active_games[game_id] = {
                "player1": player_data,
                "player2": opponent,
                "problem": problem,
                "winner": None
            }

            return render_template(
                "random.html",
                status="matched",
                player_id=player_id,
                cf_handle=cf_handle,
                opponent_handle=opponent["handle"],
                problem=problem
            )

        waiting_queue.append(player_data)
        return render_template(
            "random.html",
            status="waiting",
            player_id=player_id,
            cf_handle=cf_handle
        )

    return render_template(
        "random.html",
        status="waiting",
        player_id=session.get("player_id"),
        cf_handle=session.get("cf_handle")
    )


@app.route('/leave', methods=['POST'])
def leave_game():
    player_id = session.get("player_id")

    if player_id:
        global waiting_queue
        waiting_queue = [
            p for p in waiting_queue if p["player_id"] != player_id
        ]

    session.clear()

    return render_template("random.html")


if __name__ == '__main__':
    app.run(debug=True)
