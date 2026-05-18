"""Task 3: WebSocket chat room tests."""

import pytest


def test_ws_connect_valid(client):
    with client.websocket_connect("/ws/rooms/r_connect?username=alice") as ws:
        users = client.get("/rooms/r_connect/users").json()
        assert "alice" in users


def test_ws_send_receive(client):
    with client.websocket_connect("/ws/rooms/r_send?username=alice") as ws:
        ws.send_json({"type": "message", "text": "hello"})
        data = ws.receive_json()
        assert data["type"] == "message"
        assert data["text"] == "hello"
        assert data["username"] == "alice"
        assert data["room_id"] == "r_send"


def test_ws_multi_user_broadcast(client):
    with client.websocket_connect("/ws/rooms/r_multi?username=alice") as ws1:
        with client.websocket_connect("/ws/rooms/r_multi?username=bob") as ws2:
            ws1.send_json({"type": "message", "text": "hi all"})
            data1 = ws1.receive_json()
            data2 = ws2.receive_json()
            assert data1["text"] == "hi all"
            assert data2["text"] == "hi all"
            assert data2["username"] == "alice"


def test_ws_room_isolation(client):
    with client.websocket_connect("/ws/rooms/r_a?username=alice") as ws_a:
        with client.websocket_connect("/ws/rooms/r_b?username=bob"):
            users_a = client.get("/rooms/r_a/users").json()
            users_b = client.get("/rooms/r_b/users").json()
            assert "alice" in users_a
            assert "bob" not in users_a
            assert "bob" in users_b
            assert "alice" not in users_b


def test_ws_message_too_long(client):
    with client.websocket_connect("/ws/rooms/r_long?username=alice") as ws:
        ws.send_json({"type": "message", "text": "x" * 301})
        data = ws.receive_json()
        assert data["type"] == "error"
        assert data["detail"] == "Message is too long"


def test_ws_disconnect_removes_user(client):
    with client.websocket_connect("/ws/rooms/r_disc?username=alice"):
        pass
    resp = client.get("/rooms/r_disc/users")
    assert "alice" not in resp.json()
