import json
import typing

import starlette.status as status
from fastapi import WebSocket, WebSocketDisconnect

from api.websockets.connection_manager import ConnectionManager

manager = ConnectionManager()


class WebsocketRoute:

    def __init__(self, websocket: WebSocket, participant_id: int):
        self._websocket = websocket
        self._participant_id = participant_id

    def __await__(self) -> typing.Generator:
        return self.dispatch().__await__()

    async def dispatch(self) -> None:
        # Websocket lifecycle
        await self._on_connect()

        close_code: int = status.WS_1000_NORMAL_CLOSURE
        try:
            while True:
                data = await self._websocket.receive_text()
                await self._on_receive(data)
        except WebSocketDisconnect:
            # Handle client normal disconnect here
            manager.disconnect(self._websocket)
            await manager.broadcast(f"Participant #{self._participant_id} left the chat", self._websocket)
        except Exception as exc:
            # Handle other types of errors here
            close_code = status.WS_1011_INTERNAL_ERROR
            raise exc from None
        finally:
            await self._on_disconnect(close_code)

    async def _on_connect(self):
        # Handle your new connection here
        await manager.connect(self._websocket, self._participant_id)
        await manager.broadcast(f"Participant #{self._participant_id} joined the chat", self._websocket)

    async def _on_disconnect(self, close_code: int):
        # Handle client disconnect here
        pass

    async def _on_receive(self, msg: typing.Any):
        # Handle participant messaging here
        message = json.loads(msg)
        if 'participant' in message:
            participant_websocket = manager.get_connection_by_participant_id(int(message['participant']))
            if participant_websocket is not None:
                await manager.send_message(
                    message=message['message'],
                    websocket=participant_websocket
                )
            else:
                await manager.send_message("This participant does not exist", self._websocket)
        else:
            await manager.broadcast(message=message['message'], websocket=self._websocket)

        await manager.send_message(f"You wrote: {message['message']}", self._websocket)
