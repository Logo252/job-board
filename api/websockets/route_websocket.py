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
            await manager.broadcast(f"Participant #{self._participant_id} left the chat")
        except Exception as exc:
            # Handle other types of errors here
            close_code = status.WS_1011_INTERNAL_ERROR
            raise exc from None
        finally:
            await self._on_disconnect(close_code)

    async def _on_connect(self):
        # Handle your new connection here
        await manager.connect(self._websocket)

    async def _on_disconnect(self, close_code: int):
        # Handle client disconnect here
        pass

    async def _on_receive(self, msg: typing.Any):
        # Handle participant messaging here
        await manager.send_personal_message(f"You wrote: {msg}", self._websocket)
        await manager.broadcast(f"Participant #{self._participant_id} says: {msg}")
