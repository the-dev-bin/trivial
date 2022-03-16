import dataclasses
import logging

import names
import socketio
from starlette.applications import Starlette
from trivial.models import Choice, Question, Trivia, User

# from starlette.staticfiles import StaticFiles

log = logging.getLogger(__name__)


###################
# In Memory State #
###################

sid_to_user: dict[str, User] = {}
# Trivia game definitions
trivias = {}
# Active games
games = {}


app = Starlette(debug=True)
# app.mount('/', StaticFiles(directory='static'), name='static')


#######################
# Websocket Endpoints #
#######################
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app.mount('/sio', socketio.ASGIApp(sio))


async def get_user(sid):
    user = sid_to_user.get(sid)
    if user is None:
        log.error("User not found for sid %s", sid)
        await sio.emit({"error": "User not found!"})


@sio.on("connect")
def sio_connect(sid, environ):
    """Track user connection"""

    name = names.get_full_name()
    sid_to_user[sid] = User(
        name=name,
        sid=sid,
    )
    log.info("New connection joined. %s => %s", sid, name)


@sio.on("disconnect")
def sio_disconnect(sid):
    del sid_to_user[sid]


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
        config=msg["config"],
        challenges=[
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

    trivias[name] = trivia
    resp = dataclasses.asdict(trivia)
    print("response: %s", resp)
    await sio.emit("create_trivia", {
        "status": "ok",
        "obj": resp
    })


@sio.on("start_game")
async def start_game(sid, msg):
    pass


###################
# Client commands #
###################

@sio.on("login")
async def login(sid, msg):
    user = sid_to_user.get(sid)
    name = msg.get("name") or names.get_full_name()
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
    })


@sio.on("submit_answer")
async def submit_answer(sid, msg):
    game_name = msg["game"]

    game = games.get(game_name)

    if not game or not game.current_question:
        await sio.emit("submit_answer", {
            "status": "error",
            "message": "No current question active"
        })
        return

    game.record_answer(sid, msg["answer"])
    await sio.emit("submit_answer", {"status", "ok"})


@sio.on("join")
async def join(sid, msg):
    game_name = msg["game"]

    if game_name not in games:
        await sio.emit("join", {"status", "error"})

    sio.enter_room(sid, game_name)
    await sio.emit("join", {"status", "ok"})


@sio.on("chat message")
async def chat_message(sid, msg):
    """Receive a chat message and send to all clients"""
    print(f"Server received: {msg}")
    await sio.emit('chat message', msg)
