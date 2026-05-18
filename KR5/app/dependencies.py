from fastapi import Depends, Header, HTTPException

from app.schemas import User
from app.storage import Storage
from app.storage import storage as _storage


def get_current_user(
    x_user_id: str | None = Header(default=None),
    x_user_role: str = Header(default="user"),
) -> User:
    if x_user_id is None:
        raise HTTPException(status_code=401, detail="Missing X-User-Id header")
    try:
        uid = int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid X-User-Id header")
    return User(id=uid, role=x_user_role)


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


def get_storage() -> Storage:
    return _storage
