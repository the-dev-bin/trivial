import asyncio

import socketio

sio = socketio.AsyncClient()


async def main():
    future = asyncio.get_running_loop().create_future()

    @sio.on('chat message')
    def on_message_received(data):
        print(f"Client received: {data}")
        future.set_result(None)

    message = 20
    await sio.connect('http://localhost:8000', socketio_path='/sio/socket.io/')
    print(f"Client sends: {message}")
    await sio.emit('chat message', message)
    await asyncio.wait_for(future, timeout=1.0)
    await sio.disconnect()


asyncio.run(main())
