import logging

import socketio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from models import Trivia, User

# from starlette.staticfiles import StaticFiles

log = logging.getLogger(__name__)


###################
# In Memory State #
###################

sid_to_user: dict[str, User] = {}
trivias = {}


##################
# REST Endpoints #
##################
async def create_trivia(request):
    msg = await request.json()
    name = msg["name"]
    sid = msg["sid"]

    trivias[name] = Trivia(
        name=name,
        owner=sid,
        challenges=[]
    )


async def create_challenge(request):
    msg = await request.json()
    trivia_name = msg["trivia_name"]
    sid = msg["sid"]
    name = msg["name"]

    trivia = trivias.get(trivia_name)
    if trivia is None:
        return JSONResponse(
            {"message": f"Trivia named '{trivia_name}' not found"},
            status_code=404
        )


app = Starlette(
    routes=[
        Route("/trivia", create_trivia, methods=["PUT"]),
        Route("/challenge", create_challenge, methods=["PUT"])
    ],
    debug=True
)
# app.mount('/', StaticFiles(directory='static'), name='static')


#######################
# Websocket Endpoints #
#######################
sio = socketio.AsyncServer(async_mode='asgi')
app.mount('/sio', socketio.ASGIApp(sio))


@sio.on("connect")
def sio_connect(sid, environ):
    """Track user connection"""
    # TODO: Generate random name?
    name = "foo"
    sid_to_user[sid] = User(
        name=name,
        sid=sid,
        api_key="TODO: GENERATE ME"
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


@sio.on("chat message")
async def chat_message(sid, msg):
    """Receive a chat message and send to all clients"""
    print(f"Server received: {msg}")
    await sio.emit('chat message', msg)
