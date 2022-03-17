import dataclasses
import logging
from collections import defaultdict

import randomname
import socketio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from trivial.models import Choice, Config, Question, Trivia, User
from trivial.random import get_random_trivia
from trivial.state import TriviaGame

log = logging.getLogger(__name__)


###################
# In Memory State #
###################

sid_to_user: dict[str, User] = {}
# Active games
games = {}

# Additional session data
sessions = {}


#######################
# REST Endpoints      #
#######################
async def get_trivia(request):
    trivia_length = request.query_params.get('trivia_length', 10)
    trivia = await get_random_trivia(trivia_length)
    return JSONResponse(trivia)


routes = [
    Route('/gen', get_trivia)
]

app = Starlette(debug=True, routes=routes)
# app.mount('/', StaticFiles(directory='static'), name='static')

#######################
# Websocket Endpoints #
#######################
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app.mount('/sio', socketio.ASGIApp(sio))


@sio.on("connect")
def sio_connect(sid, environ):
    """Track user connection"""

    name = randomname.get_name().replace('-', ' ').title()
    sid_to_user[sid] = User(
        name=name,
        sid=sid,
    )
    sessions[sid] = defaultdict(dict)
    log.info("New connection joined. %s => %s", sid, name)


@sio.on("disconnect")
async def sio_disconnect(sid):
    user = sid_to_user.pop(sid)
    _ = sessions.pop(sid)
    rooms = sio.rooms(sid)

    for room in rooms:
        await sio.emit("remove_player", {"user_id": user.uid}, room=room)


###########################
# Administrative Commands #
###########################

@sio.on("create_trivia")
async def create_trivia(sid, msg):
    name = msg["name"]
    questions = msg["questions"]

    trivia = Trivia(
        name=name,
        owner=sid_to_user[sid],
        config=Config(**msg["config"]),
        questions=[
            Question(
                text=question["text"],
                notes=question.get("notes"),
                choices=[
                    Choice(
                        id=i,
                        text=choice["text"],
                        correct=choice.get("correct", False)
                    ) for i, choice in enumerate(question["choices"])
                ]
            ) for question in questions
        ]
    )

    sessions[sid]["trivias"][trivia.uid] = trivia
    resp = dataclasses.asdict(trivia)
    print("response: %s", resp)
    await sio.emit("create_trivia", {
        "status": "ok",
        "obj": resp
    }, room=sid)


@sio.on("start_game")
async def start_game(sid, msg):
    # TODO: Generate easy to type, unique game id
    game_id = "foo"
    uid = msg["trivia_id"]

    trivia = sessions[sid]["trivias"].get(uid)
    if not trivia:
        await sio.emit("start_game", {
            "status": "error",
            "message": "Invalid trivia id"
        }, room=sid)
        return

    game = TriviaGame(game_id, trivia)
    games[game_id] = game
    sessions[sid]["game"] = game

    sio.enter_room(sid, game_id)

    await sio.emit("start_game", {
        "status": "ok",
        "game_id": game_id
    }, room=sid)


@sio.on("advance_question")
async def advance_question(sid, msg):
    game: TriviaGame = sessions[sid].get("game")

    game.advance_question()

    if game.current_question:
        await sio.emit("set_question", {
            "status": "ok",
            "question": dataclasses.asdict(game.current_question.question)
        }, room=game.game_id)
    else:
        # The game is over, send scores
        scores = game.get_scores()
        await sio.emit("scores", {
            "scores": {
                sid_to_user[sid].uid: score
                for sid, score in scores.items()
            }
        }, room=game.game_id)


###################
# Client commands #
###################

@sio.on("login")
async def login(sid, msg={}):
    user = sid_to_user.get(sid)
    name = msg.get("name") or randomname.get_name().replace('-', ' ').title()
    avatar_url = msg.get("avatar_url")
    if not user:
        user = User(
            name=name,
            sid=sid,
            avatar_url=avatar_url
        )
        sid_to_user[sid] = user
    else:
        user.name = name
        user.avatar_url = avatar_url

    await sio.emit("login", {
        "status": "ok",
        "user": dataclasses.asdict(user)
    }, room=sid)


@sio.on("submit_answer")
async def submit_answer(sid, msg):
    user = sid_to_user[sid]
    game_name = msg["game"]

    game = games.get(game_name)

    if not game or not game.current_question:
        await sio.emit("submit_answer", {
            "status": "error",
            "message": "No current question active"
        }, room=sid)
        return

    answer = msg["answer"]
    game.record_answer(sid, answer)
    await sio.emit("submit_answer", {"status", "ok"}, room=sid)

    # Always send to the host
    await sio.emit("set_answer", {
        "user_id": user.uid,
        "question": game.current_question.uid,
        "answer": answer
    }, room=game.owner.sid)

    # Only send to the room if players are configured
    if game.trivia.config.show_players:
        await sio.emit("set_answer", {
            "user_id": user.uid,
            "question": game.current_question.uid,
            "answer": answer
        }, room=game, skip_sid=game.owner.sid)


@sio.on("join")
async def join(sid, msg):
    user = sid_to_user[sid]
    game_name = msg["game"]

    if game_name not in games:
        await sio.emit("join", {"status", "error"}, room=sid)
        return

    sio.enter_room(sid, game_name)
    await sio.emit("join", {"status": "ok"}, room=sid)

    await sio.emit("add_player", {"user": user.asdict()}, room=game_name)


@sio.on("chat message")
async def chat_message(sid, msg):
    """Receive a chat message and send to all clients"""
    print(f"Server received: {msg}")
    await sio.emit('chat message', msg)
