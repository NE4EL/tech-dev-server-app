import os

from fastapi import FastAPI, Query, WebSocket, WebSocketDisconnect

from app.routers import admin, tasks, users

app = FastAPI(title="Task Management API")

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(admin.router)


class RoomManager:
    def __init__(self) -> None:
        self._rooms: dict[str, dict[WebSocket, str]] = {}

    async def connect(self, room_id: str, ws: WebSocket, username: str) -> None:
        await ws.accept()
        self._rooms.setdefault(room_id, {})[ws] = username

    def disconnect(self, room_id: str, ws: WebSocket) -> None:
        room = self._rooms.get(room_id, {})
        room.pop(ws, None)
        if not room:
            self._rooms.pop(room_id, None)

    async def broadcast(self, room_id: str, message: dict) -> None:
        for ws in list(self._rooms.get(room_id, {}).keys()):
            try:
                await ws.send_json(message)
            except Exception:
                pass

    def get_users(self, room_id: str) -> list[str]:
        return list(self._rooms.get(room_id, {}).values())


room_manager = RoomManager()


@app.get("/health")
def health():
    return {"status": "ok", "env": os.getenv("APP_ENV", "local")}


@app.get("/rooms/{room_id}/users")
def get_room_users(room_id: str):
    return room_manager.get_users(room_id)


@app.websocket("/ws/rooms/{room_id}")
async def ws_room(
    room_id: str,
    ws: WebSocket,
    username: str = Query(default=""),
):
    if not username.strip():
        await ws.accept()
        await ws.close(code=1008)
        return

    await room_manager.connect(room_id, ws, username)
    try:
        while True:
            data = await ws.receive_json()
            text = data.get("text", "")
            if len(text) > 300:
                await ws.send_json({"type": "error", "detail": "Message is too long"})
            else:
                await room_manager.broadcast(
                    room_id,
                    {
                        "type": "message",
                        "room_id": room_id,
                        "username": username,
                        "text": text,
                    },
                )
    except WebSocketDisconnect:
        room_manager.disconnect(room_id, ws)
