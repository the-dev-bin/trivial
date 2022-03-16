import dataclasses
import logging

import socketio
from starlette.applications import Starlette
from trivial.models import Choice, Question, Trivia, User

# from starlette.staticfiles import StaticFiles

log = logging.getLogger(__name__)


###################
# In Memory State #
###################

sid_to_user: dict[str, User] = {}
trivias = {}


app = Starlette(debug=True)
# app.mount('/', StaticFiles(directory='static'), name='static')


#######################
# Websocket Endpoints #
#######################
sio = socketio.AsyncServer(async_mode='asgi')
app.mount('/sio', socketio.ASGIApp(sio))


async def get_user(sid):
    user = sid_to_user.get(sid)
    if user is None:
        log.error("User not found for sid %s", sid)
        await sio.emit({"error": "User not found!"})


@sio.on("connect")
def sio_connect(sid, environ):
    """Track user connection"""
    # TODO: Generate random name?
    name = "foo"
    sid_to_user[sid] = User(
        name=name,
        sid=sid,
    )
    log.info("New connection joined. %s => %s", sid, name)


@sio.on("disconnect")
def sio_disconnect(sid):
    del sid_to_user[sid]


@sio.on("login")
async def login(sid, msg):
    name = msg.get("name")
    # TODO: Validate
    if name:
        sid_to_user[sid].name = name


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


@sio.on("create_challenge")
async def create_challenge(sid, msg):
    trivia_name = msg["trivia_name"]
    sid = msg["sid"]
    prompt = msg["prompt"]
    choices = msg["choices"]

    user = await get_user(sid)

    trivia = trivias.get(trivia_name)
    if trivia is None:
        await sio.emit({"error": f"Trivia named '{trivia_name}' not found"})
        return

    if trivia.owner != user:
        await sio.emit({"error": "You do not own this trivia"})
        return


@sio.on("chat message")
async def chat_message(sid, msg):
    """Receive a chat message and send to all clients"""
    print(f"Server received: {msg}")
    await sio.emit('chat message', msg)
