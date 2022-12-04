from typing import List, Union

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.__active_connections: List[dict] = []

    async def connect(self, websocket: WebSocket, participant_id: int):
        await websocket.accept()
        self.__active_connections.append({'websocket': websocket, 'participant_id': participant_id})

    def disconnect(self, websocket: WebSocket):
        for connection in self.__active_connections:
            if connection['websocket'] == websocket:
                self.__active_connections.remove(connection)
                break

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, websocket: WebSocket):
        for connection in self.__active_connections:
            if connection['websocket'] != websocket:
                await connection['websocket'].send_text(message)

    def get_connection_by_participant_id(self, participant_id: int) -> Union[WebSocket, None]:
        for connection in self.__active_connections:
            if connection['participant_id'] == participant_id:
                return connection['websocket']
        return None
